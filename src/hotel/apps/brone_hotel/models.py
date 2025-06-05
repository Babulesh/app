from django.db import models
from django.utils import timezone


class HotelRoom(models.Model):
    description = models.TextField(verbose_name="Описание номера")
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за ночь"
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Номер отеля"
        verbose_name_plural = "Номера отелей"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Номер #{self.id} - {self.description[:50]}..."


class Booking(models.Model):
    room = models.ForeignKey(
        HotelRoom,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Номер отеля",
    )
    date_start = models.DateField(verbose_name="Дата заезда")
    date_end = models.DateField(verbose_name="Дата выезда")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["date_start"]

    def __str__(self):
        return f"Бронь #{self.id} (Номер #{self.room_id})"
