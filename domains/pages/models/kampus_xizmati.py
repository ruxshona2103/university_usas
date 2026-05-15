from django.db import models
from common.base_models import TimeStampedModel


class KampusXizmati(TimeStampedModel):
    """
    Asosiy sahifa hero pastidagi 4-ta kampus afzalliklari kartochkalari.
    """
    icon_class = models.CharField(max_length=100, blank=True, verbose_name="Icon nomi (lucide)")
    title_uz   = models.CharField(max_length=200, verbose_name="Sarlavha (Uz)")
    title_ru   = models.CharField(max_length=200, blank=True, verbose_name="Sarlavha (Ru)")
    title_en   = models.CharField(max_length=200, blank=True, verbose_name="Sarlavha (En)")
    link       = models.CharField(max_length=300, blank=True, verbose_name="Havola (relative yoki URL)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active  = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'pages_kampus_xizmati'
        ordering            = ['order']
        verbose_name        = "Kampus xizmati"
        verbose_name_plural = "Kampus xizmatlari"

    def __str__(self):
        return self.title_uz
