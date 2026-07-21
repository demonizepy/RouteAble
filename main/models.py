from django.db import models
from django.contrib.auth.models import User

# -------------------------------- Модели данных ---------------------------------

class Availability(models.Model):
    assistance = models.BooleanField(default=False, verbose_name="Требуется помощь")

    class Meta:
        verbose_name = "Доступность"
        verbose_name_plural = "Варианты доступности"

    def __str__(self):
        return "Доступен с помощью" if self.assistance else "Недоступен"


class House(models.Model):
    city = models.CharField(max_length=200, verbose_name="Город")
    street = models.CharField(max_length=500, verbose_name="Улица")
    number = models.CharField(max_length=100, verbose_name="Номер дома")
    floors = models.IntegerField(verbose_name="Этажи")

    # Параметры ЛИФТА
    has_elevator = models.BooleanField(default=False, verbose_name="Есть лифт")
    elevator_width = models.IntegerField(null=True, blank=True, verbose_name="Ширина лифта (см)")
    elevator_length = models.IntegerField(null=True, blank=True, verbose_name="Длина лифта (см)")

    # Параметры ПАНДУСА
    has_ramp = models.BooleanField(default=False, verbose_name="Есть пандус")
    ramp_degrees = models.FloatField(null=True, blank=True, verbose_name="Угол наклона пандуса (°)")
    ramp_length = models.FloatField(null=True, blank=True, verbose_name="Длина пандуса (м)")

    # Доступность и геопозиция
    availability = models.ForeignKey(
        'Availability', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Доступность"
    )
    
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"

    def __str__(self):
        return f"{self.city}, {self.street} {self.number}"