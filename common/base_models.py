import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True,     verbose_name="Yangilangan vaqt")

    class Meta:
        abstract = True


class PublishableContent(TimeStampedModel):
    """Yangiliklar, blog, tadbirlar uchun asosiy klass."""
    image  = models.FileField(upload_to='content/%Y/%m/', blank=True, null=True, verbose_name="Asosiy rasm")
    images = GenericRelation('common.ContentImage', related_query_name='%(class)s')

    title_uz = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(blank=True, null=True, verbose_name="Batafsil (Uz)")
    description_ru = models.TextField(blank=True, null=True, verbose_name="Batafsil (Ru)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Batafsil (En)")

    keywords   = models.CharField(max_length=500, blank=True, verbose_name="SEO Kalit so'zlar")
    date       = models.DateTimeField(null=True, blank=True, verbose_name="Sana")
    slug       = models.SlugField(unique=True, blank=True, max_length=300)
    is_published = models.BooleanField(default=True, verbose_name="Saytga chiqarilsinmi?")
    views      = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    likes      = models.PositiveIntegerField(default=0, verbose_name="Like soni")
    comments   = models.PositiveIntegerField(default=0, verbose_name="Komment soni")

    class Meta:
        abstract = True
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_uz) or str(self.pk)[:8]
            slug = base_slug
            counter = 1
            # Proxy model bo'lsa, concrete modelni ishlatamiz — global unique slug
            concrete = self._meta.proxy_for_model or self.__class__
            qs = concrete.objects.filter(slug=slug)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            while qs.exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                qs = concrete.objects.filter(slug=slug)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
            self.slug = slug
        super().save(*args, **kwargs)

    def get_title(self, lang='uz'):
        return getattr(self, f'title_{lang}', self.title_uz) or self.title_uz


# Navbar sahifalariga bog'liq kontent uchun abstract bazalar
class NavbarLinkedContent(TimeStampedModel):
    navbar_items = models.ManyToManyField(
        'pages.NavbarSubItem',
        blank=True,
        related_name='%(class)s_items',
        verbose_name='Navbar sahifalari',
    )
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        abstract = True
        ordering = ['order', 'created_at']


class MultiLangImageContent(NavbarLinkedContent):
    title_uz = models.CharField(max_length=500, null=True, blank=True, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, null=True, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, null=True, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(null=True, blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(null=True, blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(null=True, blank=True, verbose_name="Tavsif (En)")

    link  = models.CharField(max_length=500, null=True, blank=True, verbose_name="Havola (URL)")
    views = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")

    class Meta:
        abstract = True


class LinkableContent(NavbarLinkedContent):
    title_uz = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")

    link          = models.CharField(max_length=500, blank=True, verbose_name="Havola (URL)")
    document_file = models.FileField(
        upload_to='documents/%Y/%m/',
        null=True, blank=True,
        verbose_name="Fayl (PDF)",
    )

    class Meta:
        abstract = True
