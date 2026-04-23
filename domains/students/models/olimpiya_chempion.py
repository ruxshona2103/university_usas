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

    full_name  = models.CharField(max_length=300, blank=True, verbose_name="To'liq ismi")
    image      = models.FileField(upload_to=olimpiya_image_upload, blank=True, null=True, verbose_name="Rasm")
    yonalish   = models.CharField(max_length=300, blank=True, verbose_name="Yo'nalish (sport turi)")
    guruh      = models.CharField(max_length=200, blank=True, verbose_name="Guruh")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active  = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'students_olimpiya_chempion'
        ordering            = ['order', 'full_name']
        verbose_name        = "Olimpiya chempioni"
        verbose_name_plural = "Olimpiya chempionlari"

    def __str__(self):
        return self.full_name or f"Champion #{self.pk}"
