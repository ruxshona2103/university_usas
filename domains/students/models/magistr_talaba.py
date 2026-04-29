from django.db import models
from common.base_models import TimeStampedModel


class MagistrTalaba(TimeStampedModel):
    """
    Magistratura ta'lim bosqichi talabasi.
    Person modelga bog'langan + erkin matn maydonlari.
    """
    person = models.ForeignKey(
        'students.Person',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='magistr_talaba_entries',
        verbose_name="Shaxs (Person)",
    )

    full_name   = models.CharField(max_length=300, blank=True, verbose_name="F.I.Sh. (override)")
    specialty_code = models.CharField(max_length=50, blank=True, verbose_name="Mutaxassislik kodi")
    specialty_name_uz = models.CharField(max_length=500, blank=True, verbose_name="Mutaxassislik nomi (Uz)")
    specialty_name_ru = models.CharField(max_length=500, blank=True, verbose_name="Mutaxassislik nomi (Ru)")
    specialty_name_en = models.CharField(max_length=500, blank=True, verbose_name="Mutaxassislik nomi (En)")

    dissertation_topic_uz = models.TextField(blank=True, verbose_name="Dissertatsiya mavzusi (Uz)")
    dissertation_topic_ru = models.TextField(blank=True, verbose_name="Dissertatsiya mavzusi (Ru)")
    dissertation_topic_en = models.TextField(blank=True, verbose_name="Dissertatsiya mavzusi (En)")

    supervisor_name   = models.CharField(max_length=300, blank=True, verbose_name="Ilmiy rahbar")
    supervisor_info_uz = models.CharField(max_length=300, blank=True, verbose_name="Ilmiy daraja/unvon (Uz)")
    supervisor_info_ru = models.CharField(max_length=300, blank=True, verbose_name="Ilmiy daraja/unvon (Ru)")
    supervisor_info_en = models.CharField(max_length=300, blank=True, verbose_name="Ilmiy daraja/unvon (En)")

    education_form_uz = models.CharField(max_length=100, blank=True, verbose_name="Ta'lim shakli (Uz)", help_text="Kunduzgi / Sirtqi / Masofaviy")
    education_form_ru = models.CharField(max_length=100, blank=True, verbose_name="Ta'lim shakli (Ru)")
    education_form_en = models.CharField(max_length=100, blank=True, verbose_name="Ta'lim shakli (En)")

    year    = models.CharField(max_length=20, blank=True, verbose_name="O'quv yili", help_text="2024-2025")
    order   = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'students_magistr_talaba'
        ordering            = ['year', 'order', 'full_name']
        verbose_name        = "Magistratura talabasi (yangi)"
        verbose_name_plural = "Magistratura talabalari (yangi)"

    def __str__(self):
        name = self.full_name or (self.person.full_name_uz if self.person_id else '—')
        return f"{name} ({self.specialty_code})"
