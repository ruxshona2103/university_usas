from django.db import models

from common.base_models import TimeStampedModel


class StaffContent(TimeStampedModel):
    """
    Staff detail sahifasidagi dinamik tablar.
    Admin: har bir xodim uchun tag tanlash + matn yozish.
    Misol: "Biografiya", "Vazifa va funksiyalari", "Ilmiy faoliyat".
    """
    staff = models.ForeignKey(
        'academic.Staff',
        on_delete=models.CASCADE,
        related_name='tabs',
        verbose_name='Xodim',
    )
    tag = models.ForeignKey(
        'common.Tag',
        on_delete=models.CASCADE,
        related_name='staff_contents',
        verbose_name='Tab nomi (Tag)',
    )
    content_uz = models.TextField(blank=True, verbose_name='Matn (Uz)')
    content_ru = models.TextField(blank=True, verbose_name='Matn (Ru)')
    content_en = models.TextField(blank=True, verbose_name='Matn (En)')
    order      = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        db_table         = 'academic_staff_content'
        unique_together  = [('staff', 'tag')]
        ordering         = ['order']
        verbose_name     = 'Xodim tabi'
        verbose_name_plural = 'Xodim tablari'

    def __str__(self):
        return f'{self.staff.full_name} — {self.tag.name_uz}'
