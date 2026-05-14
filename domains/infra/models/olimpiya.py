import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel


def olimpiya_gallery_upload(instance, filename):
    ext  = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f'infra/olimpiya/gallery/{name}{ext}'


class OlimpiyaShaharchasi(TimeStampedModel):
    """
    Olimpiya shaharchasi haqida umumiy ma'lumot — singleton.
    Admin panelda faqat bitta yozuv bo'ladi.
    """

    intro_uz = models.TextField(blank=True, verbose_name="Kirish matni (Uz)")
    intro_ru = models.TextField(blank=True, verbose_name="Kirish matni (Ru)")
    intro_en = models.TextField(blank=True, verbose_name="Kirish matni (En)")

    gallery_title_uz = models.CharField(max_length=300, blank=True, default="Fotogaleriya", verbose_name="Galereya sarlavhasi (Uz)")
    gallery_title_ru = models.CharField(max_length=300, blank=True, default="Фотогалерея",  verbose_name="Galereya sarlavhasi (Ru)")
    gallery_title_en = models.CharField(max_length=300, blank=True, default="Photo gallery", verbose_name="Galereya sarlavhasi (En)")

    class Meta:
        db_table            = 'infra_olimpiya_shaharchasi'
        verbose_name        = "Olimpiya shaharchasi"
        verbose_name_plural = "Olimpiya shaharchasi"

    def __str__(self):
        return "Olimpiya shaharchasi ma'lumotlari"


class OlimpiyaGalleryImage(TimeStampedModel):
    """Olimpiya shaharchasi fotogalereyasi."""

    shaharchasi = models.ForeignKey(
        OlimpiyaShaharchasi,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name="Shaharchasi",
    )
    image   = models.FileField(upload_to=olimpiya_gallery_upload, verbose_name="Rasm")
    caption_uz = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Uz)")
    caption_ru = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Ru)")
    caption_en = models.CharField(max_length=300, blank=True, verbose_name="Izoh (En)")
    order   = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'infra_olimpiya_gallery_image'
        ordering            = ['order']
        verbose_name        = "Galereya rasmi"
        verbose_name_plural = "Galereya rasmlari"

    def __str__(self):
        return f"Rasm #{self.order}"
