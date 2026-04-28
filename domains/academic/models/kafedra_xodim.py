import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel
from .fakultet_kafedra import FakultetKafedra


def xodim_photo_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'kafedra/xodimlar/{uuid.uuid4().hex}{ext}'


class KafedraXodim(TimeStampedModel):
    kafedra     = models.ForeignKey(
        FakultetKafedra,
        on_delete=models.CASCADE,
        related_name='xodimlar',
        verbose_name="Fakultet / Kafedra",
    )
    full_name   = models.CharField(max_length=300, verbose_name="To'liq ismi")
    position_uz = models.CharField(max_length=300, verbose_name="Lavozimi (Uz)")
    position_ru = models.CharField(max_length=300, blank=True, verbose_name="Lavozimi (Ru)")
    position_en = models.CharField(max_length=300, blank=True, verbose_name="Lavozimi (En)")
    email       = models.CharField(max_length=200, blank=True, verbose_name="E-mail")
    photo       = models.FileField(
        upload_to=xodim_photo_upload,
        blank=True, null=True,
        verbose_name="Surat",
    )
    order       = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active   = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'academic_kafedra_xodim'
        ordering            = ['order', 'full_name']
        verbose_name        = "Kafedra xodimi"
        verbose_name_plural = "Kafedra xodimlari"

    def __str__(self):
        return self.full_name
