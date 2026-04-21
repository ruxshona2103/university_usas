from django.db import models

from common.base_models import TimeStampedModel


class AcademyStat(TimeStampedModel):
    """Akademiya raqamlarda — statistik ko'rsatkichlar."""

    label_uz = models.CharField(max_length=300, verbose_name="Yorliq (Uz)")
    label_ru = models.CharField(max_length=300, blank=True, verbose_name="Yorliq (Ru)")
    label_en = models.CharField(max_length=300, blank=True, verbose_name="Yorliq (En)")

    value_uz = models.CharField(max_length=300, verbose_name="Qiymat (Uz)")
    value_ru = models.CharField(max_length=300, blank=True, verbose_name="Qiymat (Ru)")
    value_en = models.CharField(max_length=300, blank=True, verbose_name="Qiymat (En)")

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table   = 'academic_academy_stat'
        ordering   = ['order', 'created_at']
        verbose_name        = "Akademiya raqamda"
        verbose_name_plural = "Akademiya raqamlarda"

    def __str__(self):
        return self.label_uz
