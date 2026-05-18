"""
Ilmiy kontentlar:
- IlmiyKontentSahifa  — har bir kategoriya uchun sahifa boshlanish matni (intro)
- IlmiyJurnal         — ilmiy jurnallar ro'yxati
- IlmiyKengashSeminar — ilmiy kengash va seminar (jadval)
- IlmiyLoyiha         — ilmiy loyihalar (jadval)
- IlmiyMaktab         — ilmiy maktablar (jadval)
- IlmiyAnjuman        — ilmiy anjuman va konferensiyalar
"""
import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel


def ilmiy_kontent_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f"ilmiy_kontent/{name}{ext}"


class IlmiyKategoriya(models.TextChoices):
    JURNALLAR = 'jurnallar', "Ilmiy jurnallar"
    KENGASH = 'kengash', "Ilmiy kengash va seminar"
    LOYIHALAR = 'loyihalar', "Ilmiy loyihalar"
    MAKTABLAR = 'maktablar', "Ilmiy maktablar"


class IlmiyKontentSahifa(TimeStampedModel):
    """Har bir ilmiy kontent sahifasi uchun sarlavha + intro matn."""

    kategoriya = models.CharField(
        max_length=20,
        choices=IlmiyKategoriya.choices,
        unique=True,
        verbose_name="Kategoriya",
    )

    title_uz = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")

    intro_uz = models.TextField(blank=True, verbose_name="Intro matn (Uz)")
    intro_ru = models.TextField(blank=True, verbose_name="Intro matn (Ru)")
    intro_en = models.TextField(blank=True, verbose_name="Intro matn (En)")

    class Meta:
        db_table = "activities_ilmiy_kontent_sahifa"
        verbose_name = "Ilmiy kontent sahifasi"
        verbose_name_plural = "Ilmiy kontent sahifalari"

    def __str__(self):
        return f"[{self.get_kategoriya_display()}] {self.title_uz}"


class IlmiyJurnal(TimeStampedModel):
    """Ilmiy jurnallar ro'yxati."""

    name_uz = models.CharField(max_length=500, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=500, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=500, blank=True, verbose_name="Nomi (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    image = models.ImageField(
        upload_to=ilmiy_kontent_image_upload, blank=True, null=True, verbose_name="Rasm (Uz)"
    )
    image_ru = models.ImageField(
        upload_to=ilmiy_kontent_image_upload, blank=True, null=True, verbose_name="Rasm (Ru)"
    )
    image_en = models.ImageField(
        upload_to=ilmiy_kontent_image_upload, blank=True, null=True, verbose_name="Rasm (En)"
    )
    link = models.URLField(blank=True, verbose_name="Jurnal sayti (URL)")

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table = "activities_ilmiy_jurnal"
        ordering = ["order", "-created_at"]
        verbose_name = "Ilmiy jurnal"
        verbose_name_plural = "Ilmiy jurnallar"

    def __str__(self):
        return self.name_uz[:80]


class IlmiyKengashSeminar(TimeStampedModel):
    """Ilmiy kengash yoki seminar — bitta jadval qatori."""

    TIPI = (
        ('kengash', "Ilmiy kengash"),
        ('seminar', "Ilmiy seminar"),
    )
    tipi = models.CharField(max_length=10, choices=TIPI, default='kengash', verbose_name="Tipi")

    shifr = models.CharField(
        max_length=200,
        verbose_name="Shifr va nomi",
        help_text="Masalan: DSc.28/2025.27.12.Ped.01.01 (pedagogika fanlari bo'yicha)",
    )
    buyruq_sanasi = models.CharField(
        max_length=100, blank=True, verbose_name="Buyruq sanasi va raqami",
        help_text="Masalan: 27.12.2025 №1599",
    )
    ixtisoslik_shifri = models.CharField(max_length=200, blank=True, verbose_name="Ixtisoslik shifri")

    ixtisoslik_nomi_uz = models.TextField(blank=True, verbose_name="Ixtisoslik nomi (Uz)")
    ixtisoslik_nomi_ru = models.TextField(blank=True, verbose_name="Ixtisoslik nomi (Ru)")
    ixtisoslik_nomi_en = models.TextField(blank=True, verbose_name="Ixtisoslik nomi (En)")

    # Rais
    rais_uz = models.CharField(max_length=300, blank=True, verbose_name="Rais F.I.SH (Uz)")
    rais_ru = models.CharField(max_length=300, blank=True, verbose_name="Rais F.I.SH (Ru)")
    rais_en = models.CharField(max_length=300, blank=True, verbose_name="Rais F.I.SH (En)")

    rais_lavozim_uz = models.CharField(max_length=300, blank=True, verbose_name="Rais ilmiy darajasi (Uz)")
    rais_lavozim_ru = models.CharField(max_length=300, blank=True, verbose_name="Rais ilmiy darajasi (Ru)")
    rais_lavozim_en = models.CharField(max_length=300, blank=True, verbose_name="Rais ilmiy darajasi (En)")

    # Kotib
    kotib_uz = models.CharField(max_length=300, blank=True, verbose_name="Kotib F.I.SH (Uz)")
    kotib_ru = models.CharField(max_length=300, blank=True, verbose_name="Kotib F.I.SH (Ru)")
    kotib_en = models.CharField(max_length=300, blank=True, verbose_name="Kotib F.I.SH (En)")

    kotib_lavozim_uz = models.CharField(max_length=300, blank=True, verbose_name="Kotib ilmiy darajasi (Uz)")
    kotib_lavozim_ru = models.CharField(max_length=300, blank=True, verbose_name="Kotib ilmiy darajasi (Ru)")
    kotib_lavozim_en = models.CharField(max_length=300, blank=True, verbose_name="Kotib ilmiy darajasi (En)")

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table = "activities_ilmiy_kengash_seminar"
        ordering = ["tipi", "order", "-created_at"]
        verbose_name = "Ilmiy kengash/seminar"
        verbose_name_plural = "Ilmiy kengash va seminarlar"

    def __str__(self):
        return f"[{self.get_tipi_display()}] {self.shifr}"


