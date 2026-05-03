from django.db import models
from common.base_models import TimeStampedModel


class QabulNavbar(TimeStampedModel):
    """Qabul sahifasining navbar kategoriyalari."""
    slug     = models.SlugField(max_length=100, unique=True)
    title_uz = models.CharField(max_length=255, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Nomi (En)")
    page_url = models.CharField(max_length=500, blank=True, verbose_name="Sahifa URL", help_text="Masalan: /qabul/bakalavr")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_navbar'
        verbose_name = "Qabul navbar"
        verbose_name_plural = "Qabul navbar kategoriyalari"
        ordering     = ['order']

    def __str__(self):
        return self.title_uz


class QabulNavbarItem(TimeStampedModel):
    """Qabul navbar ichidagi submenu itemlari."""
    navbar   = models.ForeignKey(QabulNavbar, on_delete=models.CASCADE, related_name='items')
    slug     = models.SlugField(max_length=150)
    title_uz = models.CharField(max_length=255, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Nomi (En)")
    page_url = models.CharField(max_length=500, blank=True, verbose_name="Sahifa URL", help_text="Masalan: /qabul/bakalavr/ariza")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_navbar_item'
        verbose_name = "Navbar item"
        verbose_name_plural = "Navbar itemlar"
        ordering     = ['order']
        unique_together = [('navbar', 'slug')]

    def __str__(self):
        return f"{self.navbar.title_uz} → {self.title_uz}"
