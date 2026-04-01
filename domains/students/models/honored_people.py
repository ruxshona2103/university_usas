from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class PersonCategory(TimeStampedModel):
    """
    Shaxs kategoriyasi — qaysi navbar sahifasiga tegishliligini bildiradi.
    Misol: Faxrlarimiz, Bitiruvchilar, Faxrli ustozlar
    """
    navbar_item = models.ForeignKey(
        'pages.NavbarSubItem',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='person_categories',
        verbose_name="Navbar sahifasi",
    )
    title_uz = models.CharField(max_length=100, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=100, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=100, blank=True, verbose_name="Nomi (En)")
    slug     = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table         = 'students_person_category'
        ordering         = ['order']
        verbose_name     = "Shaxs kategoriyasi"
        verbose_name_plural = "Shaxslar kategoriyalari"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz)
            slug, counter = base, 1
            while PersonCategory.objects.filter(slug=slug).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_uz


class Person(TimeStampedModel):
    """Faxrli shaxslar — kategoriya (navbar) va tag orqali boshqariladi."""
    category = models.ForeignKey(
        PersonCategory,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='persons',
        verbose_name="Kategoriya",
    )
    image = models.ImageField(upload_to='persons/%Y/%m/', verbose_name="Rasm")

    full_name_uz = models.CharField(max_length=255, verbose_name="To'liq ismi (Uz)")
    full_name_ru = models.CharField(max_length=255, blank=True, verbose_name="To'liq ismi (Ru)")
    full_name_en = models.CharField(max_length=255, blank=True, verbose_name="To'liq ismi (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table         = 'students_person'
        ordering         = ['order', '-id']
        verbose_name     = "Shaxs"
        verbose_name_plural = "Shaxslar"

    def __str__(self):
        return self.full_name_uz


class PersonContent(TimeStampedModel):
    """
    Person uchun dinamik kontent tablari (Tag asosida).
    Misol: tag='Biografiya' → content_uz='...'
    """
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='tabs',
        verbose_name="Shaxs",
    )
    tag = models.ForeignKey(
        'common.Tag',
        on_delete=models.CASCADE,
        related_name='person_contents',
        verbose_name="Tag (tab nomi)",
    )
    content_uz = models.TextField(blank=True, verbose_name="Kontent (Uz)")
    content_ru = models.TextField(blank=True, verbose_name="Kontent (Ru)")
    content_en = models.TextField(blank=True, verbose_name="Kontent (En)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table         = 'students_person_content'
        ordering         = ['order']
        unique_together  = [('person', 'tag')]
        verbose_name     = "Shaxs kontenti"
        verbose_name_plural = "Shaxslar kontenti"

    def __str__(self):
        return f"{self.person.full_name_uz} — {self.tag.name_uz}"
