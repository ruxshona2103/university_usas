from django.db import models
from django.utils.text import slugify
from common.base_models import TimeStampedModel


class XorijlikProfessor(TimeStampedModel):
    """VIII-BLOK: Xorijlik professor-o'qituvchilar profili."""

    full_name      = models.CharField(max_length=255, verbose_name="Ismi sharifi")
    photo          = models.FileField(upload_to='xorijlik_professorlar/%Y/%m/', null=True, blank=True, verbose_name="Rasm")
    country        = models.CharField(max_length=100, blank=True, verbose_name="Mamlakat")

    # Qachondan beri ishlamoqda
    from_year      = models.PositiveIntegerField(null=True, blank=True, verbose_name="Qachondan (yil)")

    # Oldingi ish tajribasi / bio (matn)
    bio_uz         = models.TextField(blank=True, verbose_name="Bio / Tavsif (Uz)")
    bio_ru         = models.TextField(blank=True, verbose_name="Bio / Tavsif (Ru)")
    bio_en         = models.TextField(blank=True, verbose_name="Bio / Tavsif (En)")

    # Ma'lumoti
    education_uz   = models.TextField(blank=True, verbose_name="Ma'lumoti (Uz)")
    education_ru   = models.TextField(blank=True, verbose_name="Ma'lumoti (Ru)")
    education_en   = models.TextField(blank=True, verbose_name="Ma'lumoti (En)")

    # Mutaxassislik
    specialty_uz   = models.CharField(max_length=300, blank=True, verbose_name="Ma'lumoti bo'yicha mutaxassisligi (Uz)")
    specialty_ru   = models.CharField(max_length=300, blank=True, verbose_name="Ma'lumoti bo'yicha mutaxassisligi (Ru)")
    specialty_en   = models.CharField(max_length=300, blank=True, verbose_name="Ma'lumoti bo'yicha mutaxassisligi (En)")

    # Ilmiy darajasi
    academic_degree_uz = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy darajasi (Uz)")
    academic_degree_ru = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy darajasi (Ru)")
    academic_degree_en = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy darajasi (En)")

    # Ilmiy unvoni
    academic_title_uz  = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy unvoni (Uz)")
    academic_title_ru  = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy unvoni (Ru)")
    academic_title_en  = models.CharField(max_length=200, blank=True, verbose_name="Ilmiy unvoni (En)")

    slug      = models.SlugField(max_length=350, unique=True, blank=True, verbose_name="Slug")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'international_xorijlik_professor'
        verbose_name        = "Xorijlik professor-o'qituvchi"
        verbose_name_plural = "Xorijlik professor-o'qituvchilar"
        ordering            = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.full_name, allow_unicode=True) or str(self.id)
            slug = base
            n = 1
            while XorijlikProfessor.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.country})"
