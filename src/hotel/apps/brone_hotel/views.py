import json
import logging
from datetime import date, datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Booking, HotelRoom

logger = logging.getLogger(__name__)


def validate_required_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return JsonResponse(
            {"error": f'Missing required fields: {", ".join(missing_fields)}'},
            status=400,
        )
    return None


@csrf_exempt
@require_http_methods(["POST"])
def create_room(request):
    try:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        error_response = validate_required_fields(
            data, ["description", "price_per_night"]
        )
        if error_response:
            return error_response

        try:
            price = float(data["price_per_night"])
            if price <= 0:
                return JsonResponse({"error": "Price must be positive"}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid price format"}, status=400)

        room = HotelRoom.objects.create(
            description=data["description"], price_per_night=price
        )
        return JsonResponse({"room_id": room.id}, status=201)

    except Exception as e:
        logger.error(f"Error in create_room: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_room(request):
    try:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        error_response = validate_required_fields(data, ["room_id"])
        if error_response:
            return error_response

        try:
            room = HotelRoom.objects.get(id=data["room_id"])
            room.delete()
            return JsonResponse({"status": "ok"})
        except HotelRoom.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)
        except ValueError:
            return JsonResponse({"error": "room_id must be an integer"}, status=400)

    except Exception as e:
        logger.error(f"Error in delete_room: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_rooms(request):
    try:
        sort_options = {
            "price_asc": "price_per_night",
            "price_desc": "-price_per_night",
            "date_asc": "created_at",
            "date_desc": "-created_at",
        }
        sort_by = request.GET.get("sort_by", "date_desc")
        order_by = sort_options.get(sort_by, "-created_at")

        rooms = HotelRoom.objects.all().order_by(order_by)
        rooms_data = [
            {
                "room_id": room.id,
                "description": room.description,
                "price": float(room.price_per_night),
                "created_at": room.created_at.isoformat(),
            }
            for room in rooms
        ]

        return JsonResponse(rooms_data, safe=False)
    except Exception as e:
        logger.error(f"Error in list_rooms: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_booking(request):
    try:
        data = json.loads(request.body)

        # Проверка обязательных полей
        required_fields = ["room_id", "date_start", "date_end"]
        if any(field not in data for field in required_fields):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Валидация room_id
        try:
            room_id = int(data["room_id"])
            room = HotelRoom.objects.get(id=room_id)
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "room_id must be a valid integer"}, status=400
            )
        except HotelRoom.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=400)

        try:
            date_start = datetime.strptime(data["date_start"], "%Y-%m-%d").date()
            date_end = datetime.strptime(data["date_end"], "%Y-%m-%d").date()

            if date_start < date.today():
                return JsonResponse(
                    {"error": "Start date cannot be in the past"}, status=400
                )

            if date_end <= date_start:
                return JsonResponse(
                    {"error": "End date must be after start date"}, status=400
                )

        except ValueError:
            return JsonResponse(
                {"error": "Invalid date format (use YYYY-MM-DD)"}, status=400
            )

        if Booking.objects.filter(
            room=room, date_start__lt=date_end, date_end__gt=date_start
        ).exists():
            return JsonResponse(
                {"error": "Room is already booked for these dates"}, status=409
            )

        booking = Booking.objects.create(
            room=room, date_start=date_start, date_end=date_end
        )
        return JsonResponse({"booking_id": booking.id}, status=201)

    except Exception as e:
        logger.error(f"Error in create_booking: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_booking(request):
    try:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        error_response = validate_required_fields(data, ["booking_id"])
        if error_response:
            return error_response

        try:
            booking = Booking.objects.get(id=data["booking_id"])
            booking.delete()
            return JsonResponse({"status": "ok"})
        except Booking.DoesNotExist:
            return JsonResponse({"error": "Booking not found"}, status=404)
        except ValueError:
            return JsonResponse({"error": "booking_id must be an integer"}, status=400)

    except Exception as e:
        logger.error(f"Error in delete_booking: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)


@require_http_methods(["GET"])
def list_bookings(request):
    try:
        room_id = request.GET.get("room_id")
        if not room_id:
            return JsonResponse({"error": "room_id parameter is required"}, status=400)

        try:
            room_id = int(room_id)
        except ValueError:
            return JsonResponse({"error": "room_id must be an integer"}, status=400)

        if not HotelRoom.objects.filter(id=room_id).exists():
            return JsonResponse({"error": "Room not found"}, status=404)

        bookings = Booking.objects.filter(room_id=room_id).order_by("date_start")
        bookings_data = [
            {
                "booking_id": b.id,
                "date_start": b.date_start.strftime("%Y-%m-%d"),
                "date_end": b.date_end.strftime("%Y-%m-%d"),
            }
            for b in bookings
        ]

        return JsonResponse(bookings_data, safe=False)
    except Exception as e:
        logger.error(f"Error in list_bookings: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)
