from django.db import models
from common.base_models import TimeStampedModel


class SportStat(TimeStampedModel):
    COLOR_CHOICES = [
        ('blue',   "Ko'k"),
        ('green',  'Yashil'),
        ('orange', "To'q sariq"),
        ('purple', 'Binafsha'),
    ]

    title_uz = models.CharField(max_length=200, verbose_name="Tavsif (Uz)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Tavsif (Ru)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Tavsif (En)")
    value    = models.PositiveIntegerField(verbose_name="Qiymat (son)")
    suffix   = models.CharField(max_length=10, blank=True, default='+', verbose_name="Qo'shimcha belgi (+, K+)")
    color    = models.CharField(max_length=30, blank=True, default='', verbose_name="Rang kodi")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_sport_stat'
        ordering            = ['order']
        verbose_name        = 'Sport statistika'
        verbose_name_plural = 'Sport statistikalar'

    def __str__(self):
        return f"{self.value}{self.suffix} — {self.title_uz}"
