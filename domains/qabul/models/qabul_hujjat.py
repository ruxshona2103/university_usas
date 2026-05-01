from django.db import models
from common.base_models import TimeStampedModel


class QabulHujjat(TimeStampedModel):
    """Qabul uchun talab qilinadigan hujjatlar ro'yxati."""
    HUJJAT_TYPE = [
        ('bakalavr',     'Bakalavr'),
        ('magistratura', 'Magistratura'),
        ('xorijiy',      'Xorijiy talabalar'),
        ('umumiy',       'Umumiy'),
    ]

    hujjat_type  = models.CharField(max_length=20, choices=HUJJAT_TYPE, default='umumiy', verbose_name="Qabul turi")
    title_uz     = models.CharField(max_length=300, verbose_name="Hujjat nomi (Uz)")
    title_ru     = models.CharField(max_length=300, blank=True, verbose_name="Hujjat nomi (Ru)")
    title_en     = models.CharField(max_length=300, blank=True, verbose_name="Hujjat nomi (En)")
    description_uz = models.TextField(blank=True, verbose_name="Izoh (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Izoh (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Izoh (En)")
    file         = models.FileField(upload_to='qabul/hujjatlar/%Y/', null=True, blank=True, verbose_name="Fayl (namuna)")
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active    = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_hujjat'
        verbose_name = "Qabul hujjati"
        verbose_name_plural = "Qabul hujjatlari"
        ordering     = ['hujjat_type', 'order']

    def __str__(self):
        return f"[{self.get_hujjat_type_display()}] {self.title_uz}"
