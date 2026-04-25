import uuid

from django.db import models

from common.base_models import TimeStampedModel


class AboutSocial(TimeStampedModel):
    """Axborot xizmati sahifasi — yagona obyekt (singleton)."""

    SINGLETON_PK = uuid.UUID('20000000-0000-0000-0000-000000000001')

    title_uz = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")

    class Meta:
        db_table            = 'pages_about_social'
        verbose_name        = "Axborot xizmati haqida"
        verbose_name_plural = "Axborot xizmati haqida"

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj

    def __str__(self):
        return self.title_uz or "Axborot xizmati haqida"


class AboutSocialSection(TimeStampedModel):
    """Har bir bo'lim (section_5, section_6, ...)."""

    about_social = models.ForeignKey(
        AboutSocial,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="Axborot xizmati",
    )
    key = models.CharField(
        max_length=50,
        verbose_name="Kalit",
        help_text="API javobida ishlatiladi, masalan: section_5, section_6",
    )
    title_uz = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'pages_about_social_section'
        ordering            = ['order']
        verbose_name        = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return f"[{self.key}] {self.title_uz}"


class AboutSocialSectionItem(TimeStampedModel):
    """Bo'lim ichidagi ro'yxat elementlari."""

    section = models.ForeignKey(
        AboutSocialSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Bo'lim",
    )
    text_uz = models.TextField(verbose_name="Matn (Uz)")
    text_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    text_en = models.TextField(blank=True, verbose_name="Matn (En)")
    order   = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'pages_about_social_section_item'
        ordering            = ['order']
        verbose_name        = "Element"
        verbose_name_plural = "Elementlar"

    def __str__(self):
        return self.text_uz[:80]


class AboutSocialExtraTask(TimeStampedModel):
    """Qo'shimcha vazifalar ro'yxati (extra_tasks)."""

    about_social = models.ForeignKey(
        AboutSocial,
        on_delete=models.CASCADE,
        related_name='extra_tasks',
        verbose_name="Axborot xizmati",
    )
    text_uz = models.CharField(max_length=300, verbose_name="Matn (Uz)")
    text_ru = models.CharField(max_length=300, blank=True, verbose_name="Matn (Ru)")
    text_en = models.CharField(max_length=300, blank=True, verbose_name="Matn (En)")
    order   = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'pages_about_social_extra_task'
        ordering            = ['order']
        verbose_name        = "Qo'shimcha vazifa"
        verbose_name_plural = "Qo'shimcha vazifalar"

    def __str__(self):
        return self.text_uz
