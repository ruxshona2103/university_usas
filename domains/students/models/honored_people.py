from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class PersonCategory(TimeStampedModel):
    """
    Shaxs kategoriyasi — admin o'zi qo'shadi.
    Misol: Rektorat, Faxrlarimiz, Bitiruvchilar, Ilg'or olimlar, UZDSA yulduzlari
    """
    parent   = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name="Ota kategoriya",
    )
    title_uz = models.CharField(max_length=100, verbose_name="Nomi (Uz)")
    title_ru = models.CharField(max_length=100, blank=True, verbose_name="Nomi (Ru)")
    title_en = models.CharField(max_length=100, blank=True, verbose_name="Nomi (En)")
    slug     = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'students_person_category'
        ordering            = ['order']
        verbose_name        = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

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
    """
    Umumiy shaxs modeli.
    Kategoriya orqali ajratiladi: Rektorat, Faxrlarimiz, Bitiruvchilar...

    Rektorat kabi xodimlar uchun title, position, kontakt fieldlari to'ldiriladi.
    Faxrlarimiz, Bitiruvchilar kabi shaxslar uchun bu fieldlar bo'sh qoladi.
    """
    category = models.ForeignKey(
        PersonCategory,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='persons',
        verbose_name="Kategoriya",
    )
    image = models.FileField(upload_to='persons/%Y/%m/', blank=True, null=True, verbose_name="Asosiy rasm")

    full_name_uz = models.CharField(max_length=255, verbose_name="To'liq ismi (Uz)")
    full_name_ru = models.CharField(max_length=255, blank=True, verbose_name="To'liq ismi (Ru)")
    full_name_en = models.CharField(max_length=255, blank=True, verbose_name="To'liq ismi (En)")

    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    # ── Xodimlar uchun ixtiyoriy (Rektorat, Dekanlar...) ──────────────────────
    title_uz    = models.CharField(max_length=255, null=True, blank=True, verbose_name="Lavozim (Uz)")
    title_ru    = models.CharField(max_length=255, null=True, blank=True, verbose_name="Lavozim (Ru)")
    title_en    = models.CharField(max_length=255, null=True, blank=True, verbose_name="Lavozim (En)")

    position_uz = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ilmiy unvon (Uz)")
    position_ru = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ilmiy unvon (Ru)")
    position_en = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ilmiy unvon (En)")

    phone     = models.CharField(max_length=100, null=True, blank=True, verbose_name="Telefon")
    fax       = models.CharField(max_length=100, null=True, blank=True, verbose_name="Faks")
    email     = models.EmailField(null=True, blank=True, verbose_name="Email")
    address   = models.CharField(max_length=300, null=True, blank=True, verbose_name="Manzil")
    reception = models.CharField(max_length=100, null=True, blank=True, verbose_name="Qabul vaqti")
    is_head   = models.BooleanField(default=False, verbose_name="Bo'lim boshlig'i")
    # ──────────────────────────────────────────────────────────────────────────

    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'students_person'
        ordering            = ['order', '-id']
        verbose_name        = "Shaxs"
        verbose_name_plural = "Shaxslar"

    def __str__(self):
        return self.full_name_uz


class PersonImage(TimeStampedModel):
    """Person uchun qo'shimcha rasmlar (ixtiyoriy)."""
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Shaxs",
    )
    image = models.FileField(upload_to='persons/gallery/%Y/%m/', verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'students_person_image'
        ordering            = ['order']
        verbose_name        = "Shaxs rasmi"
        verbose_name_plural = "Shaxs rasmlari"

    def __str__(self):
        return f'Rasm #{self.order} — {self.person}'


class PersonContent(TimeStampedModel):
    """Person uchun dinamik kontent tablari (Tag asosida)."""
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='tabs',
        verbose_name="Shaxs",
    )
    tags = models.ManyToManyField(
        'common.Tag',
        blank=True,
        related_name='person_contents',
        verbose_name="Taglar",
    )
    content_uz = models.TextField(blank=True, verbose_name="Kontent (Uz)")
    content_ru = models.TextField(blank=True, verbose_name="Kontent (Ru)")
    content_en = models.TextField(blank=True, verbose_name="Kontent (En)")
    order      = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'students_person_content'
        ordering            = ['order']
        verbose_name        = "Shaxs kontenti"
        verbose_name_plural = "Shaxslar kontenti"

    def __str__(self):
        first_tag = self.tags.first()
        tag_str = first_tag.name_uz if first_tag else '—'
        return f"{self.person.full_name_uz} — {tag_str}"
