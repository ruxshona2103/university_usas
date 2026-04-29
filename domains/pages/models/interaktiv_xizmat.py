from django.db import models
from common.base_models import TimeStampedModel


class InteraktivXizmat(TimeStampedModel):
    """
    Interaktiv xizmatlar — Elektron kutubxona, HEMIS, Dasturlar va hokazo.
    """
    icon_class  = models.CharField(max_length=100, blank=True, verbose_name="Icon (CSS class yoki SVG nomi)")
    title_uz    = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    title_ru    = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    title_en    = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")
    link        = models.URLField(blank=True, verbose_name="Havola (URL)")
    order       = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active   = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'pages_interaktiv_xizmat'
        ordering            = ['order']
        verbose_name        = "Interaktiv xizmat"
        verbose_name_plural = "Interaktiv xizmatlar"

    def __str__(self):
        return self.title_uz
