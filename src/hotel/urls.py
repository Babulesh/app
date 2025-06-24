from django.contrib import admin
from django.urls import include, path

from .health import healthcheck

urlpatterns = [
    path("health/", healthcheck),
    path("admin/", admin.site.urls),
    path("api/", include("hotel.apps.brone_hotel.urls")),
]
