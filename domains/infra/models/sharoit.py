import os
import uuid

from django.db import models
from common.base_models import TimeStampedModel


def sharoit_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'infra/sharoit/{uuid.uuid4().hex}{ext}'


class Sharoit(TimeStampedModel):
    """
    Yaratilgan sharoit va imkoniyatlar — har bir element
    (Ta'lim uchun sharoitlar va Sport inshootlar bo'limlari).
    """

    class Category(models.TextChoices):
        SPORT  = 'sport',  'Zamonaviy sport inshootlar'
        TALIM  = 'talim',  "Ta'lim uchun sharoitlar"

    category    = models.CharField(
        max_length=10,
        choices=Category.choices,
        default=Category.TALIM,
        verbose_name="Bo'lim",
        db_index=True,
    )
    title_uz    = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    title_ru    = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    title_en    = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")
    image       = models.ImageField(upload_to=sharoit_image_upload, blank=True, null=True, verbose_name="Rasm")
    icon        = models.CharField(max_length=100, blank=True, verbose_name="Icon (CSS class yoki emoji)")
    order       = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active   = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'infra_sharoit'
        ordering            = ['category', 'order']
        verbose_name        = "Sharoit va imkoniyat"
        verbose_name_plural = "Sharoit va imkoniyatlar"

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title_uz}"
