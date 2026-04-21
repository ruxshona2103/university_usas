from django.db import models
from common.base_models import TimeStampedModel


class PartnerOrganization(TimeStampedModel):
    """
    Xalqaro hamkor tashkilotlar (I-BLOK).
    Xorijiy universitetlar + O'zbekistondagi sport federatsiyalari.
    """
    class PartnerType(models.TextChoices):
        FOREIGN  = 'foreign',  'Xorijiy hamkor'
        DOMESTIC = 'domestic', "O'zbekiston tashkiloti"

    partner_type = models.CharField(
        max_length=20,
        choices=PartnerType.choices,
        default=PartnerType.FOREIGN,
        verbose_name="Hamkor turi",
    )

    title_uz = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")

    country_uz = models.CharField(max_length=100, blank=True, verbose_name="Mamlakat (Uz)")
    country_ru = models.CharField(max_length=100, blank=True, verbose_name="Mamlakat (Ru)")
    country_en = models.CharField(max_length=100, blank=True, verbose_name="Mamlakat (En)")

    logo  = models.ImageField(upload_to='international/logos/%Y/', blank=True, verbose_name="Logo")
    image = models.ImageField(upload_to='international/partners/%Y/', blank=True, verbose_name="Rasm")

    website  = models.URLField(blank=True, verbose_name="Veb-sayt")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'international_partner_organization'
        ordering            = ['partner_type', 'order']
        verbose_name        = 'Hamkor tashkilot'
        verbose_name_plural = 'Hamkor tashkilotlar'

    def __str__(self):
        return self.title_uz
