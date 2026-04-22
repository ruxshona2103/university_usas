from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class IlmiyFaoliyatCategory(TimeStampedModel):
    """Ilmiy faoliyat uchun kategoriya — ixtiyoriy."""

    title_uz = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    slug     = models.SlugField(max_length=220, unique=True, blank=True)
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'activities_ilmiy_faoliyat_category'
        ordering            = ['order', 'title_uz']
        verbose_name        = "O'quv faoliyat kategoriyasi"
        verbose_name_plural = "O'quv faoliyat kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz)
            slug = base
            n = 1
            while IlmiyFaoliyatCategory.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz
