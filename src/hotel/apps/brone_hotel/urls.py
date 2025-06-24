from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.booking import BookingViewSet
from .views.room import RoomViewSet

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
]
