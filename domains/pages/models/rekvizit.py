import uuid

from django.db import models

from common.base_models import TimeStampedModel


class Rekvizit(TimeStampedModel):
    """
    Tashkilot rekvizitlari — singleton model.
    To'liq nomi, qisqartilgan nomi, email, telefon, manzil.
    """
    SINGLETON_PK = uuid.UUID('20000000-0000-0000-0000-000000000001')

    # ── To'liq nomi ───────────────────────────────────────────────────────────
    org_name_uz = models.CharField(max_length=300, verbose_name="To'liq nomi (Uz)")
    org_name_ru = models.CharField(max_length=300, blank=True, verbose_name="To'liq nomi (Ru)")
    org_name_en = models.CharField(max_length=300, blank=True, verbose_name="To'liq nomi (En)")

    # ── Qisqartilgan nomi ─────────────────────────────────────────────────────
    org_short_name = models.CharField(max_length=50, verbose_name="Qisqartilgan nomi")

    # ── Email (ikki xil) ──────────────────────────────────────────────────────
    email_1 = models.EmailField(verbose_name="Email 1")
    email_2 = models.EmailField(blank=True, verbose_name="Email 2")

    # ── Telefon (ikki xil) ────────────────────────────────────────────────────
    phone_1 = models.CharField(max_length=30, verbose_name="Telefon 1")
    phone_2 = models.CharField(max_length=30, blank=True, verbose_name="Telefon 2")

    # ── Manzil ────────────────────────────────────────────────────────────────
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Pochta indeksi")
    address_uz  = models.CharField(max_length=500, verbose_name="Manzil (Uz)")
    address_ru  = models.CharField(max_length=500, blank=True, verbose_name="Manzil (Ru)")
    address_en  = models.CharField(max_length=500, blank=True, verbose_name="Manzil (En)")

    class Meta:
        db_table            = 'pages_rekvizit'
        verbose_name        = "Rekvizit"
        verbose_name_plural = "Rekvizitlar"

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return f"{self.org_short_name} rekvizitlari"
