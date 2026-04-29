import os
import uuid

from django.db import models
from common.base_models import TimeStampedModel


def tashkilot_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'academic/tashkilotlar/{uuid.uuid4().hex}{ext}'


class HuzuridagiTashkilot(TimeStampedModel):
    """
    Akademiya huzuridagi tashkilotlar.
    """
    name_uz        = models.CharField(max_length=400, verbose_name="Nomi (Uz)")
    name_ru        = models.CharField(max_length=400, blank=True, verbose_name="Nomi (Ru)")
    name_en        = models.CharField(max_length=400, blank=True, verbose_name="Nomi (En)")
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")
    image          = models.ImageField(upload_to=tashkilot_image_upload, blank=True, null=True, verbose_name="Rasm")
    website        = models.URLField(blank=True, verbose_name="Veb-sayt")
    phone          = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email          = models.CharField(max_length=200, blank=True, verbose_name="Email")
    address_uz     = models.CharField(max_length=400, blank=True, verbose_name="Manzil (Uz)")
    address_ru     = models.CharField(max_length=400, blank=True, verbose_name="Manzil (Ru)")
    address_en     = models.CharField(max_length=400, blank=True, verbose_name="Manzil (En)")
    order          = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active      = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'academic_huzuridagi_tashkilot'
        ordering            = ['order']
        verbose_name        = "Huzuridagi tashkilot"
        verbose_name_plural = "Akademiya huzuridagi tashkilotlar"

    def __str__(self):
        return self.name_uz
