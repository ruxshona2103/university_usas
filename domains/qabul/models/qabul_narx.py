from django.db import models
from common.base_models import TimeStampedModel


class QabulNarx(TimeStampedModel):
    """Kontrakt narxlari jadvali."""
    EDU_TYPE = [
        ('bakalavr',     'Bakalavr'),
        ('magistratura', 'Magistratura'),
        ('xorijiy',      'Xorijiy talabalar'),
    ]
    EDU_FORM = [
        ('kunduzgi', 'Kunduzgi'),
        ('sirtqi',   'Sirtqi'),
        ('kechki',   'Kechki'),
    ]

    edu_type        = models.CharField(max_length=20, choices=EDU_TYPE, default='bakalavr', verbose_name="Ta'lim turi")
    edu_form        = models.CharField(max_length=20, choices=EDU_FORM, default='kunduzgi', verbose_name="Ta'lim shakli")
    specialty_code  = models.CharField(max_length=20, blank=True, verbose_name="Yo'nalish kodi")
    specialty_name_uz = models.CharField(max_length=300, verbose_name="Yo'nalish nomi (Uz)")
    specialty_name_ru = models.CharField(max_length=300, blank=True, verbose_name="Yo'nalish nomi (Ru)")
    specialty_name_en = models.CharField(max_length=300, blank=True, verbose_name="Yo'nalish nomi (En)")
    price           = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Narx (so'm)")
    year            = models.PositiveIntegerField(default=2025, verbose_name="Yil")
    order           = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active       = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_narx'
        verbose_name = "Kontrakt narxi"
        verbose_name_plural = "Kontrakt narxlari"
        ordering     = ['edu_type', 'order']

    def __str__(self):
        return f"{self.specialty_name_uz} — {self.price:,} so'm"
