import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel


def olimpiya_image_upload(instance, filename):
    ext  = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f'olimpiya_chempionlar/{name}{ext}'


class OlimpiyaChempion(TimeStampedModel):
    """Olimpiya chempionlari."""

    full_name_uz = models.CharField(max_length=300, blank=True, verbose_name="To'liq ismi (UZ)")
    full_name_ru = models.CharField(max_length=300, blank=True, verbose_name="To'liq ismi (RU)")
    full_name_en = models.CharField(max_length=300, blank=True, verbose_name="To'liq ismi (EN)")
    image        = models.FileField(upload_to=olimpiya_image_upload, blank=True, null=True, verbose_name="Rasm")
    yonalish_uz  = models.CharField(max_length=300, blank=True, verbose_name="Sport turi (UZ)")
    yonalish_ru  = models.CharField(max_length=300, blank=True, verbose_name="Sport turi (RU)")
    yonalish_en  = models.CharField(max_length=300, blank=True, verbose_name="Sport turi (EN)")
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active    = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'students_olimpiya_chempion'
        ordering            = ['order', 'full_name_uz']
        verbose_name        = "Olimpiya chempioni"
        verbose_name_plural = "Olimpiya chempionlari"

    def __str__(self):
        return self.full_name_uz or f"Champion #{self.pk}"
