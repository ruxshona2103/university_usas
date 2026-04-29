from django.db import models
from common.base_models import TimeStampedModel


class SportTadbir(TimeStampedModel):
    """Yillik sport tadbirlari."""

    title_uz       = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru       = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en       = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    description_uz = models.TextField(blank=True, null=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, null=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Tavsif (En)")
    event_date     = models.DateField(blank=True, null=True, verbose_name="Sana")
    location_uz    = models.CharField(max_length=200, blank=True, verbose_name="Joyi (Uz)")
    location_ru    = models.CharField(max_length=200, blank=True, verbose_name="Joyi (Ru)")
    location_en    = models.CharField(max_length=200, blank=True, verbose_name="Joyi (En)")
    order          = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active      = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_sport_tadbir'
        ordering            = ['order', 'event_date']
        verbose_name        = 'Sport tadbiri'
        verbose_name_plural = 'Sport tadbirlari'

    def __str__(self):
        return self.title_uz
