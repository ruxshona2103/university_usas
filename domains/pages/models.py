import uuid

from django.db import models
from django.core.validators import RegexValidator
from common.base_models import TimeStampedModel


# ─────────────────────────────────────────────────────────────────────────────
# EMAIL VALIDATOR — standart EmailField ustiga qo'shimcha regex nazorat
# ─────────────────────────────────────────────────────────────────────────────
email_regex_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$',
    message="To'g'ri email manzil kiriting. Namuna: info@ozdsa.uz"
)


# ─────────────────────────────────────────────────────────────────────────────
# ALOQA MA'LUMOTLARI  (Singleton — faqat bitta yozuv)
# ─────────────────────────────────────────────────────────────────────────────
class ContactConfig(TimeStampedModel):
    # UUID bo'lsa ham singleton uchun doimiy kalit ishlatamiz
    SINGLETON_PK = uuid.UUID('10000000-0000-0000-0000-000000000001')

    email = models.EmailField(
        verbose_name="Rasmiy Pochta",
        validators=[email_regex_validator]
    )
    phone = models.CharField(max_length=20, verbose_name="Telefon raqam")
    address_uz = models.CharField(max_length=300, verbose_name="Manzil (Uz)")
    address_ru = models.CharField(max_length=300, blank=True, verbose_name="Manzil (Ru)")
    address_en = models.CharField(max_length=300, blank=True, verbose_name="Manzil (En)")

    class Meta:
        verbose_name = "Aloqa sozlamasi"
        verbose_name_plural = "Aloqa sozlamalari"

    def save(self, *args, **kwargs):
        # Har doim bir xil
         UUID ishlatiladi — singleton kafolati
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return "Sayt aloqa ma'lumotlari"


# ─────────────────────────────────────────────────────────────────────────────
# PREZIDENT IQTIBOSI
# ─────────────────────────────────────────────────────────────────────────────
class PresidentQuote(TimeStampedModel):
    quote_uz = models.TextField(verbose_name="Iqtibos (Uz)")
    quote_ru = models.TextField(blank=True, verbose_name="Iqtibos (Ru)")
    quote_en = models.TextField(blank=True, verbose_name="Iqtibos (En)")

    author = models.CharField(max_length=150, default="Sh. Mirziyoyev", verbose_name="Muallif")
    is_active = models.BooleanField(default=True, verbose_name="Saytda ko'rinsinmi?")

    class Meta:
        verbose_name = "Prezident iqtibosi"
        verbose_name_plural = "Prezident iqtiboslari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author}: {self.quote_uz[:40]}..."


# ─────────────────────────────────────────────────────────────────────────────
# IJTIMOIY TARMOQLAR
# ─────────────────────────────────────────────────────────────────────────────
class SocialPlatformConfigs(models.TextChoices):
    TELEGRAM  = 'telegram',  'Telegram'
    INSTAGRAM = 'instagram', 'Instagram'
    FACEBOOK  = 'facebook',  'Facebook'
    YOUTUBE   = 'youtube',   'YouTube'
    TWITTER   = 'twitter',   'Twitter'


class SocialLink(TimeStampedModel):
    platform = models.CharField(
        max_length=50,
        choices=SocialPlatformConfigs.choices,
        unique=True,
        verbose_name="Ijtimoiy tarmoq turi"
    )
    url = models.URLField(verbose_name="Manzil (URL)")
    is_active = models.BooleanField(default=True, verbose_name="Saytda ko'rinsinmi?")

    class Meta:
        verbose_name = "Ijtimoiy tarmoq"
        verbose_name_plural = "Ijtimoiy tarmoqlar"

    def __str__(self):
        return self.get_platform_display()
