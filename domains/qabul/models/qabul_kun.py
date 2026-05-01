from django.db import models
from common.base_models import TimeStampedModel


class QabulKuni(TimeStampedModel):
    """Qabul kunlari jadvali."""
    QABUL_TYPE = [
        ('bakalavr',     'Bakalavr'),
        ('magistratura', 'Magistratura'),
        ('xorijiy',      'Xorijiy talabalar'),
    ]

    qabul_type   = models.CharField(max_length=20, choices=QABUL_TYPE, default='bakalavr', verbose_name="Qabul turi")
    title_uz     = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Uz)")
    title_ru     = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en     = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    start_date   = models.DateField(null=True, blank=True, verbose_name="Boshlanish sanasi")
    end_date     = models.DateField(null=True, blank=True, verbose_name="Tugash sanasi")
    description_uz = models.TextField(blank=True, verbose_name="Izoh (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Izoh (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Izoh (En)")
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active    = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_kun'
        verbose_name = "Qabul kuni"
        verbose_name_plural = "Qabul kunlari"
        ordering     = ['order', 'start_date']

    def __str__(self):
        return f"{self.get_qabul_type_display()} — {self.title_uz}"
