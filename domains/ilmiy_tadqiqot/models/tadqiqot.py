from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class IlmiyTadqiqotCategory(TimeStampedModel):
    """Ilmiy tadqiqotlar kategoriyasi."""

    title_uz = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")
    slug     = models.SlugField(max_length=320, unique=True, blank=True)
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'ilmiy_tadqiqot_category'
        ordering            = ['order', 'title_uz']
        verbose_name        = "Ilmiy tadqiqot kategoriyasi"
        verbose_name_plural = "Ilmiy tadqiqot kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz)
            slug = base
            n = 1
            while IlmiyTadqiqotCategory.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz


class IlmiyTadqiqot(TimeStampedModel):
    """Ilmiy tadqiqot maqolasi — fayl yuklash imkoni bilan."""

    category = models.ForeignKey(
        IlmiyTadqiqotCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tadqiqotlar',
        verbose_name="Kategoriya",
    )

    title_uz = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(blank=True, null=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, null=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Tavsif (En)")

    # Muallif
    author_uz = models.CharField(max_length=300, blank=True, verbose_name="Muallif (Uz)")
    author_ru = models.CharField(max_length=300, blank=True, verbose_name="Muallif (Ru)")
    author_en = models.CharField(max_length=300, blank=True, verbose_name="Muallif (En)")

    image        = models.FileField(upload_to='ilmiy_tadqiqot/images/%Y/%m/', blank=True, null=True, verbose_name="Asosiy rasm (Uz)")
    image_ru     = models.FileField(upload_to='ilmiy_tadqiqot/images/%Y/%m/', blank=True, null=True, verbose_name="Asosiy rasm (Ru)")
    image_en     = models.FileField(upload_to='ilmiy_tadqiqot/images/%Y/%m/', blank=True, null=True, verbose_name="Asosiy rasm (En)")
    slug         = models.SlugField(max_length=550, unique=True, blank=True, verbose_name="Slug")
    date         = models.DateTimeField(null=True, blank=True, verbose_name="Nashr sanasi")
    is_published = models.BooleanField(default=True, verbose_name="Chiqarilsinmi?")
    views        = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    likes        = models.PositiveIntegerField(default=0, verbose_name="Like soni")
    comments     = models.PositiveIntegerField(default=0, verbose_name="Komment soni")

    class Meta:
        db_table            = 'ilmiy_tadqiqot'
        ordering            = ['-date', '-created_at']
        verbose_name        = "Ilmiy tadqiqot"
        verbose_name_plural = "Ilmiy tadqiqotlar"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz, allow_unicode=True) or str(self.id)
            slug = base
            n = 1
            while IlmiyTadqiqot.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz


class IlmiyTadqiqotFile(TimeStampedModel):
    """Ilmiy tadqiqotga bog'liq fayllar (PDF, Word, va boshqalar)."""

    tadqiqot = models.ForeignKey(
        IlmiyTadqiqot,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name="Ilmiy tadqiqot",
    )
    title_uz = models.CharField(max_length=300, blank=True, verbose_name="Fayl nomi (Uz)")
    title_ru = models.CharField(max_length=300, blank=True, verbose_name="Fayl nomi (Ru)")
    title_en = models.CharField(max_length=300, blank=True, verbose_name="Fayl nomi (En)")
    file     = models.FileField(upload_to='ilmiy_tadqiqot/files/%Y/%m/', verbose_name="Fayl")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'ilmiy_tadqiqot_file'
        ordering = ['order']

    def __str__(self):
        return f'{self.title_uz or "Fayl"} — {self.tadqiqot}'
