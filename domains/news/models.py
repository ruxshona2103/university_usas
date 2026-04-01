from django.contrib.auth import get_user_model
from django.db import models

from common.base_models import PublishableContent, TimeStampedModel

User = get_user_model()


# ──────────────────────────────────────────────────────────────────────────────
# Mavjud modellar (o'zgarishsiz)
# ──────────────────────────────────────────────────────────────────────────────

class News(PublishableContent):
    """So'nggi yangiliklar."""
    source = models.CharField(max_length=200, blank=True, verbose_name="Manba")

    class Meta:
        verbose_name        = "Yangilik"
        verbose_name_plural = "So'nggi yangiliklar"
        db_table            = "news_news"

    def __str__(self):
        return self.title_uz


class Event(PublishableContent):
    """Kutilayotgan tadbirlar."""
    location_uz = models.CharField(max_length=300, verbose_name="Manzil (Uz)")
    location_ru = models.CharField(max_length=300, blank=True, verbose_name="Manzil (Ru)")
    location_en = models.CharField(max_length=300, blank=True, verbose_name="Manzil (En)")
    start_time  = models.DateTimeField(null=True, blank=True, verbose_name="Boshlanish vaqti")

    class Meta:
        verbose_name        = "Tadbir"
        verbose_name_plural = "Kutilayotgan tadbirlar"
        db_table            = "news_event"

    def __str__(self):
        return self.title_uz


class Blog(PublishableContent):
    """Blog."""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blogs',
        verbose_name="Muallif",
    )

    class Meta:
        verbose_name        = "Blog"
        verbose_name_plural = "Bloglar"
        db_table            = "news_blog"

    def __str__(self):
        return self.title_uz


# ──────────────────────────────────────────────────────────────────────────────
# InformationContent — Axborot xizmati kontent
# ──────────────────────────────────────────────────────────────────────────────

class InformationContentType(models.TextChoices):
    RECTOR   = 'rector',   'Rektor tadbirlari va nutqlari'
    BRIEFING = 'briefing', 'Brifinglar'
    CONTEST  = 'contest',  'Tanlovlar'
    PRESS    = 'press',    'Matbuot xizmati'
    PHOTO    = 'photo',    'Fotogalereya'
    VIDEO    = 'video',    'Videogalereya'


class InformationContent(TimeStampedModel):
    """
    Axborot xizmati kontent — navbar sahifasiga bog'liq.
    content_type orqali tur aniqlanadi.
    Barcha maydonlar nullable — admin faqat keraklilarini to'ldiradi.
    """
    navbar_item = models.ForeignKey(
        'pages.NavbarSubItem',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='information_items',
        verbose_name='Navbar sahifasi',
    )
    content_type = models.CharField(
        max_length=20,
        choices=InformationContentType.choices,
        verbose_name='Tur',
    )
    title_uz = models.CharField(max_length=500, null=True, blank=True, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, null=True, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, null=True, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(null=True, blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(null=True, blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(null=True, blank=True, verbose_name="Tavsif (En)")

    date         = models.DateTimeField(null=True, blank=True, verbose_name="Sana")
    video_url    = models.URLField(null=True, blank=True, verbose_name="Video URL")
    external_url = models.URLField(null=True, blank=True, verbose_name="Tashqi havola")
    is_published = models.BooleanField(default=True, verbose_name="Chiqarilsinmi?")
    views        = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")

    class Meta:
        db_table            = 'news_information_content'
        ordering            = ['-date', '-created_at']
        verbose_name        = 'Axborot xizmati kontenti'
        verbose_name_plural = 'Axborot xizmati kontentlari'
        indexes             = [
            models.Index(fields=['content_type', 'is_published']),
            models.Index(fields=['navbar_item', 'content_type']),
        ]

    def __str__(self):
        return f'[{self.get_content_type_display()}] {self.title_uz or "—"}'


# ──────────────────────────────────────────────────────────────────────────────
# Proxy modellar — har bir tur uchun alohida admin menu item
# DB da yangi jadval yaratmaydi
# ──────────────────────────────────────────────────────────────────────────────

class RectorActivity(InformationContent):
    class Meta:
        proxy               = True
        verbose_name        = "Rektor tadbirlari va nutqlari"
        verbose_name_plural = "Rektor tadbirlari va nutqlari"


class Briefing(InformationContent):
    class Meta:
        proxy               = True
        verbose_name        = "Brifing"
        verbose_name_plural = "Brifinglar"


class Contest(InformationContent):
    class Meta:
        proxy               = True
        verbose_name        = "Tanlov"
        verbose_name_plural = "Tanlovlar"


class PressService(InformationContent):
    class Meta:
        proxy               = True
        verbose_name        = "Matbuot xizmati"
        verbose_name_plural = "Matbuot xizmati"


class PhotoGallery(InformationContent):
    class Meta:
        proxy               = True
        verbose_name        = "Fotogalereya"
        verbose_name_plural = "Fotogalereya"


class VideoGallery(InformationContent):
    class Meta:
        proxy               = True
        verbose_name        = "Videogalereya"
        verbose_name_plural = "Videogalereya"


class InformationImage(TimeStampedModel):
    """InformationContent uchun ko'p rasm."""
    content = models.ForeignKey(
        InformationContent,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Kontent',
    )
    image = models.ImageField(upload_to='information/%Y/%m/', verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'news_information_image'
        ordering = ['order']

    def __str__(self):
        return f'Rasm #{self.order} — {self.content}'
