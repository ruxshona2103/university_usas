from django.db import models
from common.base_models import TimeStampedModel


class QabulRaqami(TimeStampedModel):
    number    = models.CharField(max_length=50, unique=True, verbose_name="Qabul raqami")
    link      = models.URLField(max_length=500, blank=True, null=True, verbose_name="Havola")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'contact_qabul_raqami'
        verbose_name        = "Qabul raqami"
        verbose_name_plural = "Qabul raqamlari"

    def __str__(self):
        return self.number
