from rest_framework import serializers

from .models import Booking, HotelRoom


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ["id", "description", "price_per_night", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room", "date_start", "date_end"]
