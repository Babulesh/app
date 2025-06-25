import json
from datetime import date, timedelta

from django.urls import reverse
from hotel.apps.brone_hotel.models import Booking, HotelRoom


def _room():
    return HotelRoom.objects.create(description="Suite", price_per_night=9999)


def test_booking_success(client):
    room = _room()
    url = reverse("booking-list")
    payload = {
        "room": room.id,
        "date_start": str(date.today() + timedelta(days=1)),
        "date_end": str(date.today() + timedelta(days=3)),
    }
    resp = client.post(url, data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 201
    assert Booking.objects.filter(room=room).count() == 1


def test_booking_conflict(client):
    room = _room()
    Booking.objects.create(
        room=room,
        date_start=date.today() + timedelta(days=5),
        date_end=date.today() + timedelta(days=7),
    )
    payload = {
        "room": room.id,
        "date_start": str(date.today() + timedelta(days=6)),
        "date_end": str(date.today() + timedelta(days=8)),
    }
    resp = client.post(reverse("booking-list"), data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 409
