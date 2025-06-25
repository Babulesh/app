# apps/brone_hotel/services/room_service.py
from decimal import Decimal

from django.db import transaction

from ..models import HotelRoom


def create_room(description: str, price_per_night: Decimal) -> HotelRoom:
    with transaction.atomic():
        return HotelRoom.objects.create(
            description=description,
            price_per_night=price_per_night,
        )


def delete_room(room_id: int) -> None:
    HotelRoom.objects.filter(id=room_id).delete()
