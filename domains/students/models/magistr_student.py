from django.db import models

from common.base_models import TimeStampedModel


class MagistrGroup(TimeStampedModel):
    """Magistratura yo'nalishi / guruhi."""

    LANG_CHOICES = [('uz', "O'zbek"), ('ru', 'Rus')]

    specialty_code    = models.CharField(max_length=20, verbose_name="Mutaxassislik kodi")
    specialty_name_uz = models.CharField(max_length=500, verbose_name="Mutaxassislik nomi (Uz)")
    specialty_name_ru = models.CharField(max_length=500, blank=True, verbose_name="Mutaxassislik nomi (Ru)")
    specialty_name_en = models.CharField(max_length=500, blank=True, verbose_name="Mutaxassislik nomi (En)")
    education_lang    = models.CharField(max_length=5, choices=LANG_CHOICES, default='uz', verbose_name="Ta'lim tili")
    year              = models.CharField(max_length=20, verbose_name="O'quv yili", help_text="Masalan: 2025-2026")
    order             = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active         = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'students_magistr_group'
        ordering            = ['year', 'order', 'specialty_code']
        verbose_name        = "Magistratura guruhi"
        verbose_name_plural = "Magistratura guruhlari"

    def __str__(self):
        return f"{self.specialty_code} — {self.specialty_name_uz} ({self.year})"


class MagistrStudent(TimeStampedModel):
    """Magistratura talabasi — dissertatsiya mavzusi va ilmiy rahbar."""

    group = models.ForeignKey(
        MagistrGroup,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name="Guruh",
    )

    student_name           = models.CharField(max_length=300, verbose_name="Talabaning F.I.Sh.")
    dissertation_topic_uz  = models.TextField(verbose_name="Dissertatsiya mavzusi (Uz)")
    dissertation_topic_ru  = models.TextField(blank=True, verbose_name="Dissertatsiya mavzusi (Ru)")
    dissertation_topic_en  = models.TextField(blank=True, verbose_name="Dissertatsiya mavzusi (En)")
    supervisor_name        = models.CharField(max_length=300, verbose_name="Ilmiy rahbar F.I.Sh.")
    supervisor_info_uz     = models.CharField(max_length=300, blank=True, verbose_name="Ilmiy daraja va unvon (Uz)", help_text="Masalan: p.f.d (DsC), dotsent")
    supervisor_info_ru     = models.CharField(max_length=300, blank=True, verbose_name="Ilmiy daraja va unvon (Ru)")
    supervisor_info_en     = models.CharField(max_length=300, blank=True, verbose_name="Ilmiy daraja va unvon (En)")
    order                  = models.PositiveIntegerField(default=0, verbose_name="Tartib (№)")

    class Meta:
        db_table            = 'students_magistr_student'
        ordering            = ['group', 'order']
        verbose_name        = "Magistratura talabasi"
        verbose_name_plural = "Magistratura talabalari"

    def __str__(self):
        return self.student_name
