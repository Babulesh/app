from django.urls import path

from . import views

urlpatterns = [
    path("rooms/create/", views.create_room, name="create_room"),
    path("rooms/delete/", views.delete_room, name="delete_room"),
    path("rooms/list/", views.list_rooms, name="list_rooms"),
    path("bookings/create/", views.create_booking, name="create_booking"),
    path("bookings/delete/", views.delete_booking, name="delete_booking"),
    path("bookings/list/", views.list_bookings, name="list_bookings"),
]
