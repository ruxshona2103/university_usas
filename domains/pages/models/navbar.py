from django.db import models
from django.utils.text import slugify
from common.base_models import TimeStampedModel


class NavbarCategory(TimeStampedModel):
    """
    Navbar yuqori darajasi — AKADEMIYA, TALABALARGA, AXBOROT XIZMATI ...
    """
    name_uz = models.CharField(max_length=100, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Nomi (En)")

    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="Slug (URL)")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Ko'rsatilsinmi?")
    direct_url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="To'g'ridan URL (ixtiyoriy)",
        help_text="Children bo'lmasa ishlatiladi. Masalan: /news yoki https://hemis.uz. Bo'sh qolsa slug'dan avtomatik yasaladi."
    )

    class Meta:
        verbose_name = "Navbar bo'limi"
        verbose_name_plural = "Navbar bo'limlari"
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name_uz)
            slug = base_slug
            counter = 1
            while NavbarCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class NavbarSubItem(TimeStampedModel):
    """
    Navbar quyi darajasi — Akademiya tarixi, Rahbariyat, Yangiliklar ...
    Har bir sub-item o'ziga xos sahifaga ega bo'ladi (static matn yoki redirect URL).
    """

    class PageType(models.TextChoices):
        STATIC   = 'static',   'Statik sahifa (matn)'
        REDIRECT = 'redirect', 'Yo\'naltirish (URL)'

    category = models.ForeignKey(
        NavbarCategory,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Bo'lim"
    )

    name_uz = models.CharField(max_length=100, verbose_name="Nomi (Uz)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Nomi (Ru)")
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Nomi (En)")

    slug = models.SlugField(max_length=150, unique=True, blank=True, verbose_name="Slug (URL)")

    page_type = models.CharField(
        max_length=10,
        choices=PageType.choices,
        default=PageType.STATIC,
        verbose_name="Sahifa turi"
    )

    # Statik sahifa uchun — matn to'g'ridan-to'g'ri shu yerda saqlanadi
    content_uz = models.TextField(blank=True, verbose_name="Sahifa matni (Uz)")
    content_ru = models.TextField(blank=True, verbose_name="Sahifa matni (Ru)")
    content_en = models.TextField(blank=True, verbose_name="Sahifa matni (En)")

    # Redirect uchun — tashqi yoki ichki URL
    redirect_url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Yo'naltirish manzili (URL)",
        help_text="Masalan: /api/news/ yoki https://hemis.uz"
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    is_active = models.BooleanField(default=True, verbose_name="Ko'rsatilsinmi?")

    class Meta:
        verbose_name = "Navbar sahifasi"
        verbose_name_plural = "Navbar sahifalari"
        ordering = ['category__order', 'order']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name_uz)
            slug = base_slug
            counter = 1
            while NavbarSubItem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name_uz} → {self.name_uz}"
