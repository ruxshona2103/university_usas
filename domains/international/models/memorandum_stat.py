from django.db import models

from common.base_models import TimeStampedModel


class MemorandumStat(TimeStampedModel):
    """Tashkilot bo'yicha imzolangan memorandumlar statistikasi."""

    organization_uz = models.CharField(max_length=500, verbose_name="Tashkilot nomi (Uz)")
    organization_ru = models.CharField(max_length=500, blank=True, verbose_name="Tashkilot nomi (Ru)")
    organization_en = models.CharField(max_length=500, blank=True, verbose_name="Tashkilot nomi (En)")
    foreign_count   = models.PositiveIntegerField(default=0, verbose_name="Xorijiy memorandumlar soni")
    domestic_count  = models.PositiveIntegerField(default=0, verbose_name="Mahalliy memorandumlar soni")
    order           = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'international_memorandum_stat'
        ordering            = ['order']
        verbose_name        = "Memorandum statistikasi"
        verbose_name_plural = "Memorandumlar statistikasi"

    def __str__(self):
        return self.organization_uz
