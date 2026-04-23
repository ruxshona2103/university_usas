import os
import uuid

from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


def rating_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'international/ratings/images/{uuid.uuid4().hex}{ext}'


def rating_cover_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'international/ratings/covers/{uuid.uuid4().hex}{ext}'


class InternationalRating(TimeStampedModel):
    """Xalqaro reyting — QS Stars, THE, UI Green Metric va h.k."""

    title_uz   = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru   = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en   = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(verbose_name="Matn (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Matn (En)")

    cover  = models.ImageField(
        upload_to=rating_cover_upload,
        blank=True, null=True,
        verbose_name="Muqova rasmi",
    )

    slug      = models.SlugField(max_length=350, unique=True, blank=True)
    date      = models.DateField(verbose_name="Sana")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'international_rating'
        ordering            = ['-date', 'order']
        verbose_name        = "Xalqaro reyting"
        verbose_name_plural = "Xalqaro reytinglar"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz)
            slug = base
            n = 1
            while InternationalRating.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz


class InternationalRatingImage(TimeStampedModel):
    """Reyting yozuviga bog'liq qo'shimcha rasmlar."""

    rating = models.ForeignKey(
        InternationalRating,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Reyting",
    )
    image = models.ImageField(upload_to=rating_image_upload, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'international_rating_image'
        ordering            = ['order']
        verbose_name        = "Reyting rasmi"
        verbose_name_plural = "Reyting rasmlari"

    def __str__(self):
        return f"{self.rating} — rasm #{self.order}"
