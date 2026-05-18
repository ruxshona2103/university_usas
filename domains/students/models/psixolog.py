from django.db import models

from common.base_models import TimeStampedModel


class PsixologXizmat(TimeStampedModel):
    """Psixolog maslahatlari sahifasidagi xizmat turlari (raqamlangan ro'yxat)."""
    title_uz = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        db_table            = 'students_psixolog_xizmat'
        ordering            = ['order']
        verbose_name        = "Psixolog xizmati"
        verbose_name_plural = "Psixolog xizmatlari"

    def __str__(self):
        return self.title_uz


class PsixologSection(TimeStampedModel):
    """Psixolog maslahatlari sahifasidagi mazmun bo'limlari (sarlavha + matn)."""
    title_uz   = models.CharField(max_length=200, verbose_name="Sarlavha (Uz)")
    title_ru   = models.CharField(max_length=200, blank=True, verbose_name="Sarlavha (Ru)")
    title_en   = models.CharField(max_length=200, blank=True, verbose_name="Sarlavha (En)")
    content_uz = models.TextField(verbose_name="Matn (Uz)")
    content_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    content_en = models.TextField(blank=True, verbose_name="Matn (En)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active  = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        db_table            = 'students_psixolog_section'
        ordering            = ['order']
        verbose_name        = "Psixolog bo'limi"
        verbose_name_plural = "Psixolog bo'limlari"

    def __str__(self):
        return self.title_uz
