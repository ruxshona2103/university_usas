from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from common.base_models import PublishableContent, TimeStampedModel

User = get_user_model()


# ── NewsCategory ───────────────────────────────────────────────────────────────
class NewsCategory(TimeStampedModel):
    """Yangiliklar uchun kategoriya (ota-bola ierarxiyasini qo'llab-quvvatlaydi)."""

    parent   = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name="Ota kategoriya",
    )
    title_uz = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    slug     = models.SlugField(max_length=220, unique=True, blank=True)
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'news_category'
        ordering            = ['order', 'title_uz']
        verbose_name        = "Yangilik kategoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz)
            slug = base
            n = 1
            while NewsCategory.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz


# Article — bitta jadval, uch turdagi kontent
class ArticleType(models.TextChoices):
    NEWS  = 'news',  'Yangilik'
    EVENT = 'event', 'Tadbir'
    BLOG  = 'blog',  'Blog'



class Article(PublishableContent):
    """
    Yangilik, Tadbir, Blog — bitta DB jadval (news_article).
    article_type orqali tur aniqlanadi — xuddi InformationContent kabi.
    """
    article_type = models.CharField(
        max_length=10,
        choices=ArticleType.choices,
        verbose_name='Tur',
        db_index=True,
    )

    # Kategoriyalar (bir nechta, ixtiyoriy)
    categories = models.ManyToManyField(
        NewsCategory,
        blank=True,
        related_name='articles',
        verbose_name="Kategoriyalar",
    )

    # Qisqa tavsif (kartada ko'rinadigan preview)
    tavsif_uz = models.TextField(blank=True, null=True, verbose_name="Tavsif (Uz)")
    tavsif_ru = models.TextField(blank=True, null=True, verbose_name="Tavsif (Ru)")
    tavsif_en = models.TextField(blank=True, null=True, verbose_name="Tavsif (En)")

    # News uchun
    source = models.CharField(max_length=200, blank=True, verbose_name="Manba")

    # Event uchun
    location_uz = models.CharField(max_length=300, blank=True, verbose_name="Manzil (Uz)")
    location_ru = models.CharField(max_length=300, blank=True, verbose_name="Manzil (Ru)")
    location_en = models.CharField(max_length=300, blank=True, verbose_name="Manzil (En)")
    start_time  = models.DateTimeField(null=True, blank=True, verbose_name="Boshlanish vaqti")

    # Blog uchun
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='articles',
        verbose_name="Muallif",
    )

    class Meta:
        db_table            = 'news_article'
        ordering            = ['-date']
        verbose_name        = 'Maqola'
        verbose_name_plural = 'Maqolalar'

    def __str__(self):
        return f'[{self.get_article_type_display()}] {self.title_uz}'

    def get_content_type(self) -> str:
        """Polymorphic method — har bir tur o'z nomini qaytaradi."""
        return self.article_type


#proxy model uchun avtomatik filter

class NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(article_type=ArticleType.NEWS)


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(article_type=ArticleType.EVENT)


class BlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(article_type=ArticleType.BLOG)


#Proxy modellar DB da yangi jadval yo

class News(Article):
    objects = NewsManager()

    class Meta:
        proxy               = True
        verbose_name        = "Yangilik"
        verbose_name_plural = "Yangiliklar (News)"

    def save(self, *args, **kwargs):
        self.article_type = ArticleType.NEWS
        super().save(*args, **kwargs)


class Event(Article):
    objects = EventManager()

    class Meta:
        proxy               = True
        verbose_name        = "Tadbir"
        verbose_name_plural = "Tadbirlar (Event)"

    def save(self, *args, **kwargs):
        self.article_type = ArticleType.EVENT
        super().save(*args, **kwargs)


class Blog(Article):
    objects = BlogManager()

    class Meta:
        proxy               = True
        verbose_name        = "Blog"
        verbose_name_plural = "Bloglar"

    def save(self, *args, **kwargs):
        self.article_type = ArticleType.BLOG
        super().save(*args, **kwargs)



# InformationContent — Axborot xizmati (o'zgarishsiz)

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
    """
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
    likes        = models.PositiveIntegerField(default=0, verbose_name="Like soni")
    comments     = models.PositiveIntegerField(default=0, verbose_name="Komment soni")

    class Meta:
        db_table            = 'news_information_content'
        ordering            = ['-date', '-created_at']
        verbose_name        = 'Axborot xizmati kontenti'
        verbose_name_plural = 'Axborot xizmati kontentlari'
        indexes             = [
            models.Index(fields=['content_type', 'is_published']),
        ]

    def __str__(self):
        return f'[{self.get_content_type_display()}] {self.title_uz or "—"}'


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
    image = models.FileField(upload_to='information/%Y/%m/', verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'news_information_image'
        ordering = ['order']

    def __str__(self):
        return f'Rasm #{self.order} — {self.content}'
