from django.db import models
from common.base_models import TimeStampedModel


class AcademyDetailPage(TimeStampedModel):
    """
    Akademiya raqamlarda — batafsil sahifa (yagona yozuv).
    Yuqori statistikalar (Fakultetlar, Kafedralar...) AcademyStat dan keladi.
    Bu model qo'shimcha bo'limlarni saqlaydi.
    """

    # ── Axborot-resurs markazi ────────────────────────────────────────────────
    resource_center_uz = models.TextField(blank=True, null=True, verbose_name="Axborot-resurs markazi (Uz)")
    resource_center_ru = models.TextField(blank=True, null=True, verbose_name="Axborot-resurs markazi (Ru)")
    resource_center_en = models.TextField(blank=True, null=True, verbose_name="Axborot-resurs markazi (En)")

    # ── Ta'lim va tarkib ko'rsatkichlari ──────────────────────────────────────
    edu_direction_count = models.CharField(max_length=50, blank=True, default='', verbose_name="Ta'lim yo'nalishlari")
    sport_type_count    = models.CharField(max_length=50, blank=True, default='', verbose_name="Sport turlari")
    masters_count       = models.CharField(max_length=50, blank=True, default='', verbose_name="Magistratura mutaxassisliklari")
    auditorium_count    = models.CharField(max_length=50, blank=True, default='', verbose_name="O'quv auditoriyalari")

    # ── Batafsil ma'lumotlar ──────────────────────────────────────────────────
    detail_uz = models.TextField(blank=True, null=True, verbose_name="Batafsil ma'lumotlar (Uz)")
    detail_ru = models.TextField(blank=True, null=True, verbose_name="Batafsil ma'lumotlar (Ru)")
    detail_en = models.TextField(blank=True, null=True, verbose_name="Batafsil ma'lumotlar (En)")

    class Meta:
        db_table            = 'academic_detail_page'
        verbose_name        = "Akademiya raqamlarda — batafsil"
        verbose_name_plural = "Akademiya raqamlarda — batafsil"

    def __str__(self):
        return "Akademiya batafsil sahifasi"
