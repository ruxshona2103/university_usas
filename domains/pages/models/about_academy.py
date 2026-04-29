import os
import uuid

from django.db import models

from common.base_models import TimeStampedModel


def about_academy_gallery_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'about_academy/gallery/{uuid.uuid4().hex}{ext}'


class AboutAcademy(TimeStampedModel):
    """Akademiya haqida sahifasi — yagona obyekt (singleton)."""

    SINGLETON_PK = uuid.UUID('30000000-0000-0000-0000-000000000001')

    logo  = models.ImageField(upload_to='about_academy/', blank=True, null=True, verbose_name="Logo")
    image = models.ImageField(upload_to='about_academy/', blank=True, null=True, verbose_name="Asosiy rasm")

    description_uz = models.TextField(verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    class Meta:
        db_table            = 'pages_about_academy'
        verbose_name        = "Akademiya haqida"
        verbose_name_plural = "Akademiya haqida"

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return "Akademiya haqida"


class AboutAcademySection(TimeStampedModel):
    """Bo'lim: maqsad, vazifalar, tizim, hamkorlik, va h.k."""

    about = models.ForeignKey(
        AboutAcademy,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="Akademiya haqida",
    )
    key = models.CharField(
        max_length=50,
        verbose_name="Kalit",
        help_text="API javobida ishlatiladi, masalan: goals, tasks, system, partners",
    )
    title_uz = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'pages_about_academy_section'
        ordering            = ['order']
        verbose_name        = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return f"[{self.key}] {self.title_uz}"


class AboutAcademySectionItem(TimeStampedModel):
    """Bo'lim ichidagi ro'yxat elementlari."""

    section = models.ForeignKey(
        AboutAcademySection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Bo'lim",
    )
    text_uz = models.TextField(verbose_name="Matn (Uz)")
    text_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    text_en = models.TextField(blank=True, verbose_name="Matn (En)")
    order   = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'pages_about_academy_section_item'
        ordering            = ['order']
        verbose_name        = "Element"
        verbose_name_plural = "Elementlar"

    def __str__(self):
        return self.text_uz[:80]


class AboutAcademyProgram(TimeStampedModel):
    """Bakalavriat va magistratura dasturlari."""

    PROGRAM_TYPE_CHOICES = [
        ('bachelor', 'Bakalavriat'),
        ('master',   'Magistratura'),
    ]

    about        = models.ForeignKey(
        AboutAcademy,
        on_delete=models.CASCADE,
        related_name='programs',
        verbose_name="Akademiya haqida",
    )
    program_type = models.CharField(
        max_length=10,
        choices=PROGRAM_TYPE_CHOICES,
        verbose_name="Dastur turi",
    )
    direction_uz = models.CharField(max_length=300, verbose_name="Yo'nalish (Uz)")
    direction_ru = models.CharField(max_length=300, blank=True, verbose_name="Yo'nalish (Ru)")
    direction_en = models.CharField(max_length=300, blank=True, verbose_name="Yo'nalish (En)")
    profession_uz = models.CharField(max_length=300, verbose_name="Mutaxassislik (Uz)")
    profession_ru = models.CharField(max_length=300, blank=True, verbose_name="Mutaxassislik (Ru)")
    profession_en = models.CharField(max_length=300, blank=True, verbose_name="Mutaxassislik (En)")
    order         = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'pages_about_academy_program'
        ordering            = ['program_type', 'order']
        verbose_name        = "Ta'lim dasturi"
        verbose_name_plural = "Ta'lim dasturlari"

    def __str__(self):
        return f"[{self.get_program_type_display()}] {self.direction_uz}"


class AboutAcademyImage(TimeStampedModel):
    """Akademiya haqida sahifasi uchun gallery rasmlari."""

    about     = models.ForeignKey(
        AboutAcademy,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Akademiya haqida",
    )
    image     = models.ImageField(upload_to=about_academy_gallery_upload, verbose_name="Rasm")
    caption_uz = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Uz)")
    caption_ru = models.CharField(max_length=300, blank=True, verbose_name="Izoh (Ru)")
    caption_en = models.CharField(max_length=300, blank=True, verbose_name="Izoh (En)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active  = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'pages_about_academy_image'
        ordering            = ['order']
        verbose_name        = "Gallery rasmi"
        verbose_name_plural = "Gallery rasmlari"

    def __str__(self):
        return f"Rasm #{self.order}"
