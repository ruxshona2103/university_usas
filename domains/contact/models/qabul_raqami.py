from django.db import models
from common.base_models import TimeStampedModel


class QabulRaqami(TimeStampedModel):
    label_uz = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    label_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    label_en = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    number   = models.CharField(max_length=50, verbose_name="Raqam")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'contact_qabul_raqami'
        ordering            = ['order']
        verbose_name        = "Qabul raqami"
        verbose_name_plural = "Qabul raqamlari"

    def __str__(self):
        return f"{self.label_uz} — {self.number}"
