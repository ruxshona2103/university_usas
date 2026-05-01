from django.db import models
from common.base_models import TimeStampedModel


class QabulBolim(TimeStampedModel):
    """
    Qabul bo'limining asosiy kategoriyalari.
    Masalan: Bakalavr, Magistratura, Xorijiy talabalar, Talabalar turar joyi
    """
    BOLIM_CHOICES = [
        ('bakalavr',          'Bakalavr'),
        ('magistratura',      'Magistratura'),
        ('xorijiy',           'Xorijiy talabalar'),
        ('turar_joy',         'Talabalar turar joyi'),
        ('komissiya',         'Qabul komissiyasi'),
        ('other',             'Boshqa'),
    ]

    slug         = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    bolim_type   = models.CharField(max_length=30, choices=BOLIM_CHOICES, default='other', verbose_name="Bo'lim turi")
    title_uz     = models.CharField(max_length=255, verbose_name="Sarlavha (Uz)")
    title_ru     = models.CharField(max_length=255, blank=True, verbose_name="Sarlavha (Ru)")
    title_en     = models.CharField(max_length=255, blank=True, verbose_name="Sarlavha (En)")
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active    = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_bolim'
        verbose_name = "Qabul bo'limi"
        verbose_name_plural = "Qabul bo'limlari"
        ordering     = ['order']

    def __str__(self):
        return self.title_uz


class QabulBolimItem(TimeStampedModel):
    """
    Bo'lim ichidagi ma'lumot bloklari (matn, fayl, rasm bilan).
    """
    ITEM_TYPE_CHOICES = [
        ('text',     'Matn'),
        ('file',     'Fayl (PDF)'),
        ('table',    'Jadval (HTML)'),
        ('link',     'Havola'),
    ]

    bolim      = models.ForeignKey(QabulBolim, on_delete=models.CASCADE, related_name='items', verbose_name="Bo'lim")
    item_type  = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='text', verbose_name="Tur")
    title_uz   = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Uz)")
    title_ru   = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en   = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    body_uz    = models.TextField(blank=True, verbose_name="Matn (Uz)")
    body_ru    = models.TextField(blank=True, verbose_name="Matn (Ru)")
    body_en    = models.TextField(blank=True, verbose_name="Matn (En)")
    file       = models.FileField(upload_to='qabul/files/%Y/', null=True, blank=True, verbose_name="Fayl")
    link       = models.URLField(blank=True, verbose_name="Havola (URL)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active  = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_bolim_item'
        verbose_name = "Bo'lim ma'lumoti"
        verbose_name_plural = "Bo'lim ma'lumotlari"
        ordering     = ['order']

    def __str__(self):
        return f"{self.bolim} — {self.title_uz or self.item_type}"
