from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class TenderAnnouncement(TimeStampedModel):
    """Tenderlar va e'lonlar."""
    TYPE_TENDER  = 'tender'
    TYPE_TANLOV  = 'tanlov'
    TYPE_CHOICES = [
        (TYPE_TENDER, 'Tender'),
        (TYPE_TANLOV, "Tanlov (e'lon)"),
    ]

    announcement_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES,
        default=TYPE_TENDER, verbose_name="Turi",
    )

    title_uz = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")

    description_uz = models.TextField(null=True, blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(null=True, blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(null=True, blank=True, verbose_name="Tavsif (En)")

    date    = models.DateTimeField(verbose_name="Sana")
    address = models.CharField(max_length=300, blank=True, verbose_name="Manzil")
    email   = models.EmailField(blank=True, verbose_name="Email")
    phone   = models.CharField(max_length=25, blank=True, verbose_name="Telefon")

    slug         = models.SlugField(max_length=550, unique=True, blank=True, verbose_name="Slug")
    is_published = models.BooleanField(default=True, verbose_name="Chiqarilsinmi?")
    views        = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    likes        = models.PositiveIntegerField(default=0, verbose_name="Like soni")
    comments     = models.PositiveIntegerField(default=0, verbose_name="Komment soni")

    class Meta:
        db_table            = 'tenders_announcement'
        ordering            = ['-date']
        verbose_name        = "Tender / E'lon"
        verbose_name_plural = "Tenderlar va e'lonlar"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz, allow_unicode=True) or str(self.id)
            slug = base
            n = 1
            while TenderAnnouncement.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz


class TenderImage(TimeStampedModel):
    """TenderAnnouncement uchun ko'p rasm."""
    tender = models.ForeignKey(
        TenderAnnouncement,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Tender',
    )
    image = models.FileField(upload_to='tenders/%Y/%m/', verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'tenders_image'
        ordering = ['order']

    def __str__(self):
        return f'Rasm #{self.order} — {self.tender}'
