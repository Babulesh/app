from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from ..models import Booking, HotelRoom
from ..serializers import BookingSerializer
from ..services.booking_service import create_booking, delete_booking


class BookingViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.select_related("room").all().order_by("date_start")
    serializer_class = BookingSerializer

    def list(self, request, *args, **kwargs):
        room_id = request.query_params.get("room_id")
        if not room_id:
            return Response({"error": "room_id query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            qs = self.queryset.filter(room_id=int(room_id))
        except ValueError:
            return Response({"error": "room_id must be integer"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        room = HotelRoom.objects.get(pk=data["room"].id)
        try:
            booking = create_booking(room, data["date_start"], data["date_end"])
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        delete_booking(kwargs["pk"])
        return Response(status=status.HTTP_204_NO_CONTENT)