class IlmiyLoyiha(TimeStampedModel):
    """Ilmiy loyihalar — jadval qatori."""

    raqami_uz = models.CharField(
        max_length=300,
        verbose_name="Loyiha raqami va muddati (Uz)",
        help_text="Masalan: Bajarilishi 2027-2028 - yillarga mo'ljallangan Amaliy loyiha",
    )
    raqami_ru = models.CharField(max_length=300, blank=True, verbose_name="Loyiha raqami va muddati (Ru)")
    raqami_en = models.CharField(max_length=300, blank=True, verbose_name="Loyiha raqami va muddati (En)")

    mavzusi_uz = models.TextField(verbose_name="Loyiha mavzusi (Uz)")
    mavzusi_ru = models.TextField(blank=True, verbose_name="Loyiha mavzusi (Ru)")
    mavzusi_en = models.TextField(blank=True, verbose_name="Loyiha mavzusi (En)")

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table = "activities_ilmiy_loyiha"
        ordering = ["order", "-created_at"]
        verbose_name = "Ilmiy loyiha"
        verbose_name_plural = "Ilmiy loyihalar"

    def __str__(self):
        return self.mavzusi_uz[:80]


class IlmiyMaktab(TimeStampedModel):
    """Ilmiy maktablar — jadval qatori."""

    nomi_uz = models.CharField(max_length=300, verbose_name="Maktab nomi (Uz)")
    nomi_ru = models.CharField(max_length=300, blank=True, verbose_name="Maktab nomi (Ru)")
    nomi_en = models.CharField(max_length=300, blank=True, verbose_name="Maktab nomi (En)")

    asoschi_uz = models.CharField(max_length=300, verbose_name="Asoschi (Uz)")
    asoschi_ru = models.CharField(max_length=300, blank=True, verbose_name="Asoschi (Ru)")
    asoschi_en = models.CharField(max_length=300, blank=True, verbose_name="Asoschi (En)")

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table = "activities_ilmiy_maktab"
        ordering = ["order", "-created_at"]
        verbose_name = "Ilmiy maktab"
        verbose_name_plural = "Ilmiy maktablar"

    def __str__(self):
        return self.nomi_uz[:80]


def anjuman_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    name = uuid.uuid4().hex
    return f"ilmiy_anjumanlar/{name}{ext}"


class AnjumanTuri(models.TextChoices):
    RESPUBLIKA    = 'republic',      "Respublika konferensiyasi"
    XALQARO       = 'international', "Xalqaro konferensiya"
    SEMINAR       = 'seminar',       "Ilmiy seminar"
    DAVRA         = 'roundtable',    "Davra suhbati"
    VEBINAR       = 'webinar',       "Vebinar"


class AnjumanStatus(models.TextChoices):
    UPCOMING = 'upcoming', "Kutilmoqda"
    ONGOING  = 'ongoing',  "Davom etmoqda"
    PAST     = 'past',     "O'tkazildi"


class IlmiyAnjuman(TimeStampedModel):
    """Ilmiy anjuman va konferensiyalar."""

    title_uz = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    date = models.DateField(verbose_name="Sana")

    location_uz = models.CharField(max_length=300, blank=True, verbose_name="Manzil (Uz)")
    location_ru = models.CharField(max_length=300, blank=True, verbose_name="Manzil (Ru)")
    location_en = models.CharField(max_length=300, blank=True, verbose_name="Manzil (En)")

    turi = models.CharField(
        max_length=20,
        choices=AnjumanTuri.choices,
        default=AnjumanTuri.RESPUBLIKA,
        verbose_name="Turi",
    )
    status = models.CharField(
        max_length=10,
        choices=AnjumanStatus.choices,
        default=AnjumanStatus.UPCOMING,
        verbose_name="Holati",
    )

    image = models.ImageField(
        upload_to=anjuman_image_upload, blank=True, null=True, verbose_name="Rasm"
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table = "activities_ilmiy_anjuman"
        ordering = ["-date", "order"]
        verbose_name = "Ilmiy anjuman"
        verbose_name_plural = "Ilmiy anjumanlar"

    def __str__(self):
        return self.title_uz[:100]
