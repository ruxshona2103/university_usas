from rest_framework import serializers

from common.models import ContentImage
from domains.pages.models import (
    ContactConfig, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo,
    ContentBlock, LinkBlock,
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

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}


class HeroVideoSerializer(serializers.ModelSerializer):
    poster_image = serializers.SerializerMethodField()

    class Meta:
        model  = HeroVideo
        fields = ['id', 'title', 'video_url', 'poster_image', 'is_active', 'created_at']

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

class _StaffSerializer(serializers.Serializer):
    """Staff ro'yxati uchun ichki serializer (pages context da ishlatiladi)."""
    id        = serializers.UUIDField()
    is_head   = serializers.BooleanField()
    role      = serializers.CharField()
    title     = serializers.SerializerMethodField()
    full_name = serializers.CharField()
    position  = serializers.SerializerMethodField()
    image     = serializers.SerializerMethodField()
    address   = serializers.CharField()
    reception = serializers.CharField()
    phone     = serializers.CharField()
    fax       = serializers.CharField()
    email     = serializers.EmailField()
    order     = serializers.IntegerField()

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}', obj.title_uz) or obj.title_uz

    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}', obj.position_uz) or obj.position_uz

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


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


class _InformationItemSerializer(serializers.Serializer):
    """InformationContent — page detail ichida (news domain dan)."""
    id           = serializers.UUIDField()
    content_type = serializers.CharField()
    title        = serializers.SerializerMethodField()
    description  = serializers.SerializerMethodField()
    date         = serializers.DateTimeField(allow_null=True)
    video_url    = serializers.URLField(allow_null=True)
    external_url = serializers.URLField(allow_null=True)
    views        = serializers.IntegerField()
    images       = serializers.SerializerMethodField()

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}') or obj.description_uz

    def get_images(self, obj):
        request = self.context.get('request')
        return [
            _abs_url(request, img.image)
            for img in obj.images.all().order_by('order')
        ]


class _ForeignReviewSerializer(serializers.Serializer):
    """ForeignProfessorReview — page detail ichida (international domain dan)."""
    id       = serializers.UUIDField()
    full_name = serializers.CharField()
    position = serializers.SerializerMethodField()
    country  = serializers.CharField()
    photo    = serializers.SerializerMethodField()
    review   = serializers.SerializerMethodField()
    order    = serializers.IntegerField()

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz

    def get_photo(self, obj):
        return _abs_url(self.context.get('request'), obj.photo)

    def get_review(self, obj):
        lang = self._lang()
        return getattr(obj, f'review_{lang}') or obj.review_uz


class NavbarPageSerializer(serializers.ModelSerializer):
    """
    /api/pages/{slug}/ — universal page serializer.
    NavbarSubItem ga bog'liq barcha kontent turlari qaytariladi.
    """
    name                = serializers.SerializerMethodField()
    content             = serializers.SerializerMethodField()
    has_staff           = serializers.SerializerMethodField()
    staff               = serializers.SerializerMethodField()
    has_content_blocks  = serializers.SerializerMethodField()
    content_blocks      = serializers.SerializerMethodField()
    has_link_blocks     = serializers.SerializerMethodField()
    link_blocks         = serializers.SerializerMethodField()
    has_information     = serializers.SerializerMethodField()
    information         = serializers.SerializerMethodField()
    has_foreign_reviews = serializers.SerializerMethodField()
    foreign_reviews     = serializers.SerializerMethodField()

    class Meta:
        model  = NavbarSubItem
        fields = [
            'id', 'slug', 'name', 'page_type', 'content', 'redirect_url',
            'has_staff',          'staff',
            'has_content_blocks', 'content_blocks',
            'has_link_blocks',    'link_blocks',
            'has_information',    'information',
            'has_foreign_reviews','foreign_reviews',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}') or obj.name_uz

    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}') or obj.content_uz

    # ── Staff ──
    def get_has_staff(self, obj):
        return obj.staff.filter(is_active=True).exists()

    def get_staff(self, obj):
        qs = obj.staff.filter(is_active=True).order_by('-is_head', 'order')
        return _StaffSerializer(qs, many=True, context=self.context).data

    # ── ContentBlock ──
    def get_has_content_blocks(self, obj):
        return obj.contentblock_items.filter(is_active=True).exists()

    def get_content_blocks(self, obj):
        qs = (
            obj.contentblock_items
            .filter(is_active=True)
            .prefetch_related('images', 'tags')
            .order_by('order', 'created_at')
        )
        return _ContentBlockSerializer(qs, many=True, context=self.context).data

    # ── LinkBlock ──
    def get_has_link_blocks(self, obj):
        return obj.linkblock_items.filter(is_active=True).exists()

    def get_link_blocks(self, obj):
        qs = obj.linkblock_items.filter(is_active=True).order_by('order', 'created_at')
        return _LinkBlockSerializer(qs, many=True, context=self.context).data

    # ── InformationContent (news domain) ──
    def get_has_information(self, obj):
        return obj.information_items.filter(is_published=True).exists()

    def get_information(self, obj):
        qs = (
            obj.information_items
            .filter(is_published=True)
            .prefetch_related('images')
            .order_by('-date', '-created_at')
        )
        return _InformationItemSerializer(qs, many=True, context=self.context).data

    # ── ForeignProfessorReview (international domain) ──
    def get_has_foreign_reviews(self, obj):
        return obj.foreign_reviews.filter(is_active=True).exists()

    def get_foreign_reviews(self, obj):
        qs = obj.foreign_reviews.filter(is_active=True).order_by('order', 'created_at')
        return _ForeignReviewSerializer(qs, many=True, context=self.context).data
