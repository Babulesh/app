import json
from datetime import date, timedelta

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from brone_hotel.models import Booking, HotelRoom


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def sample_room():
    return HotelRoom.objects.create(description="Test Room", price_per_night=10000.00)


@pytest.fixture
def sample_booking(sample_room):
    return Booking.objects.create(
        room=sample_room,
        date_start=date.today() + timedelta(days=1),
        date_end=date.today() + timedelta(days=3),
    )


@pytest.mark.django_db
def test_create_booking_success(client, sample_room):
    url = reverse("create_booking")
    data = {
        "room_id": sample_room.id,
        "date_start": str(date.today() + timedelta(days=5)),
        "date_end": str(date.today() + timedelta(days=7)),
    }
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    response_data = response.json()

    assert response.status_code == 201
    assert "booking_id" in response_data
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_create_booking_invalid_dates(client, sample_room):
    test_cases = [
        (
            {  # Даты в прошлом
                "room_id": sample_room.id,
                "date_start": "2020-01-01",
                "date_end": "2020-01-02",
            },
            "in the past",
        ),
        (
            {  # Неправильный формат даты
                "room_id": sample_room.id,
                "date_start": "01-01-2023",
                "date_end": "02-01-2023",
            },
            "invalid date format",
        ),
        (
            {
                "room_id": sample_room.id,
                "date_start": str(date.today() + timedelta(days=3)),
                "date_end": str(date.today() + timedelta(days=1)),
            },
            "must be after start date",
        ),
        (
            {  # Несуществующий номер
                "room_id": 99999,
                "date_start": str(date.today()),
                "date_end": str(date.today() + timedelta(days=1)),
            },
            "room not found",
        ),
    ]

    for data, error_keyword in test_cases:
        response = client.post(
            reverse("create_booking"),
            data=json.dumps(data),
            content_type="application/json",
        )
        response_data = response.json()

        # Основные проверки
        assert response.status_code == 400, f"Expected 400 for data: {data}"
        assert "error" in response_data, "Error message missing in response"
        assert error_keyword in response_data["error"].lower(), "Wrong error message"


@pytest.mark.django_db
def test_booking_conflict(client, sample_room, sample_booking):
    url = reverse("create_booking")
    data = {
        "room_id": sample_room.id,
        "date_start": str(sample_booking.date_start),
        "date_end": str(sample_booking.date_end),
    }
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    response_data = response.json()

    assert response.status_code == 409
    assert "error" in response_data
    assert "already booked" in response_data["error"].lower()


@pytest.mark.django_db
def test_list_bookings(client, sample_room, sample_booking):
    url = reverse("list_bookings")
    response = client.get(url, {"room_id": sample_room.id})
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1
    assert response_data[0]["booking_id"] == sample_booking.id
