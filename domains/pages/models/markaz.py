from django.db import models
from common.base_models import TimeStampedModel


def markaz_image_upload(instance, filename):
    import os
    name, ext = os.path.splitext(filename)
    return f'pages/markazlar/{instance.slug or name}{ext}'


class Markaz(TimeStampedModel):
    """
    Akademiya markazlari / bo'limlari.
    Har bir markaz rasm, matn + sub-bo'limlarga ega.
    """
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    name_uz = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    image = models.ImageField(
        upload_to=markaz_image_upload,
        null=True, blank=True,
        verbose_name="Rasm",
    )

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'pages_markaz'
        ordering            = ['order', 'name_uz']
        verbose_name        = "Markaz / Bo'lim"
        verbose_name_plural = "Markazlar / Bo'limlar"

    def __str__(self):
        return self.name_uz

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.name_uz) or f'markaz-{self.order}'
            slug = base
            counter = 1
            while Markaz.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class MarkazSubBolim(TimeStampedModel):
    """Sub-bo'lim — Markazga bog'langan."""
    markaz = models.ForeignKey(
        Markaz,
        on_delete=models.CASCADE,
        related_name='sub_bolimlar',
        verbose_name="Markaz",
    )

    name_uz = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'pages_markaz_sub_bolim'
        ordering            = ['order', 'name_uz']
        verbose_name        = "Sub-bo'lim"
        verbose_name_plural = "Sub-bo'limlar"

    def __str__(self):
        return f"{self.markaz.name_uz} → {self.name_uz}"
