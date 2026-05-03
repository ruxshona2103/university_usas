from django.db import models
from django.utils.text import slugify
from common.base_models import TimeStampedModel


class InternationalPost(TimeStampedModel):
    """
    Xalqaro bo'lim e'lonlari (IV-BLOK) va Bo'lim yangiliklari (VI-BLOK).
    Ikkalasi ham sarlavha + to'liq matn + sana + rasm tuzilmasiga ega.
    """
    class PostType(models.TextChoices):
        ANNOUNCEMENT      = 'announcement',      "E'lon"
        NEWS              = 'news',              'Yangilik'
        TRAINING          = 'training',          'Xorijda malaka oshirish'
        ACADEMIC_EXCHANGE = 'academic_exchange', 'Akademik almashinuv'

    post_type = models.CharField(
        max_length=20,
        choices=PostType.choices,
        default=PostType.NEWS,
        verbose_name="Tur",
    )

    title_uz   = models.CharField(max_length=300, verbose_name="Sarlavha (Uz)")
    title_ru   = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en   = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")

    content_uz = models.TextField(verbose_name="Matn (Uz)")
    content_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    content_en = models.TextField(blank=True, verbose_name="Matn (En)")

    slug  = models.SlugField(max_length=350, unique=True, blank=True, verbose_name="Slug")

    image = models.FileField(upload_to='international/posts/%Y/%m/', blank=True, verbose_name="Rasm")
    date  = models.DateField(verbose_name="Sana")

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'international_post'
        ordering            = ['-date', 'order']
        verbose_name        = "Xalqaro bo'lim xabari"
        verbose_name_plural = "Xalqaro bo'lim xabarlari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz, allow_unicode=True)
            slug = base
            n = 1
            while InternationalPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.get_post_type_display()}] {self.title_uz}'
