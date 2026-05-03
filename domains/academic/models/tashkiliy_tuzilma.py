import os
import uuid

from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


def tashkiliy_tuzilma_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"academic/tashkiliy_tuzilma/{uuid.uuid4().hex}{ext}"


class TashkiliyTuzilmaItem(TimeStampedModel):
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    text_uz = models.TextField(verbose_name="Matn (Uz)")
    text_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    text_en = models.TextField(blank=True, verbose_name="Matn (En)")
    image = models.ImageField(
        upload_to=tashkiliy_tuzilma_image_upload,
        blank=True,
        null=True,
        verbose_name="Rasm",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table = "academic_tashkiliy_tuzilma_item"
        ordering = ["order", "created_at"]
        verbose_name = "Tashkiliy tuzilma elementi"
        verbose_name_plural = "Tashkiliy tuzilma elementlari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify((self.text_uz or "")[:80]) or uuid.uuid4().hex[:12]
            slug = base
            counter = 1
            while TashkiliyTuzilmaItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text_uz[:80]
