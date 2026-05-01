from django.db import models
from common.base_models import TimeStampedModel


class CallCenter(TimeStampedModel):
    """Call-center ma'lumotlari."""
    phone      = models.CharField(max_length=50, verbose_name="Telefon raqami")
    label_uz   = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Uz)")
    label_ru   = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    label_en   = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    working_hours_uz = models.CharField(max_length=200, blank=True, verbose_name="Ish vaqti (Uz)")
    working_hours_ru = models.CharField(max_length=200, blank=True, verbose_name="Ish vaqti (Ru)")
    working_hours_en = models.CharField(max_length=200, blank=True, verbose_name="Ish vaqti (En)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active  = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_call_center'
        verbose_name = "Call-center"
        verbose_name_plural = "Call-center raqamlari"
        ordering     = ['order']

    def __str__(self):
        return self.phone
