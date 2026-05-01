from django.db import models
from common.base_models import TimeStampedModel


class QabulYangilik(TimeStampedModel):
    """Qabul bo'limi yangiliklari."""
    title_uz     = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru     = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en     = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    body_uz      = models.TextField(blank=True, verbose_name="Matn (Uz)")
    body_ru      = models.TextField(blank=True, verbose_name="Matn (Ru)")
    body_en      = models.TextField(blank=True, verbose_name="Matn (En)")
    image        = models.ImageField(upload_to='qabul/yangiliklar/%Y/%m/', null=True, blank=True, verbose_name="Rasm")
    date         = models.DateField(null=True, blank=True, verbose_name="Sana")
    views        = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar")
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_published = models.BooleanField(default=True, verbose_name="Chiqarilsinmi?")

    class Meta:
        db_table     = 'qabul_yangilik'
        verbose_name = "Qabul yangiligi"
        verbose_name_plural = "Qabul yangiliklari"
        ordering     = ['-date', 'order']

    def __str__(self):
        return self.title_uz
