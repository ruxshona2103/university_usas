import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel
from .fakultet_kafedra import FakultetKafedra


def kafedra_rasm_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'kafedra/rasmlar/{uuid.uuid4().hex}{ext}'


class KafedraRasm(TimeStampedModel):
    kafedra   = models.ForeignKey(
        FakultetKafedra,
        on_delete=models.CASCADE,
        related_name='rasmlar',
        verbose_name="Fakultet / Kafedra",
    )
    image     = models.FileField(
        upload_to=kafedra_rasm_upload,
        verbose_name="Rasm",
    )
    caption_uz = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Uz)")
    caption_ru = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Ru)")
    caption_en = models.CharField(max_length=300, blank=True, verbose_name="Izoh (En)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active  = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'academic_kafedra_rasm'
        ordering            = ['order']
        verbose_name        = "Kafedra rasmi"
        verbose_name_plural = "Kafedra rasmlari"

    def __str__(self):
        return f"{self.kafedra.name_uz} — rasm #{self.order}"
