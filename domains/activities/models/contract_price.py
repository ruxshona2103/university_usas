from django.db import models

from common.base_models import TimeStampedModel


class ContractPrice(TimeStampedModel):
    """To'lov-kontrakt narxlari — bakalavr va magistratura yo'nalishlari bo'yicha."""

    class EducationType(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER   = 'master',   'Magistratura'

    class EducationForm(models.TextChoices):
        DAYTIME  = 'daytime',  'Kunduzgi'
        EVENING  = 'evening',  'Kechki'
        DISTANCE = 'distance', "Sirtqi"

    specialty_code = models.CharField(max_length=20, verbose_name="Mutaxassislik kodi")

    specialty_name_uz = models.CharField(max_length=300, verbose_name="Mutaxassislik nomi (Uz)")
    specialty_name_ru = models.CharField(max_length=300, blank=True, verbose_name="Mutaxassislik nomi (Ru)")
    specialty_name_en = models.CharField(max_length=300, blank=True, verbose_name="Mutaxassislik nomi (En)")

    education_type = models.CharField(
        max_length=20,
        choices=EducationType.choices,
        default=EducationType.BACHELOR,
        verbose_name="Ta'lim darajasi",
    )
    education_form = models.CharField(
        max_length=20,
        choices=EducationForm.choices,
        default=EducationForm.DAYTIME,
        verbose_name="Ta'lim shakli",
    )

    price     = models.PositiveIntegerField(verbose_name="To'lov miqdori (so'm)")
    order     = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table            = 'activities_contract_price'
        ordering            = ['education_type', 'education_form', 'order']
        verbose_name        = "Kontrakt narxi"
        verbose_name_plural = "To'lov-kontrakt narxlari"

    def __str__(self):
        return f"{self.specialty_code} — {self.specialty_name_uz}"
