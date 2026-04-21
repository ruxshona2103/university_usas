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
    """Ilmiy faoliyat — maqolalar, hisobotlar, ko'rsatmalar va boshqa hujjatlar."""

    class CategoryChoices(models.TextChoices):
        ARTICLE     = 'article',     "Maqola"
        MONOGRAPH   = 'monograph',   "Monografiya"
        MANUAL      = 'manual',      "O'quv qo'llanma"
        REPORT      = 'report',      "Hisobot"
        PATENT      = 'patent',      "Patent"
        CONFERENCE  = 'conference',  "Konferensiya"
        OTHER       = 'other',       "Boshqa"

    # ── Sarlavha (3 til) ───────────────────────────────────────────────────
    title_uz = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")

    # ── Tavsif / annotatsiya (3 til) ───────────────────────────────────────
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    # ── Kategoriya (ixtiyoriy) ─────────────────────────────────────────────
    category_fk = models.ForeignKey(
        IlmiyFaoliyatCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='items',
        verbose_name="Kategoriya",
    )

    # ── Muallif va yil ─────────────────────────────────────────────────────
    author    = models.CharField(max_length=300, blank=True, verbose_name="Muallif(lar)")
    year      = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Yil")
    category  = models.CharField(
        max_length=30,
        choices=CategoryChoices.choices,
        default=CategoryChoices.OTHER,
        verbose_name="Turi",
    )

    # ── Rasm va fayl ──────────────────────────────────────────────────────
    image = models.ImageField(
        upload_to=ilmiy_image_upload,
        blank=True,
        null=True,
        verbose_name="Muqova rasmi",
    )
    file = models.FileField(
        upload_to=ilmiy_file_upload,
        blank=True,
        null=True,
        verbose_name="Fayl (PDF / DOC)",
        help_text="PDF, DOCX, DOC, PPTX formatlari qo'llab-quvvatlanadi",
    )

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_ilmiy_faoliyat'
        ordering            = ['-year', 'order']
        verbose_name        = "Ilmiy faoliyat"
        verbose_name_plural = "Ilmiy faoliyat"

    def __str__(self):
        return self.title_uz
