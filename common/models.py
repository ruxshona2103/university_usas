from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

from .base_models import TimeStampedModel


class Tag(TimeStampedModel):
    name_uz = models.CharField(max_length=100, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Nomi (En)")
    slug    = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        db_table         = 'common_tag'
        verbose_name     = 'Tag'
        verbose_name_plural = 'Taglar'
        ordering         = ['name_uz']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz)
            slug = base
            counter = 1
            while Tag.objects.filter(slug=slug).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class ContentImage(TimeStampedModel):
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    image = models.ImageField(upload_to='content_images/%Y/%m/', verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table         = 'common_content_image'
        verbose_name     = 'Kontent rasmi'
        verbose_name_plural = 'Kontent rasmlari'
        ordering         = ['order']

    def __str__(self):
        return f'Image #{self.order} — {self.content_type}'
