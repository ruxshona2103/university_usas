from django.db import models

from common.base_models import TimeStampedModel


class AxborotSection(TimeStampedModel):
    """Axborot xizmati vazifalar bo'limi (5-band, 6-band va boshqalar)."""

    number    = models.PositiveSmallIntegerField(unique=True, verbose_name="Band raqami")
    title_uz  = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru  = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en  = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'axborot_section'
        ordering            = ['order', 'number']
        verbose_name        = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return f"{self.number}-band: {self.title_uz[:60]}"


class AxborotVazifa(TimeStampedModel):
    """Axborot xizmati vazifasi — bo'limga bog'liq alohida band."""

    section   = models.ForeignKey(
        AxborotSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Bo'lim",
    )
    body_uz   = models.TextField(verbose_name="Matn (Uz)")
    body_ru   = models.TextField(blank=True, verbose_name="Matn (Ru)")
    body_en   = models.TextField(blank=True, verbose_name="Matn (En)")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'axborot_vazifa'
        ordering            = ['order']
        verbose_name        = "Vazifa"
        verbose_name_plural = "Vazifalar"

    def __str__(self):
        return f"[{self.section.number}-band] {self.body_uz[:80]}"
