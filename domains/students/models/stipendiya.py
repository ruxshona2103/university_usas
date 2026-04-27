from django.db import models

from common.base_models import TimeStampedModel


class Stipendiya(TimeStampedModel):
    """Akademiyada tayinlanadigan stipendiyalar miqdori jadvali."""

    status_uz = models.CharField(max_length=200, verbose_name="Status (Uz)")
    status_ru = models.CharField(max_length=200, blank=True, verbose_name="Status (Ru)")
    status_en = models.CharField(max_length=200, blank=True, verbose_name="Status (En)")

    # "569 670" kabi formatlangan ko'rsatish uchun string, lekin sorting uchun int ham kerak
    amount     = models.PositiveIntegerField(verbose_name="Oylik miqdori (so'm)")

    # "+20%", "+50%" kabi izoh — ixtiyoriy
    note_uz   = models.CharField(max_length=50, blank=True, verbose_name="Izoh (Uz)")
    note_ru   = models.CharField(max_length=50, blank=True, verbose_name="Izoh (Ru)")
    note_en   = models.CharField(max_length=50, blank=True, verbose_name="Izoh (En)")

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'students_stipendiya'
        ordering            = ['order']
        verbose_name        = "Stipendiya"
        verbose_name_plural = "Stipendiyalar"

    def __str__(self):
        return f"{self.status_uz} — {self.amount:,} so'm"
