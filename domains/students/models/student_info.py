from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class StudentInfoCategory(TimeStampedModel):
    """
    Talaba ma'lumotlari kategoriyasi.
    Misol: Bakalavriat, Magistratura, Bakalavriat ma'lumotnomasi...
    """
    title_uz = models.CharField(max_length=200, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Nomi (En)")
    slug     = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'students_info_category'
        ordering            = ['order']
        verbose_name        = "Bakalavriat kategoriyasi"
        verbose_name_plural = "Bakalavriat kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz)
            slug, n = base, 1
            while StudentInfoCategory.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz


class StudentInfo(TimeStampedModel):
    """
    Talabalarga mo'ljallangan ma'lumot sahifalari.
    Misol: Yo'riqnoma, Baholash tizimi, GPA, Stipendiyalar...
    """
    category = models.ForeignKey(
        StudentInfoCategory,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='items',
        verbose_name="Kategoriya",
    )

    title_uz   = models.CharField(max_length=255, verbose_name="Sarlavha (Uz)")
    title_ru   = models.CharField(max_length=255, blank=True, verbose_name="Sarlavha (Ru)")
    title_en   = models.CharField(max_length=255, blank=True, verbose_name="Sarlavha (En)")

    content_uz = models.TextField(verbose_name="Matn (Uz)")
    content_ru = models.TextField(blank=True, verbose_name="Matn (Ru)")
    content_en = models.TextField(blank=True, verbose_name="Matn (En)")

    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        db_table            = 'students_student_info'
        ordering            = ['order']
        verbose_name        = "Talaba ma'lumoti"
        verbose_name_plural = "Talaba ma'lumotlari"

    def __str__(self):
        return self.title_uz
