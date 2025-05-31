from django.urls import path
from . import views

urlpatterns = [
    path('rooms/create/', views.create_room, name='create_room'),
    path('rooms/delete/', views.delete_room, name='delete_room'),
    path('rooms/list/', views.list_rooms, name='list_rooms'),
]