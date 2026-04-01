from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from common.base_models import MultiLangImageContent, LinkableContent
from common.models import ContentImage


class ContentBlock(MultiLangImageContent):
    """
    Universal kontent bloki — navbar sahifasiga bog'liq.
    Akademiya raqamlarda, Yashil akademiya, Ekofaol, Psixolog,
    Talabalar hayoti, Kontrakt narxlari va h.k. uchun.
    Admin da navbar_item tanlanadi — qaysi sahifaga tegishli.
    """
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
            models.Index(fields=['navbar_item', 'is_active', 'order']),
        ]

    def __str__(self):
        title = self.title_uz or f'Block #{self.pk}'
        page  = self.navbar_item.slug if self.navbar_item else 'no-page'
        return f'{page} — {title}'


class LinkBlock(LinkableContent):
    """
    Havola bloki — faqat title + link bo'lgan kontent.
    Me'yoriy hujjatlar, Ma'naviyat rukni, Mening Konstitutsiyam uchun.
    """
    class Meta:
        db_table         = 'pages_link_block'
        verbose_name     = 'Havola bloki'
        verbose_name_plural = 'Havola bloklari'
        ordering         = ['order', 'created_at']
        indexes          = [
            models.Index(fields=['navbar_item', 'is_active', 'order']),
        ]

    def __str__(self):
        page = self.navbar_item.slug if self.navbar_item else 'no-page'
        return f'{page} — {self.title_uz}'
