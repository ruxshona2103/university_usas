import os
import uuid

from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


def majmua_image_upload(instance, filename):
    ext  = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f'infra/images/{name}{ext}'


class SportMajmua(TimeStampedModel):
    """Sport majmuasi — pasporti bilan."""

    name_uz     = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    name_ru     = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    name_en     = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")

    # "Olimpiya shaharchasi hududidagi" kabi joylashuv
    location_uz = models.CharField(max_length=300, blank=True, verbose_name="Joylashuvi (Uz)")
    location_ru = models.CharField(max_length=300, blank=True, verbose_name="Joylashuvi (Ru)")
    location_en = models.CharField(max_length=300, blank=True, verbose_name="Joylashuvi (En)")

    slug      = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'infra_sport_majmua'
        ordering            = ['order']
        verbose_name        = "Sport majmuasi"
        verbose_name_plural = "Sport majmualari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz)
            slug, n = base, 1
            while SportMajmua.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class SportMajmuaImage(TimeStampedModel):
    """Majmuaning rasmlari (galereya)."""

    majmua = models.ForeignKey(
        SportMajmua,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Majmua",
    )
    image = models.FileField(upload_to=majmua_image_upload, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'infra_sport_majmua_image'
        ordering = ['order']
        verbose_name        = "Majmua rasmi"
        verbose_name_plural = "Majmua rasmlari"

    def __str__(self):
        return f"Rasm #{self.order} — {self.majmua.name_uz}"


class SportMajmuaStat(TimeStampedModel):
    """Texnik ko'rsatkichlar jadvali — label:value juftlari."""

    majmua    = models.ForeignKey(
        SportMajmua,
        on_delete=models.CASCADE,
        related_name='stats',
        verbose_name="Majmua",
    )
    label_uz  = models.CharField(max_length=300, verbose_name="Maydon nomi (Uz)")
    label_ru  = models.CharField(max_length=300, blank=True, verbose_name="Maydon nomi (Ru)")
    label_en  = models.CharField(max_length=300, blank=True, verbose_name="Maydon nomi (En)")
    value_uz  = models.CharField(max_length=500, verbose_name="Qiymati (Uz)")
    value_ru  = models.CharField(max_length=500, blank=True, verbose_name="Qiymati (Ru)")
    value_en  = models.CharField(max_length=500, blank=True, verbose_name="Qiymati (En)")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'infra_sport_majmua_stat'
        ordering            = ['order']
        verbose_name        = "Texnik ko'rsatkich"
        verbose_name_plural = "Texnik ko'rsatkichlar"

    def __str__(self):
        return f"{self.majmua.name_uz} — {self.label_uz}"


class SportMajmuaSportTuri(TimeStampedModel):
    """Majmuada foydalaniladigan sport turlari."""

    majmua   = models.ForeignKey(
        SportMajmua,
        on_delete=models.CASCADE,
        related_name='sport_types',
        verbose_name="Majmua",
    )
    name_uz  = models.CharField(max_length=200, verbose_name="Sport turi (Uz)")
    name_ru  = models.CharField(max_length=200, blank=True, verbose_name="Sport turi (Ru)")
    name_en  = models.CharField(max_length=200, blank=True, verbose_name="Sport turi (En)")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'infra_sport_majmua_sport_turi'
        ordering            = ['order']
        verbose_name        = "Sport turi"
        verbose_name_plural = "Sport turlari"

    def __str__(self):
        return f"{self.majmua.name_uz} — {self.name_uz}"


class SportMajmuaTadbir(TimeStampedModel):
    """Sport tadbirlari — xalqaro va mahalliy darajada."""

    class Level(models.TextChoices):
        INTERNATIONAL = 'xalqaro', 'Xalqaro'
        LOCAL         = 'maxaliy', 'Mahalliy'

    majmua   = models.ForeignKey(
        SportMajmua,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name="Majmua",
    )
    level    = models.CharField(
        max_length=10,
        choices=Level.choices,
        verbose_name="Daraja",
    )
    title_uz = models.CharField(max_length=500, verbose_name="Tadbir nomi (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Tadbir nomi (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Tadbir nomi (En)")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'infra_sport_majmua_tadbir'
        ordering            = ['level', 'order']
        verbose_name        = "Tadbir"
        verbose_name_plural = "Tadbirlar"

    def __str__(self):
        return f"[{self.level}] {self.title_uz[:60]}"
