from rest_framework import serializers
from domains.pages.models import (
    ContactConfig, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner,
)


class ContactConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactConfig
        fields = ['email', 'phone', 'address_uz', 'address_ru', 'address_en']


class PresidentQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresidentQuote
        fields = ['id', 'author', 'quote_uz', 'quote_ru', 'quote_en']


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='get_platform_display', read_only=True)

    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'platform_name', 'url']


# ----------------------------------------------NAVBAR---------------------------------------------------------

class NavbarSubItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarSubItem
        fields = [
            'id', 'name_uz', 'name_ru', 'name_en',
            'slug', 'page_type', 'redirect_url', 'order',
        ]


class NavbarCategorySerializer(serializers.ModelSerializer):
    items = NavbarSubItemSerializer(many=True, read_only=True)

    class Meta:
        model = NavbarCategory
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'slug', 'order', 'items']


class NavbarLanguageGroupedSerializer(serializers.Serializer):

    def to_representation(self, categories):
        result = {'uz': [], 'ru': [], 'en': []}
        for lang in ('uz', 'ru', 'en'):
            for cat in categories:
                label = getattr(cat, f'name_{lang}') or cat.name_uz
                items = [
                    getattr(item, f'name_{lang}') or item.name_uz
                    for item in cat.items.all()
                ]
                result[lang].append({
                    'key':   cat.slug,
                    'label': label,
                    'items': items,
                })
        return result


class NavbarPageSerializer(serializers.ModelSerializer):
    category_name_uz = serializers.CharField(source='category.name_uz', read_only=True)
    is_empty = serializers.SerializerMethodField()

    class Meta:
        model = NavbarSubItem
        fields = [
            'id', 'category_name_uz',
            'name_uz', 'name_ru', 'name_en',
            'slug', 'page_type', 'is_empty',
            'content_uz', 'content_ru', 'content_en',
            'redirect_url',
        ]

    def get_is_empty(self, obj):
        if obj.page_type == NavbarSubItem.PageType.REDIRECT:
            return False
        return not any([obj.content_uz, obj.content_ru, obj.content_en])


class PartnerSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id', 'image', 'url', 'title', 'order']

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}
