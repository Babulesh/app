import json

from django.urls import reverse
from hotel.apps.brone_hotel.models import HotelRoom


def test_create_room_ok(client):
    url = reverse("room-list")
    payload = {"description": "Standard", "price_per_night": "1200.50"}

    resp = client.post(url, data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 201
    assert HotelRoom.objects.count() == 1
    assert resp.json()["room_id"] == HotelRoom.objects.first().id


def test_create_room_bad(client):
    url = reverse("room-list")

    for payload in [{}, {"description": "No price"}, {"price_per_night": -1}]:
        resp = client.post(url, data=json.dumps(payload), content_type="application/json")
        assert resp.status_code == 400
