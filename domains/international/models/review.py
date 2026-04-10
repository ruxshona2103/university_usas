from django.db import models

from common.base_models import TimeStampedModel


class ForeignProfessorReview(TimeStampedModel):
    """Xorijlik professorlar fikri."""
    full_name   = models.CharField(max_length=255, verbose_name="Ismi sharifi")
    position_uz = models.CharField(max_length=255, blank=True, verbose_name="Lavozimi (Uz)")
    position_ru = models.CharField(max_length=255, blank=True, verbose_name="Lavozimi (Ru)")
    position_en = models.CharField(max_length=255, blank=True, verbose_name="Lavozimi (En)")
    country     = models.CharField(max_length=100, blank=True, verbose_name="Mamlakat")
    photo       = models.ImageField(upload_to='foreign_professors/%Y/%m/', null=True, blank=True, verbose_name="Foto")
    review_uz   = models.TextField(verbose_name="Fikr (Uz)")
    review_ru   = models.TextField(blank=True, verbose_name="Fikr (Ru)")
    review_en   = models.TextField(blank=True, verbose_name="Fikr (En)")
    is_active   = models.BooleanField(default=True, verbose_name="Faolmi?")
    order       = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'international_foreign_professor_review'
        ordering            = ['order', '-created_at']
        verbose_name        = 'Xorijlik professor fikri'
        verbose_name_plural = 'Xorijlik professorlar fikrlari'

    def __str__(self):
        return f'{self.full_name} ({self.country})'
