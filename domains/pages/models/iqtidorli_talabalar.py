import uuid
from django.db import models
from common.base_models import TimeStampedModel


class IqtidorliTalabalar(TimeStampedModel):
    """
    Iqtidorli talabalar bo'limi — singleton (faqat bitta yozuv).
    """
    SINGLETON_PK = uuid.UUID('70000000-0000-0000-0000-000000000001')

    # Sektor boshlig'i ma'lumotlari
    boshliq_lavozim_uz = models.CharField(max_length=200, default="Sektor boshlig'i", verbose_name="Lavozim (Uz)")
    boshliq_lavozim_ru = models.CharField(max_length=200, blank=True, verbose_name="Lavozim (Ru)")
    boshliq_lavozim_en = models.CharField(max_length=200, blank=True, verbose_name="Lavozim (En)")

    boshliq_fio_uz = models.CharField(max_length=200, verbose_name="F.I.O (Uz)")
    boshliq_fio_ru = models.CharField(max_length=200, blank=True, verbose_name="F.I.O (Ru)")
    boshliq_fio_en = models.CharField(max_length=200, blank=True, verbose_name="F.I.O (En)")

    qabul_kunlari_uz = models.CharField(max_length=200, blank=True, verbose_name="Qabul kunlari (Uz)")
    qabul_kunlari_ru = models.CharField(max_length=200, blank=True, verbose_name="Qabul kunlari (Ru)")
    qabul_kunlari_en = models.CharField(max_length=200, blank=True, verbose_name="Qabul kunlari (En)")

    telefon = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    image    = models.ImageField(upload_to='iqtidorli/', blank=True, null=True, verbose_name="Rasm (Uz)")
    image_ru = models.ImageField(upload_to='iqtidorli/', blank=True, null=True, verbose_name="Rasm (Ru)")
    image_en = models.ImageField(upload_to='iqtidorli/', blank=True, null=True, verbose_name="Rasm (En)")

    # Bo'lim sarlavhasi
    bolim_title_uz = models.CharField(max_length=200, default="Bo'lim vazifalari:", verbose_name="Bo'lim sarlavhasi (Uz)")
    bolim_title_ru = models.CharField(max_length=200, blank=True, verbose_name="Bo'lim sarlavhasi (Ru)")
    bolim_title_en = models.CharField(max_length=200, blank=True, verbose_name="Bo'lim sarlavhasi (En)")

    class Meta:
        db_table = 'pages_iqtidorli_talabalar'
        verbose_name = "Iqtidorli talabalar (bosh)"
        verbose_name_plural = "Iqtidorli talabalar (bosh)"

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return "Iqtidorli talabalar bo'limi"


class IqtidorliVazifa(TimeStampedModel):
    """
    Iqtidorli talabalar bo'limining vazifalari (ro'yxat).
    """
    parent = models.ForeignKey(IqtidorliTalabalar, on_delete=models.CASCADE, related_name='vazifalar')
    text_uz = models.TextField(verbose_name="Matn (Uz)")
    text_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    text_en = models.TextField(blank=True, verbose_name="Matn (En)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'pages_iqtidorli_vazifa'
        ordering = ['order']
        verbose_name = "Iqtidorli talabalar vazifasi"
        verbose_name_plural = "Iqtidorli talabalar vazifalari"

    def __str__(self):
        return self.text_uz[:60]
