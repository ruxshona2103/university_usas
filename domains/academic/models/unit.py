from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class UnitType(models.TextChoices):
    COUNCIL = 'council', 'Universitet kengashi'
    SUPERVISORY = 'supervisory', 'Kuzatuv kengashi'
    RECTOR = 'rector', 'Rektor'
    PRORECTOR = 'prorector', 'Prorektor'
    FACULTY = 'faculty', 'Fakultet'
    DEPARTMENT = 'department', 'Kafedra'
    CENTER = 'center', 'Markaz'
    INSTITUTE = 'institute', 'Institut'
    PUBLIC_ORG = 'public_org', 'Jamoat tashkiloti'
    DIVISION = 'division', "Bo'lim"


class OrganizationUnit(TimeStampedModel):
    title_uz = models.CharField(max_length=255, verbose_name='Nomi (Uz)')
    title_ru = models.CharField(max_length=255, blank=True, verbose_name='Nomi (Ru)')
    title_en = models.CharField(max_length=255, blank=True, verbose_name='Nomi (En)')

    slug = models.SlugField(unique=True, blank=True, max_length=300)
    unit_type = models.CharField(max_length=20, choices=UnitType.choices, verbose_name='Bo‘lim turi')

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
        verbose_name='Yuqori bo‘lim',
    )

    content_uz = models.TextField(blank=True, verbose_name='To‘liq matn (Uz)')
    content_ru = models.TextField(blank=True, verbose_name='To‘liq matn (Ru)')
    content_en = models.TextField(blank=True, verbose_name='To‘liq matn (En)')

    has_own_page = models.BooleanField(default=False, verbose_name='Alohida sahifasi bormi?')
    is_featured = models.BooleanField(default=False, verbose_name='Asosiy ajratilgan blokmi?')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Tartib')
    is_active = models.BooleanField(default=True, verbose_name='Faolmi?')

    class Meta:
        db_table = 'academic_organization_unit'
        ordering = ['order', 'created_at']
        verbose_name = "Tashkiliy bo'linma"
        verbose_name_plural = "Tashkiliy bo'linmalar"
        indexes = [
            models.Index(fields=['unit_type', 'is_active']),
            models.Index(fields=['slug']),
            models.Index(fields=['parent', 'order']),
        ]

    def __str__(self):
        return self.title_uz

    def clean(self):
        super().clean()
        if self.parent_id and self.parent_id == self.id:
            raise ValidationError({'parent': 'Bo‘lim o‘ziga parent bo‘lolmaydi.'})

        ancestor = self.parent
        while ancestor is not None:
            if ancestor.id == self.id:
                raise ValidationError({'parent': 'Daraxtda aylana (cycle) hosil bo‘lishi mumkin emas.'})
            ancestor = ancestor.parent

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title_uz)
            candidate = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f'{base_slug}-{counter}'
                counter += 1
            self.slug = candidate

        self.full_clean()
        super().save(*args, **kwargs)
