from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from common.models import ContentImage
from domains.pages.models import (
    ContactConfig, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo,
    ContentBlock, LinkBlock,
    OrgNode, OrgSection, Rekvizit,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _abs_url(request, file_field):
    """ImageField / FileField → absolute URL yoki None."""
    if not file_field:
        return None
    try:
        url = file_field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


# ──────────────────────────────────────────────────────────────────────────────
# Site-wide
# ──────────────────────────────────────────────────────────────────────────────

class ContactConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactConfig
        fields = ['email', 'phone', 'address_uz', 'address_ru', 'address_en']


class RekvizitSerializer(serializers.ModelSerializer):
    org_name = serializers.SerializerMethodField()
    address  = serializers.SerializerMethodField()

    class Meta:
        model  = Rekvizit
        fields = [
            'org_name', 'org_short_name',
            'email_1', 'email_2',
            'phone_1', 'phone_2',
            'postal_code', 'address',
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_org_name(self, obj):
        return {
            'uz': obj.org_name_uz,
            'ru': obj.org_name_ru or obj.org_name_uz,
            'en': obj.org_name_en or obj.org_name_uz,
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_address(self, obj):
        return {
            'uz': obj.address_uz,
            'ru': obj.address_ru or obj.address_uz,
            'en': obj.address_en or obj.address_uz,
        }


class PresidentQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PresidentQuote
        fields = ['id', 'author', 'quote_uz', 'quote_ru', 'quote_en']


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='get_platform_display', read_only=True)

    class Meta:
        model  = SocialLink
        fields = ['id', 'platform', 'platform_name', 'url']


class PartnerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model  = Partner
        fields = ['id', 'image', 'url', 'title', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}


class HeroVideoSerializer(serializers.ModelSerializer):
    poster_image = serializers.SerializerMethodField()

    class Meta:
        model  = HeroVideo
        fields = ['id', 'title', 'video_url', 'poster_image', 'is_active', 'created_at']

    @extend_schema_field(OpenApiTypes.URI)
    def get_poster_image(self, obj):
        return _abs_url(self.context.get('request'), obj.poster_image)


# ──────────────────────────────────────────────────────────────────────────────
# Navbar tree
# ──────────────────────────────────────────────────────────────────────────────

class NavbarSubItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = NavbarSubItem
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'slug', 'page_type', 'redirect_url', 'order']


class NavbarCategorySerializer(serializers.ModelSerializer):
    items = NavbarSubItemSerializer(many=True, read_only=True)

    class Meta:
        model  = NavbarCategory
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'slug', 'order', 'items']


# ──────────────────────────────────────────────────────────────────────────────
# Page detail — /api/pages/{slug}/
# ──────────────────────────────────────────────────────────────────────────────

class _ContentImageSerializer(serializers.Serializer):
    """ContentBlock ichidagi rasmlar."""
    id    = serializers.UUIDField()
    image = serializers.SerializerMethodField()
    order = serializers.IntegerField()

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class _ContentBlockSerializer(serializers.ModelSerializer):
    """ContentBlock — page detail ichida."""
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images      = serializers.SerializerMethodField()
    tags        = serializers.SerializerMethodField()

    class Meta:
        model  = ContentBlock
        fields = ['id', 'title', 'description', 'link', 'images', 'tags', 'views', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}') or obj.description_uz

    def get_images(self, obj):
        imgs = obj.images.all().order_by('order')
        return _ContentImageSerializer(imgs, many=True, context=self.context).data

    def get_tags(self, obj):
        return [{'slug': t.slug, 'name': t.name_uz} for t in obj.tags.all()]


