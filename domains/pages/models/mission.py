import uuid

from django.db import models

from common.base_models import TimeStampedModel


class AkademiyaMissiya(TimeStampedModel):
    """Akademiya missiyasi sahifasi — yagona obyekt (singleton)."""

    SINGLETON_PK = uuid.UUID('40000000-0000-0000-0000-000000000001')

    description_uz = models.TextField(verbose_name="Missiya matni (Uz)", blank=True)
    description_ru = models.TextField(verbose_name="Missiya matni (Ru)", blank=True)
    description_en = models.TextField(verbose_name="Missiya matni (En)", blank=True)

    class Meta:
        db_table = 'pages_akademiya_missiya'
        verbose_name = "Akademiya missiyasi"
        verbose_name_plural = "Akademiya missiyasi"

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return "Akademiya missiyasi"


class AkademiyaMissiyaYonalish(TimeStampedModel):
    """Missiyaning asosiy yo'nalishlari — har biri bitta band."""

    missiya = models.ForeignKey(
        AkademiyaMissiya,
        on_delete=models.CASCADE,
        related_name='yonalishlar',
    )
    text_uz = models.TextField(verbose_name="Yo'nalish matni (Uz)")
    text_ru = models.TextField(verbose_name="Yo'nalish matni (Ru)", blank=True)
    text_en = models.TextField(verbose_name="Yo'nalish matni (En)", blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'pages_akademiya_missiya_yonalish'
        verbose_name = "Missiya yo'nalishi"
        verbose_name_plural = "Missiya yo'nalishlari"
        ordering = ['order']

    def __str__(self):
        return self.text_uz[:80]
