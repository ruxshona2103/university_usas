from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from common.base_models import TimeStampedModel


class Partner(TimeStampedModel):
    image  = models.FileField(upload_to='partners/', verbose_name="Logo")
    images = GenericRelation('common.ContentImage', related_query_name='partner')
    url = models.URLField(blank=True, verbose_name="Sayt manzili (URL)")
    title_uz = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Ko'rsatilsinmi?")

    class Meta:
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlarimiz"
        ordering = ['order']

    def __str__(self):
        return self.title_uz
