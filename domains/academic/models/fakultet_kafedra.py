from django.db import models
from django.utils.text import slugify
from common.base_models import TimeStampedModel


class FakultetKafedra(TimeStampedModel):
    FAKULTET = 'fakultet'
    KAFEDRA  = 'kafedra'
    TYPE_CHOICES = [
        (FAKULTET, 'Fakultet'),
        (KAFEDRA,  'Kafedra'),
    ]

    type     = models.CharField(max_length=20, choices=TYPE_CHOICES, default=KAFEDRA, verbose_name="Turi")
    slug     = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    name_uz  = models.CharField(max_length=300, verbose_name="Nomi (Uz)")
    name_ru  = models.CharField(max_length=300, blank=True, verbose_name="Nomi (Ru)")
    name_en  = models.CharField(max_length=300, blank=True, verbose_name="Nomi (En)")

    # Qisqa tavsif
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    # Sport turlari — har bir satr bitta sport tur
    sport_types_uz = models.TextField(blank=True, verbose_name="Sport turlari (Uz)", help_text="Har birini yangi satrga yozing")
    sport_types_ru = models.TextField(blank=True, verbose_name="Sport turlari (Ru)")
    sport_types_en = models.TextField(blank=True, verbose_name="Sport turlari (En)")

    # Bakalavriat fanlari — har bir satr bitta fan
    bachelor_subjects_uz = models.TextField(blank=True, verbose_name="Bakalavriat fanlari (Uz)", help_text="Har birini yangi satrga yozing")
    bachelor_subjects_ru = models.TextField(blank=True, verbose_name="Bakalavriat fanlari (Ru)")
    bachelor_subjects_en = models.TextField(blank=True, verbose_name="Bakalavriat fanlari (En)")

    # Magistratura fanlari — har bir satr bitta fan
    master_subjects_uz = models.TextField(blank=True, verbose_name="Magistratura fanlari (Uz)", help_text="Har birini yangi satrga yozing")
    master_subjects_ru = models.TextField(blank=True, verbose_name="Magistratura fanlari (Ru)")
    master_subjects_en = models.TextField(blank=True, verbose_name="Magistratura fanlari (En)")

    decree_info = models.CharField(max_length=300, blank=True, verbose_name="Asos hujjat (farmon/qaror)")
    phone       = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email       = models.CharField(max_length=200, blank=True, verbose_name="E-mail")

    link      = models.URLField(blank=True, verbose_name="Tashqi havola (URL)")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'academic_fakultet_kafedra'
        ordering            = ['order', 'name_uz']
        verbose_name        = "Fakultet / Kafedra"
        verbose_name_plural = "Fakultetlar va kafedralar"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz)
            slug, counter = base, 1
            while FakultetKafedra.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz


class KafedraPublication(TimeStampedModel):
    MONOGRAF = 'monograf'
    DARSLIK  = 'darslik'
    QOLLANMA = 'qollanma'
    TYPE_CHOICES = [
        (MONOGRAF, 'Monografiya'),
        (DARSLIK,  'Darslik'),
        (QOLLANMA, "O'quv qo'llanma"),
    ]

    kafedra  = models.ForeignKey(
        FakultetKafedra,
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name="Kafedra",
    )
    title_uz = models.CharField(max_length=500, verbose_name="Sarlavha (Uz)")
    title_ru = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (Ru)")
    title_en = models.CharField(max_length=500, blank=True, verbose_name="Sarlavha (En)")
    author   = models.CharField(max_length=300, blank=True, verbose_name="Muallif(lar)")
    pub_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=MONOGRAF, verbose_name="Turi")
    cover    = models.FileField(upload_to='kafedra/publications/', blank=True, null=True, verbose_name="Muqova rasmi")
    order    = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table            = 'academic_kafedra_publication'
        ordering            = ['order', 'title_uz']
        verbose_name        = "Kafedra nashri"
        verbose_name_plural = "Kafedra nashrlari"

    def __str__(self):
        return self.title_uz
