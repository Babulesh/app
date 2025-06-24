from datetime import date

from django.db import transaction

from ..models import Booking, HotelRoom


def is_available(room: HotelRoom, start: date, end: date) -> bool:
    return not Booking.objects.filter(room=room, date_start__lt=end, date_end__gt=start).exists()


@transaction.atomic
def create_booking(room: HotelRoom, start: date, end: date) -> Booking:
    if not is_available(room, start, end):
        raise ValueError("Room is already booked for these dates")
    return Booking.objects.create(room=room, date_start=start, date_end=end)


def delete_booking(booking_id: int) -> None:
    Booking.objects.filter(id=booking_id).delete()
