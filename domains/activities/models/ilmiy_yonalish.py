import os
import uuid

from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


def ilmiy_yonalish_image_upload(instance, filename):
    ext  = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f'ilmiy_yonalish/images/{name}{ext}'


class IlmiyYonalish(TimeStampedModel):
    """Ilmiy yo'nalish (parent) — faqat name + slug."""

    name_uz = models.CharField(max_length=255, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=255, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=255, blank=True, verbose_name="Nomi (En)")

    slug      = models.SlugField(max_length=270, unique=True, blank=True)
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_ilmiy_yonalish'
        ordering            = ['order', 'name_uz']
        verbose_name        = "Ilmiy yo'nalish"
        verbose_name_plural = "Ilmiy yo'nalishlar"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz) or 'yonalish'
            slug, n = base, 1
            while IlmiyYonalish.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class IlmiyYonalishItem(TimeStampedModel):
    """Ilmiy yo'nalish ichidagi element (child) — name, description, photo, slug."""

    yonalish = models.ForeignKey(
        IlmiyYonalish,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Yo'nalish",
    )

    name_uz = models.CharField(max_length=255, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=255, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=255, blank=True, verbose_name="Nomi (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    photo = models.FileField(
        upload_to=ilmiy_yonalish_image_upload,
        blank=True, null=True,
        verbose_name="Rasm",
    )

    slug      = models.SlugField(max_length=270, unique=True, blank=True)
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_ilmiy_yonalish_item'
        ordering            = ['order', 'name_uz']
        verbose_name        = "Ilmiy yo'nalish elementi"
        verbose_name_plural = "Ilmiy yo'nalish elementlari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz) or 'item'
            slug, n = base, 1
            while IlmiyYonalishItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz
