import uuid

from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        abstract = True


class PublishableContent(TimeStampedModel):
    image = models.ImageField(upload_to='content/%Y/%m/', verbose_name="Asosiy rasm")

    title_uz = models.CharField(max_length=255, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Sarlavha (En)")

    text_uz = models.TextField(verbose_name="To'liq matn (Uz)")
    text_ru = models.TextField(blank=True, verbose_name="To'liq matn (Ru)")
    text_en = models.TextField(blank=True, verbose_name="To'liq matn (En)")

    description_uz = models.TextField(blank=True, verbose_name="Qisqa tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Qisqa tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Qisqa tavsif (En)")

    keywords = models.CharField(max_length=500, blank=True, verbose_name="SEO Kalit so'zlar")
    date = models.DateField(verbose_name="Sana")
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    is_published = models.BooleanField(default=True, verbose_name="Saytga chiqarilsinmi?")
    views = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")

    class Meta:
        abstract = True
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_uz)
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_title(self, lang='uz'):
        return getattr(self, f'title_{lang}', self.title_uz) or self.title_uz
