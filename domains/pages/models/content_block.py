from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from common.base_models import MultiLangImageContent, LinkableContent
from common.models import ContentImage


class BlockType(models.TextChoices):
    HERO       = 'hero',       'Hero banner'
    RICH_TEXT  = 'rich-text',  'Matn (HTML)'
    STATS      = 'stats',      'Statistikalar'
    GALLERY    = 'gallery',    'Galereya'
    QUOTE      = 'quote',      'Iqtibos'
    TABLE      = 'table',      'Jadval'
    TIMELINE   = 'timeline',   "Vaqt chizig'i"


class LinkBlockType(models.TextChoices):
    FILE_LIST     = 'file-list',     "Fayllar ro'yxati"
    USEFUL_LINKS  = 'useful-links',  'Foydali havolalar'


class ContentBlock(MultiLangImageContent):
    """
    Universal kontent bloki — navbar sahifasiga bog'liq.
    block_type orqali frontend qanday komponent ko'rsatishini biladi.
    json_data — stats/table/timeline uchun strukturali ma'lumot (JSON).
    """
    block_type = models.CharField(
        max_length=20,
        choices=BlockType.choices,
        default=BlockType.RICH_TEXT,
        verbose_name='Blok turi',
    )
    json_data = models.JSONField(
        null=True, blank=True,
        verbose_name='JSON ma\'lumot',
        help_text='Stats, table, timeline uchun strukturali JSON. Rich-text/hero/gallery da bo\'sh qoldiring.',
    )
    tags   = models.ManyToManyField(
        'common.Tag',
        blank=True,
        related_name='content_blocks',
        verbose_name='Taglar',
    )
    images = GenericRelation(ContentImage, verbose_name='Rasmlar')

    class Meta:
        db_table         = 'pages_content_block'
        verbose_name     = 'Kontent bloki'
        verbose_name_plural = 'Kontent bloklari'
        ordering         = ['order', 'created_at']
        indexes          = [
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return f'[{self.block_type}] {self.title_uz or self.pk}'


class LinkBlock(LinkableContent):
    """
    Havola bloki — faqat title + link bo'lgan kontent.
    block_type: file-list (PDF yuklab olish) yoki useful-links (oddiy havolalar).
    """
    block_type = models.CharField(
        max_length=20,
        choices=LinkBlockType.choices,
        default=LinkBlockType.USEFUL_LINKS,
        verbose_name='Blok turi',
    )

    class Meta:
        db_table         = 'pages_link_block'
        verbose_name     = 'Havola bloki'
        verbose_name_plural = 'Havola bloklari'
        ordering         = ['order', 'created_at']
        indexes          = [
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return f'[{self.block_type}] {self.title_uz}'
