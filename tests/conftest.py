import os

import django
import pytest
from rest_framework.test import APIClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel.settings_test")  # <— SQLite
django.setup()


@pytest.fixture(scope="session")
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def _enable_db_access(db):
    pass
