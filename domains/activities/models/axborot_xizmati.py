from django.db import models
from common.base_models import TimeStampedModel


class AxborotVazifa(TimeStampedModel):
    """Axborot xizmatining vazifalari ro'yxati."""

    title_uz = models.CharField(max_length=500, verbose_name="Vazifa (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Vazifa (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Vazifa (En)")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_axborot_vazifa'
        ordering            = ['order']
        verbose_name        = 'Axborot vazifasi'
        verbose_name_plural = 'Axborot vazifalari'

    def __str__(self):
        return self.title_uz[:80]


class AxborotXodim(TimeStampedModel):
    """Axborot xizmati xodimi."""

    full_name_uz = models.CharField(max_length=200, verbose_name="To'liq ismi (Uz)")
    full_name_ru = models.CharField(max_length=200, blank=True, verbose_name="To'liq ismi (Ru)")
    full_name_en = models.CharField(max_length=200, blank=True, verbose_name="To'liq ismi (En)")
    position_uz  = models.CharField(max_length=300, verbose_name="Lavozimi (Uz)")
    position_ru  = models.CharField(max_length=300, blank=True, verbose_name="Lavozimi (Ru)")
    position_en  = models.CharField(max_length=300, blank=True, verbose_name="Lavozimi (En)")
    phone        = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email        = models.EmailField(blank=True, verbose_name="E-mail")
    photo        = models.ImageField(upload_to='axborot/xodimlar/', blank=True, null=True, verbose_name="Surat")
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active    = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_axborot_xodim'
        ordering            = ['order']
        verbose_name        = 'Axborot xizmati xodimi'
        verbose_name_plural = 'Axborot xizmati xodimlari'

    def __str__(self):
        return self.full_name_uz
