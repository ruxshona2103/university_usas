from django.db import models
from common.base_models import TimeStampedModel


class QabulKomissiyaTarkibi(TimeStampedModel):
    """Qabul komissiyasi a'zolari."""
    full_name_uz = models.CharField(max_length=200, verbose_name="F.I.O (Uz)")
    full_name_ru = models.CharField(max_length=200, blank=True, verbose_name="F.I.O (Ru)")
    full_name_en = models.CharField(max_length=200, blank=True, verbose_name="F.I.O (En)")
    position_uz  = models.CharField(max_length=300, blank=True, verbose_name="Lavozim (Uz)")
    position_ru  = models.CharField(max_length=300, blank=True, verbose_name="Lavozim (Ru)")
    position_en  = models.CharField(max_length=300, blank=True, verbose_name="Lavozim (En)")
    phone        = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email        = models.EmailField(blank=True, verbose_name="Email")
    photo        = models.ImageField(upload_to='qabul/commission/%Y/', null=True, blank=True, verbose_name="Rasm")
    order        = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active    = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        db_table     = 'qabul_komissiya_tarkibi'
        verbose_name = "Komissiya a'zosi"
        verbose_name_plural = "Komissiya tarkibi"
        ordering     = ['order']

    def __str__(self):
        return self.full_name_uz
