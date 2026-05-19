import os
import uuid

from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


def national_rating_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'international/national-ratings/images/{uuid.uuid4().hex}{ext}'


class NationalRating(TimeStampedModel):
    name_uz = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")

    title_uz = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(verbose_name="Matn (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Matn (En)")

    slug = models.SlugField(max_length=350, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table = 'national_rating'
        ordering = ['order', '-created_at']
        verbose_name = "Milliy reyting"
        verbose_name_plural = "Milliy reytinglar"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz or self.name_uz)
            slug = base
            n = 1
            while NationalRating.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz or self.name_uz


class NationalRatingImage(TimeStampedModel):
    rating = models.ForeignKey(
        NationalRating,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Milliy reyting",
    )
    image_uz = models.FileField(upload_to=national_rating_image_upload, verbose_name="Rasm (Uz)")
    image_ru = models.FileField(upload_to=national_rating_image_upload, blank=True, null=True, verbose_name="Rasm (Ru)")
    image_en = models.FileField(upload_to=national_rating_image_upload, blank=True, null=True, verbose_name="Rasm (En)")
    alt_uz = models.CharField(max_length=300, blank=True, verbose_name="Alt (Uz)")
    alt_ru = models.CharField(max_length=300, blank=True, verbose_name="Alt (Ru)")
    alt_en = models.CharField(max_length=300, blank=True, verbose_name="Alt (En)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'national_rating_image'
        ordering = ['order']
        verbose_name = "Milliy reyting rasmi"
        verbose_name_plural = "Milliy reyting rasmlari"

    def __str__(self):
        return f"{self.rating} - rasm #{self.order}"

