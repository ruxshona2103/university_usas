import os
import uuid

from django.db import models
from common.base_models import TimeStampedModel


def almashinuv_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'international/almashinuv/{uuid.uuid4().hex}{ext}'


class AkademikAlmashinuv(TimeStampedModel):
    """Akademik almashinuv sahifasi — matn bo'limlari."""

    title_uz = models.CharField(max_length=400, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=400, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=400, blank=True, verbose_name="Sarlavha (En)")

    body_uz = models.TextField(verbose_name="Matn (Uz)")
    body_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    body_en = models.TextField(blank=True, verbose_name="Matn (En)")

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'international_akademik_almashinuv'
        ordering            = ['order']
        verbose_name        = "Akademik almashinuv bo'limi"
        verbose_name_plural = "Akademik almashinuv bo'limlari"

    def __str__(self):
        return self.title_uz


class AkademikAlmashinuvRasm(TimeStampedModel):
    """Bo'limga bog'liq rasmlar."""

    section = models.ForeignKey(
        AkademikAlmashinuv,
        on_delete=models.CASCADE,
        related_name='rasmlar',
        verbose_name="Bo'lim",
    )
    image   = models.ImageField(upload_to=almashinuv_image_upload, verbose_name="Rasm")
    caption_uz = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Uz)")
    caption_ru = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Ru)")
    caption_en = models.CharField(max_length=300, blank=True, verbose_name="Izoh (En)")
    order   = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'international_akademik_almashinuv_rasm'
        ordering            = ['order']
        verbose_name        = "Almashinuv rasmi"
        verbose_name_plural = "Almashinuv rasmlari"

    def __str__(self):
        return f"{self.section.title_uz} — rasm #{self.order}"
