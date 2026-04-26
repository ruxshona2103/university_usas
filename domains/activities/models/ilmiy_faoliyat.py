import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel
from .ilmiy_faoliyat_category import IlmiyFaoliyatCategory


def ilmiy_file_upload(instance, filename):
    ext  = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f'ilmiy_faoliyat/files/{name}{ext}'


def ilmiy_image_upload(instance, filename):
    ext  = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f'ilmiy_faoliyat/images/{name}{ext}'


class IlmiyFaoliyat(TimeStampedModel):
    """Ilmiy faoliyat — fayl va muqova rasmi bilan kategoriyaga bog'langan yozuv."""

    category = models.ForeignKey(
        IlmiyFaoliyatCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='items',
        verbose_name="Kategoriya",
    )
    title_uz       = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru       = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en       = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")
    description_uz = models.TextField(blank=True, null=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, null=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Tavsif (En)")

    image = models.FileField(
        upload_to=ilmiy_image_upload,
        blank=True, null=True,
        verbose_name="Muqova rasmi",
    )
    file = models.FileField(
        upload_to=ilmiy_file_upload,
        blank=True, null=True,
        max_length=500,
        verbose_name="Fayl (PDF / DOC)",
        help_text="PDF, DOCX, DOC, PPTX formatlari qo'llab-quvvatlanadi",
    )
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_ilmiy_faoliyat'
        ordering            = ['order']
        verbose_name        = "O'quv faoliyat"
        verbose_name_plural = "O'quv faoliyat"

    def __str__(self):
        return self.title_uz
