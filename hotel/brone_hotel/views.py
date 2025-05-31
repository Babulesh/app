from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import HotelRoom
import json

@require_http_methods(["POST"])
def create_room(request):
    try:
        data = json.loads(request.body)
        room = HotelRoom.objects.create(
            description=data['description'],
            price_per_night=data['price_per_night']
        )
        return JsonResponse({'room_id': room.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["DELETE"])
def delete_room(request):
    try:
        data = json.loads(request.body)
        room = HotelRoom.objects.get(id=data['room_id'])
        room.delete()
        return JsonResponse({'status': 'ok'})
    except HotelRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_rooms(request):
    sort_options = {
        'price_asc': 'price_per_night',
        'price_desc': '-price_per_night',
        'date_asc': 'created_at',
        'date_desc': '-created_at',
    }
    sort_by = request.GET.get('sort_by', 'date_desc')
    order_by = sort_options.get(sort_by, '-created_at')
    
    rooms = HotelRoom.objects.all().order_by(order_by)
    rooms_data = [{
        'room_id': room.id,
        'description': room.description,
        'price': float(room.price_per_night),
        'created_at': room.created_at.isoformat()
    } for room in rooms]
    
    return JsonResponse(rooms_data, safe=False)