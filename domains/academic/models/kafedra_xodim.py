from django.db import models

from common.base_models import TimeStampedModel
from .fakultet_kafedra import FakultetKafedra


def xodim_photo_upload(instance, filename):
    # eski migration uchun saqlab qolindi
    return f'kafedra/xodimlar/{filename}'


class KafedraXodim(TimeStampedModel):
    kafedra = models.ForeignKey(
        FakultetKafedra,
        on_delete=models.CASCADE,
        related_name='xodimlar',
        verbose_name="Fakultet / Kafedra",
    )
    person = models.ForeignKey(
        'students.Person',
        on_delete=models.CASCADE,
        related_name='kafedra_links',
        verbose_name="Shaxs",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'academic_kafedra_xodim'
        ordering            = ['order']
        unique_together     = [('kafedra', 'person')]
        verbose_name        = "Kafedra xodimi"
        verbose_name_plural = "Kafedra xodimlari"

    def __str__(self):
        return f"{self.kafedra.name_uz} — {self.person.full_name_uz}"
