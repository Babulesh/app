from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from ..models import HotelRoom
from ..serializers import RoomSerializer
from ..services.room_service import create_room, delete_room


class RoomViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = HotelRoom.objects.all().order_by("-created_at")
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        room = create_room(**ser.validated_data)
        headers = self.get_success_headers(ser.data)
        return Response({"room_id": room.id}, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        room_id = kwargs.get("pk")
        delete_room(room_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
