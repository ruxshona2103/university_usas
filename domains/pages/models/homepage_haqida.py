import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel


def homepage_haqida_rasm_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'homepage_haqida/{uuid.uuid4().hex}{ext}'


class HomepageHaqida(TimeStampedModel):
    """Asosiy sahifa — 'Akademiya haqida' bloki (singleton)."""

    SINGLETON_PK = uuid.UUID('40000000-0000-0000-0000-000000000001')

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    feature_1_title_uz = models.CharField(max_length=300, blank=True, verbose_name="1-xususiyat sarlavhasi (Uz)")
    feature_1_title_ru = models.CharField(max_length=300, blank=True, verbose_name="1-xususiyat sarlavhasi (Ru)")
    feature_1_title_en = models.CharField(max_length=300, blank=True, verbose_name="1-xususiyat sarlavhasi (En)")
    feature_1_desc_uz  = models.TextField(blank=True, verbose_name="1-xususiyat tavsifi (Uz)")
    feature_1_desc_ru  = models.TextField(blank=True, verbose_name="1-xususiyat tavsifi (Ru)")
    feature_1_desc_en  = models.TextField(blank=True, verbose_name="1-xususiyat tavsifi (En)")

    feature_2_title_uz = models.CharField(max_length=300, blank=True, verbose_name="2-xususiyat sarlavhasi (Uz)")
    feature_2_title_ru = models.CharField(max_length=300, blank=True, verbose_name="2-xususiyat sarlavhasi (Ru)")
    feature_2_title_en = models.CharField(max_length=300, blank=True, verbose_name="2-xususiyat sarlavhasi (En)")
    feature_2_desc_uz  = models.TextField(blank=True, verbose_name="2-xususiyat tavsifi (Uz)")
    feature_2_desc_ru  = models.TextField(blank=True, verbose_name="2-xususiyat tavsifi (Ru)")
    feature_2_desc_en  = models.TextField(blank=True, verbose_name="2-xususiyat tavsifi (En)")

    class Meta:
        db_table            = 'pages_homepage_haqida'
        verbose_name        = "Asosiy sahifa — Haqida bloki"
        verbose_name_plural = "Asosiy sahifa — Haqida bloki"

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return "Asosiy sahifa — Haqida bloki"


class HomepageHaqidaRasm(TimeStampedModel):
    """Carousel rasmlari."""

    haqida   = models.ForeignKey(
        HomepageHaqida,
        on_delete=models.CASCADE,
        related_name='rasmlar',
        verbose_name="Haqida bloki",
    )
    image    = models.ImageField(upload_to=homepage_haqida_rasm_upload, verbose_name="Rasm")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'pages_homepage_haqida_rasm'
        ordering            = ['order']
        verbose_name        = "Carousel rasmi"
        verbose_name_plural = "Carousel rasmlari"

    def __str__(self):
        return f"Rasm #{self.order}"
