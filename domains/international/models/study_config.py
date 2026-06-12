from django.db import models


VARIANT_CHOICES = [
    ('warning', 'Sariq (warning)'),
    ('info',    'Ko\'k (info)'),
    ('success', 'Yashil (success)'),
]


class StudyInUzbekistanConfig(models.Model):
    """Singleton — Study in Uzbekistan sahifasi konfiguratsiyasi."""

    # Kirish matni
    intro_uz = models.TextField(blank=True, verbose_name="Kirish matni (Uz)",
                                help_text="Sahifa bosh qismidagi matn. HTML qabul qiladi.")
    intro_ru = models.TextField(blank=True, verbose_name="Kirish matni (Ru)")
    intro_en = models.TextField(blank=True, verbose_name="Kirish matni (En)")

    # Banner rasm
    banner_image = models.FileField(
        upload_to='study_in_uzbekistan/',
        blank=True, null=True,
        verbose_name="Banner rasm",
    )
    banner_link = models.URLField(max_length=500, blank=True, verbose_name="Banner linki",
                                  help_text="Rasmni bosganda ochiladi")
    banner_caption_uz = models.CharField(max_length=300, blank=True, verbose_name="Rasm taglik (Uz)")
    banner_caption_ru = models.CharField(max_length=300, blank=True, verbose_name="Rasm taglik (Ru)")
    banner_caption_en = models.CharField(max_length=300, blank=True, verbose_name="Rasm taglik (En)")

    # E'lon qutisi
    announcement_show   = models.BooleanField(default=True, verbose_name="E'lonni ko'rsatish")
    announcement_variant = models.CharField(
        max_length=20, choices=VARIANT_CHOICES, default='info',
        verbose_name="E'lon rangi",
    )
    announcement_icon       = models.CharField(max_length=10, blank=True, default='🔔', verbose_name="E'lon ikoni (emoji)")
    announcement_title_uz   = models.CharField(max_length=300, blank=True, verbose_name="E'lon sarlavhasi (Uz)")
    announcement_title_ru   = models.CharField(max_length=300, blank=True, verbose_name="E'lon sarlavhasi (Ru)")
    announcement_title_en   = models.CharField(max_length=300, blank=True, verbose_name="E'lon sarlavhasi (En)")
    announcement_text_uz    = models.TextField(blank=True, verbose_name="E'lon matni (Uz)")
    announcement_text_ru    = models.TextField(blank=True, verbose_name="E'lon matni (Ru)")
    announcement_text_en    = models.TextField(blank=True, verbose_name="E'lon matni (En)")
    announcement_link       = models.URLField(max_length=500, blank=True, verbose_name="E'lon linki")
    announcement_link_text  = models.CharField(max_length=200, blank=True, verbose_name="Link matni")

    # Portal tugmasi
    portal_url        = models.URLField(max_length=500, blank=True,
                                        default='https://studyinuzbekistan.com',
                                        verbose_name="Portal URL (studyinuzbekistan.com)")
    portal_button_uz  = models.CharField(max_length=200, blank=True, default='Study in Uzbekistan',
                                         verbose_name="Tugma matni (Uz)")
    portal_button_ru  = models.CharField(max_length=200, blank=True, default='Study in Uzbekistan',
                                         verbose_name="Tugma matni (Ru)")
    portal_button_en  = models.CharField(max_length=200, blank=True, default='Study in Uzbekistan',
                                         verbose_name="Tugma matni (En)")

    class Meta:
        db_table            = 'study_in_uzbekistan_config'
        verbose_name        = "Study in Uzbekistan sahifasi"
        verbose_name_plural = "Study in Uzbekistan sahifasi"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Study in Uzbekistan sahifasi konfiguratsiyasi"
