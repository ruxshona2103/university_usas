import os
import uuid

from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


def savol_javob_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f"savol_javob/{name}{ext}"


class SavolJavobCategory(TimeStampedModel):
    """Savol-javob kategoriyalari (Qabul, Talabalik, Imtihon va h.k.) — ixtiyoriy."""

    name_uz = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")

    slug      = models.SlugField(max_length=220, unique=True, blank=True)
    icon      = models.CharField(max_length=64, blank=True, default="", verbose_name="Icon nomi (ixtiyoriy)")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = "pages_savol_javob_category"
        ordering            = ["order", "name_uz"]
        verbose_name        = "Savol-javob kategoriyasi"
        verbose_name_plural = "Savol-javob kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz) or "category"
            slug, n = base, 1
            while SavolJavobCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class SavolJavob(TimeStampedModel):
    """Sayt foydalanuvchilari uchun savol-javob (FAQ)."""

    category = models.ForeignKey(
        SavolJavobCategory,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="savol_javoblar",
        verbose_name="Kategoriya",
    )

    question_uz = models.CharField(max_length=500, verbose_name="Savol (Uz)")
    question_ru = models.CharField(max_length=500, blank=True, verbose_name="Savol (Ru)")
    question_en = models.CharField(max_length=500, blank=True, verbose_name="Savol (En)")

    answer_uz = models.TextField(verbose_name="Javob (Uz)")
    answer_ru = models.TextField(blank=True, verbose_name="Javob (Ru)")
    answer_en = models.TextField(blank=True, verbose_name="Javob (En)")

    image = models.ImageField(
        upload_to=savol_javob_image_upload,
        blank=True, null=True,
        verbose_name="Rasm (ixtiyoriy)",
    )

    slug         = models.SlugField(max_length=270, unique=True, blank=True)
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active    = models.BooleanField(default=True, verbose_name="Faolmi?")
    is_featured  = models.BooleanField(default=False, verbose_name="Tepada chiqsin?")
    views_count  = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")

    class Meta:
        db_table            = "pages_savol_javob"
        ordering            = ["-is_featured", "order", "-created_at"]
        verbose_name        = "Savol-javob"
        verbose_name_plural = "Savol-javoblar"
        indexes             = [
            models.Index(fields=["is_active", "order"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.question_uz[:80]) or "savol"
            slug, n = base, 1
            while SavolJavob.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_uz[:80]
