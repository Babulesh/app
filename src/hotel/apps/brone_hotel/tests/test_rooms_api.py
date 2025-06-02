import json
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from brone_hotel.models import HotelRoom


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_create_room_success(client: APIClient):
    url = reverse("create_room")
    data = {"description": "Standard Room", "price_per_night": 5000.00}
    response = client.post(url, data=json.dumps(data), content_type="application/json")
    response_data = response.json()

    assert response.status_code == 201
    assert "room_id" in response_data
    assert HotelRoom.objects.count() == 1


@pytest.mark.django_db
def test_create_room_invalid_data(client: APIClient):
    url = reverse("create_room")
    test_cases = [
        ({}, 400),  # Пустые данные
        ({"description": "No price"}, 400),  # Нет цены
        ({"price_per_night": 100}, 400),  # Нет описания
        ({"description": "Test", "price_per_night": -100}, 400),  # Отрицательная цена
    ]

    for data, expected_status in test_cases:
        response = client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        assert response.status_code == expected_status
        if expected_status == 400:
            response_data = response.json()
            assert "error" in response_data


@pytest.mark.django_db
def test_list_rooms_sorting(client: APIClient):
    # Создаем тестовые данные
    HotelRoom.objects.create(
        description="Budget Room",
        price_per_night=5000.00,
        created_at=timezone.now() - timedelta(days=1),
    )

    HotelRoom.objects.create(
        description="Luxury Room", price_per_night=20000.00, created_at=timezone.now()
    )

    # Тестируем разные варианты сортировки
    sort_cases = [
        ("price_asc", [5000.0, 20000.0]),
        ("price_desc", [20000.0, 5000.0]),
        ("date_asc", [5000.0, 20000.0]),  # room1 создан раньше
        ("date_desc", [20000.0, 5000.0]),
    ]

    for sort_by, expected_prices in sort_cases:
        url = reverse("list_rooms") + f"?sort_by={sort_by}"
        response = client.get(url)
        response_data = response.json()

        assert response.status_code == 200
        assert len(response_data) == 2
        assert [r["price"] for r in response_data] == expected_prices