class _LinkBlockSerializer(serializers.ModelSerializer):
    """LinkBlock — page detail ichida."""
    title         = serializers.SerializerMethodField()
    document_file = serializers.SerializerMethodField()

    class Meta:
        model  = LinkBlock
        fields = ['id', 'title', 'link', 'document_file', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_document_file(self, obj):
        return _abs_url(self.context.get('request'), obj.document_file)


class NavbarPageSerializer(serializers.ModelSerializer):
    """
    /api/pages/{slug}/ — universal page serializer.
    Barcha kontent turlari bitta `blocks` array da qaytariladi,
    frontend tipiga qarab komponent ko'rsatadi.

    Block turlari:
      hero, rich-text, stats, gallery, quote, table, timeline  ← ContentBlock
      file-list, useful-links                                   ← LinkBlock
    """
    name    = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    blocks  = serializers.SerializerMethodField()

    class Meta:
        model  = NavbarSubItem
        fields = ['id', 'slug', 'name', 'page_type', 'redirect_url', 'content', 'blocks']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}') or obj.name_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}') or obj.content_uz or ''

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_blocks(self, obj):
        blocks = []

        # ── ContentBlock (hero/rich-text/stats/gallery/quote/table/timeline) ──
        cb_qs = (
            obj.contentblock_items
            .filter(is_active=True)
            .prefetch_related('images', 'tags')
            .order_by('order', 'created_at')
        )
        for cb in cb_qs:
            blocks.append({
                'type':  cb.block_type,
                'order': cb.order,
                'data':  self._content_block_data(cb),
            })

        # ── LinkBlock (file-list / useful-links) ──
        lb_qs = obj.linkblock_items.filter(is_active=True).order_by('order', 'created_at')
        for lb in lb_qs:
            blocks.append({
                'type':  lb.block_type,
                'order': lb.order,
                'data':  self._link_block_data(lb),
            })

        # order bo'yicha tartiblash
        blocks.sort(key=lambda b: b['order'])
        return blocks

    # ── Helpers ──

    def _content_block_data(self, obj):
        lang = self._lang()
        title = getattr(obj, f'title_{lang}') or obj.title_uz
        desc  = getattr(obj, f'description_{lang}') or obj.description_uz

        base = {'title': title, 'description': desc, 'link': obj.link, 'views': obj.views}

        if obj.block_type == 'hero':
            return {'title': title, 'subtitle': desc}

        if obj.block_type == 'rich-text':
            return {'content': desc}

        if obj.block_type == 'quote':
            return {'text': desc, 'author': title, 'role': obj.link}

        if obj.block_type == 'gallery':
            imgs = obj.images.all().order_by('order')
            return {
                'title':  title,
                'images': [
                    {'src': _abs_url(self.context.get('request'), i.image), 'order': i.order}
                    for i in imgs
                ],
            }

        if obj.block_type in ('stats', 'table', 'timeline'):
            return obj.json_data or {}

        # fallback
        return base

    def _link_block_data(self, obj):
        lang  = self._lang()
        title = getattr(obj, f'title_{lang}') or obj.title_uz
        return {
            'title':    title,
            'link':     obj.link,
            'document': _abs_url(self.context.get('request'), obj.document_file),
        }


# ──────────────────────────────────────────────────────────────────────────────
# Org Structure
# ──────────────────────────────────────────────────────────────────────────────

class OrgNodeSerializer(serializers.ModelSerializer):
    title     = serializers.SerializerMethodField()
    structure = serializers.SerializerMethodField()

    class Meta:
        model  = OrgNode
        fields = [
            'id', 'slug', 'node_type', 'title',
            'is_starred', 'is_double_starred', 'is_highlighted',
            'order', 'structure',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(serializers.ListField())
    def get_structure(self, obj):
        qs = obj.children.filter(is_active=True).order_by('order', 'title_uz')
        return OrgNodeSerializer(qs, many=True, context=self.context).data


# ──────────────────────────────────────────────────────────────────────────────
# Org Sections (frontend card view)
# ──────────────────────────────────────────────────────────────────────────────

class OrgNodeCardSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = OrgNode
        fields = [
            'id', 'slug', 'node_type', 'title', 'description',
            'is_starred', 'is_double_starred', 'is_highlighted',
            'section_order',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'description_{lang}') or obj.description_uz


class OrgSectionSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    nodes       = serializers.SerializerMethodField()

    class Meta:
        model  = OrgSection
        fields = ['id', 'slug', 'title', 'description', 'order', 'nodes']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'description_{lang}') or obj.description_uz

    @extend_schema_field(OrgNodeCardSerializer(many=True))
    def get_nodes(self, obj):
        qs = obj.nodes.filter(is_active=True).order_by('section_order')
        return OrgNodeCardSerializer(qs, many=True, context=self.context).data
