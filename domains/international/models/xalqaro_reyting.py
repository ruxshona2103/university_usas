import os
import uuid

from django.db import models
from django.utils.text import slugify
from common.base_models import TimeStampedModel


def xalqaro_reyting_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'international/xalqaro_reyting/{uuid.uuid4().hex}{ext}'


class XalqaroReytingBolim(TimeStampedModel):
    """
    Xalqaro reyting bo'limi — masalan:
      - Sportchilar reytingi
      - Professor-o'qituvchilar reytingi
    """
    TYPE_SPORT     = 'sport'
    TYPE_PROFESSOR = 'professor'
    TYPE_CHOICES   = [
        (TYPE_SPORT,     'Sportchilar reytingi'),
        (TYPE_PROFESSOR, "Professor-o'qituvchilar reytingi"),
    ]

    bolim_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES,
        verbose_name="Bo'lim turi",
    )
    title_uz = models.CharField(max_length=400, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=400, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=400, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    image    = models.ImageField(
        upload_to=xalqaro_reyting_image_upload, blank=True, null=True, verbose_name="Rasm (screenshot)"
    )
    link      = models.URLField(blank=True, verbose_name="Tashqi havola (URL)")
    slug      = models.SlugField(max_length=450, unique=True, blank=True, verbose_name="Slug")

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'international_xalqaro_reyting_bolim'
        ordering            = ['bolim_type', 'order']
        verbose_name        = "Xalqaro reyting bo'limi"
        verbose_name_plural = "Xalqaro reyting bo'limlari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz, allow_unicode=True) or str(self.id)
            slug = base
            n = 1
            while XalqaroReytingBolim.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_bolim_type_display()}] {self.title_uz}"
