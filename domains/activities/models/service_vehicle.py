from django.db import models

from common.base_models import TimeStampedModel


class ServiceVehicle(TimeStampedModel):
    """Xizmat avtomototransport vositalari."""

    class FuelType(models.TextChoices):
        PETROL   = 'petrol',   'Benzin'
        DIESEL   = 'diesel',   'Dizel'
        GAS      = 'gas',      'Gaz'
        ELECTRIC = 'electric', 'Elektr'
        HYBRID   = 'hybrid',   'Gibrid'

    name = models.CharField(max_length=200, verbose_name="Rusumi (modeli)")

    vehicle_type_uz = models.CharField(max_length=200, verbose_name="Transport vositasi turi (Uz)")
    vehicle_type_ru = models.CharField(max_length=200, blank=True, verbose_name="Transport vositasi turi (Ru)")
    vehicle_type_en = models.CharField(max_length=200, blank=True, verbose_name="Transport vositasi turi (En)")

    manufactured_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name="Ishlab chiqarilgan yili",
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
        default=FuelType.PETROL,
        verbose_name="Yoqilg'i turi",
    )

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_service_vehicle'
        ordering            = ['order', 'created_at']
        verbose_name        = "Xizmat avtomobili"
        verbose_name_plural = "Xizmat avtomototransport vositalari"

    def __str__(self):
        return f"{self.name} ({self.get_fuel_type_display()})"
