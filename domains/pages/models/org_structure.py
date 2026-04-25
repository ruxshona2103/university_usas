from django.db import models
from django.utils.text import slugify

from common.base_models import TimeStampedModel


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
    name_uz = models.CharField(max_length=400, verbose_name='Nomi (Uz)')
    name_ru = models.CharField(max_length=400, blank=True, verbose_name='Nomi (Ru)')
    name_en = models.CharField(max_length=400, blank=True, verbose_name='Nomi (En)')
    slug    = models.SlugField(max_length=220, unique=True, blank=True, verbose_name='Slug')

    is_starred        = models.BooleanField(default=False, verbose_name='* (bir yulduz)')
    is_double_starred = models.BooleanField(default=False, verbose_name='** (ikki yulduz)')
    is_highlighted    = models.BooleanField(default=False, verbose_name='Ajratilgan (qizil ramka)')
    is_active         = models.BooleanField(default=True,  verbose_name='Faolmi?')
    order             = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        db_table            = 'pages_org_node'
        ordering            = ['order', 'name_uz']
        verbose_name        = 'Tashkiliy tugun'
        verbose_name_plural = 'Tashkiliy tuzilma'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_uz) or str(self.id)[:8]
            slug = base
            n = 1
            while OrgNode.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        mark = ' *' if self.is_starred else (' **' if self.is_double_starred else '')
        return f'{self.name_uz}{mark}'
