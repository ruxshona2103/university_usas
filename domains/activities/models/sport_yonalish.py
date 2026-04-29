from django.db import models
from common.base_models import TimeStampedModel


class SportYonalish(TimeStampedModel):
    """Sport yo'nalishlari — emoji icon, sarlavha va qisqa tavsif bilan."""

    icon           = models.CharField(max_length=20, blank=True, default='', verbose_name="Emoji yoki icon")
    title_uz       = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    title_ru       = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    title_en       = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    description_uz = models.TextField(blank=True, null=True, verbose_name="Qisqa tavsif (Uz)")
    description_ru = models.TextField(blank=True, null=True, verbose_name="Qisqa tavsif (Ru)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Qisqa tavsif (En)")
    order          = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active      = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_sport_yonalish'
        ordering            = ['order']
        verbose_name        = "Sport yo'nalishi"
        verbose_name_plural = "Sport yo'nalishlari"

    def __str__(self):
        return self.title_uz
