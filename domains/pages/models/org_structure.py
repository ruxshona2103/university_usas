from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


class OrgSection(TimeStampedModel):
    """Frontend uchun tashkiliy tuzilmani bo'limlarga guruhlash."""
    title_uz       = models.CharField(max_length=200, verbose_name='Sarlavha (Uz)')
    title_ru       = models.CharField(max_length=200, blank=True, verbose_name='Sarlavha (Ru)')
    title_en       = models.CharField(max_length=200, blank=True, verbose_name='Sarlavha (En)')
    description_uz = models.CharField(max_length=500, blank=True, verbose_name='Tavsif (Uz)')
    description_ru = models.CharField(max_length=500, blank=True, verbose_name='Tavsif (Ru)')
    description_en = models.CharField(max_length=500, blank=True, verbose_name='Tavsif (En)')
    slug           = models.SlugField(max_length=120, unique=True)
    order          = models.PositiveIntegerField(default=0)
    is_active      = models.BooleanField(default=True)

    class Meta:
        db_table            = 'pages_org_section'
        ordering            = ['order']
        verbose_name        = 'Tuzilma bo\'limi'
        verbose_name_plural = 'Tuzilma bo\'limlari'

    def __str__(self):
        return self.title_uz


class OrgNode(TimeStampedModel):
    """
    Tashkiliy tuzilma daraxti — har bir tugun (bo'lim, sektor, institut...).
    parent=None bo'lsa — ildiz tugun (Kuzatuv kengashi).
    """

    class NodeType(models.TextChoices):
        GOVERNING  = 'governing',  'Boshqaruv organi'
        RECTOR     = 'rector',     'Rektor'
        PROREKTOR  = 'prorektor',  'Prorektor / Yordamchi'
        DEPARTMENT = 'department', "Bo'lim / Sektor"
        INSTITUTE  = 'institute',  'Institut / Markaz'
        KAFEDRA    = 'kafedra',    'Kafedra'
        OTHER      = 'other',      'Boshqa'

    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='Yuqori daraja',
    )
    node_type = models.CharField(
        max_length=20,
        choices=NodeType.choices,
        default=NodeType.DEPARTMENT,
        verbose_name='Tur',
    )
    title_uz = models.CharField(max_length=400, verbose_name='Nomi (Uz)')
    title_ru = models.CharField(max_length=400, blank=True, verbose_name='Nomi (Ru)')
    title_en = models.CharField(max_length=400, blank=True, verbose_name='Nomi (En)')
    slug    = models.SlugField(max_length=220, unique=True, blank=True, verbose_name='Slug')

    description_uz = models.CharField(max_length=500, blank=True, verbose_name='Tavsif (Uz)')
    description_ru = models.CharField(max_length=500, blank=True, verbose_name='Tavsif (Ru)')
    description_en = models.CharField(max_length=500, blank=True, verbose_name='Tavsif (En)')

    section       = models.ForeignKey(
        OrgSection,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='nodes',
        verbose_name="Bo'lim (sektsiya)",
    )
    section_order = models.PositiveIntegerField(default=0, verbose_name="Bo'limdagi tartib")

    image             = models.ImageField(upload_to='org_nodes/', blank=True, null=True, verbose_name='Rasm (Uz)')
    image_ru          = models.ImageField(upload_to='org_nodes/', blank=True, null=True, verbose_name='Rasm (Ru)')
    image_en          = models.ImageField(upload_to='org_nodes/', blank=True, null=True, verbose_name='Rasm (En)')

    is_starred        = models.BooleanField(default=False, verbose_name='* (bir yulduz)')
    is_double_starred = models.BooleanField(default=False, verbose_name='** (ikki yulduz)')
    is_highlighted    = models.BooleanField(default=False, verbose_name='Ajratilgan (qizil ramka)')
    is_active         = models.BooleanField(default=True,  verbose_name='Faolmi?')
    order             = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        db_table            = 'pages_org_node'
        ordering            = ['order', 'title_uz']
        verbose_name        = 'Tashkiliy tugun'
        verbose_name_plural = 'Tashkiliy tuzilma'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_uz) or str(self.id)[:8]
            slug = base
            n = 1
            while OrgNode.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        mark = ' *' if self.is_starred else (' **' if self.is_double_starred else '')
        return f'{self.title_uz}{mark}'
