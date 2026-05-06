import uuid

from django.db import models

from common.base_models import TimeStampedModel


class IlmiyBolim(TimeStampedModel):
    SINGLETON_PK = uuid.UUID("50000000-0000-0000-0000-000000000001")

    description_uz = models.TextField(verbose_name="Bo'lim haqida (Uz)", blank=True)
    description_ru = models.TextField(verbose_name="Bo'lim haqida (Ru)", blank=True)
    description_en = models.TextField(verbose_name="Bo'lim haqida (En)", blank=True)

    class Meta:
        db_table = "pages_ilmiy_bolim"
        verbose_name = "Ilmiy bo'lim"
        verbose_name_plural = "Ilmiy bo'lim"

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return "Ilmiy bo'lim"


class IlmiyBolimYonalish(TimeStampedModel):
    bolim = models.ForeignKey(
        IlmiyBolim,
        on_delete=models.CASCADE,
        related_name="yonalishlar",
    )
    text_uz = models.TextField(verbose_name="Yo'nalish (Uz)")
    text_ru = models.TextField(verbose_name="Yo'nalish (Ru)", blank=True)
    text_en = models.TextField(verbose_name="Yo'nalish (En)", blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = "pages_ilmiy_bolim_yonalish"
        verbose_name = "Ilmiy bo'lim yo'nalishi"
        verbose_name_plural = "Ilmiy bo'lim yo'nalishlari"
        ordering = ["order"]

    def __str__(self):
        return self.text_uz[:80]
