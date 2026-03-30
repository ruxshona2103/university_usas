from django.db import models

from common.base_models import TimeStampedModel
from .unit import OrganizationUnit


class StaffRole(models.TextChoices):
    RECTOR = 'rector', 'Rektor'
    PRORECTOR = 'prorector', 'Prorektor'
    DEAN = 'dean', 'Dekan'
    DEPT_HEAD = 'dept_head', 'Kafedra mudiri'
    COUNCIL_MEMBER = 'council_member', "Kengash a'zosi"
    STAFF = 'staff', 'Xodim'


class Staff(TimeStampedModel):
    unit = models.ForeignKey(
        OrganizationUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff',
        verbose_name='Bo‘lim',
    )

    role = models.CharField(max_length=20, choices=StaffRole.choices, verbose_name='Lavozim turi')
    is_head = models.BooleanField(default=False, verbose_name='Rahbar xodimmi?')

    title_uz = models.CharField(max_length=255, verbose_name='Lavozim nomi (Uz)')
    title_ru = models.CharField(max_length=255, blank=True, verbose_name='Lavozim nomi (Ru)')
    title_en = models.CharField(max_length=255, blank=True, verbose_name='Lavozim nomi (En)')

    full_name = models.CharField(max_length=255, verbose_name='To‘liq ism')

    position_uz = models.CharField(max_length=255, blank=True, verbose_name='Ilmiy daraja / unvon (Uz)')
    position_ru = models.CharField(max_length=255, blank=True, verbose_name='Ilmiy daraja / unvon (Ru)')
    position_en = models.CharField(max_length=255, blank=True, verbose_name='Ilmiy daraja / unvon (En)')

    image = models.ImageField(upload_to='staff/%Y/%m/', null=True, blank=True, verbose_name='Rasm')
    address = models.CharField(max_length=300, blank=True, verbose_name='Manzil')

    reception = models.CharField(max_length=100, blank=True, verbose_name='Qabul vaqti')
    description_uz = models.TextField(null=True, blank=True, verbose_name='Batafsil (Uz)')
    description_ru = models.TextField(null=True, blank=True, verbose_name='Batafsil (Ru)')
    description_en = models.TextField(null=True, blank=True, verbose_name='Batafsil (En)')

    phone = models.CharField(max_length=25, blank=True, verbose_name='Telefon')
    fax = models.CharField(max_length=25, blank=True, verbose_name='Faks')
    email = models.EmailField(blank=True, verbose_name='Email')

    order = models.PositiveSmallIntegerField(default=0, verbose_name='Tartib')
    is_active = models.BooleanField(default=True, verbose_name='Faolmi?')

    class Meta:
        db_table = 'academic_staff'
        ordering = ['order', 'created_at']
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'
        indexes = [
            models.Index(fields=['unit', 'order']),
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['is_head']),
        ]

    def __str__(self):
        return f'{self.full_name} ({self.title_uz})'
