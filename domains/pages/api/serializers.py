from rest_framework import serializers
from domains.pages.models import (
    ContactConfig, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo
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


class _StaffSerializer(serializers.Serializer):
    """Ichki ishlatish uchun — academic staff ma'lumotlari."""
    id          = serializers.UUIDField()
    is_head     = serializers.BooleanField()
    role        = serializers.CharField()
    title       = serializers.SerializerMethodField()
    full_name   = serializers.CharField()
    position    = serializers.SerializerMethodField()
    image       = serializers.SerializerMethodField()
    address     = serializers.CharField()
    reception   = serializers.CharField()
    phone       = serializers.CharField()
    fax         = serializers.CharField()
    email       = serializers.EmailField()
    order       = serializers.IntegerField()

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}', obj.title_uz) or obj.title_uz

    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}', obj.position_uz) or obj.position_uz

    def get_image(self, obj):
        if not obj.image:
            return None
        try:
            url = obj.image.url
        except Exception:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url



class NavbarPageSerializer(serializers.ModelSerializer):
    """
    Bitta unified serializer — NavbarSubItem + ixtiyoriy academic ma'lumotlar.

    Javob tuzilmasi:
      slug, name, page_type, content, redirect_url  — har doim
      has_academic                                   — academic unit bog'langanmi
      academic { unit_type, staff, children, ... }   — faqat has_academic=true bo'lsa
    """
    name         = serializers.SerializerMethodField()
    content      = serializers.SerializerMethodField()
    has_academic = serializers.SerializerMethodField()
    academic     = serializers.SerializerMethodField()

    class Meta:
        model  = NavbarSubItem
        fields = [
            'id', 'slug',
            'name',
            'page_type',
            'content',
            'redirect_url',
            'has_academic',
            'academic',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'name_{lang}', obj.name_uz) or obj.name_uz

    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}', obj.content_uz) or obj.content_uz

    def get_has_academic(self, obj):
        return obj.staff.filter(is_active=True).exists()

    def get_academic(self, obj):
        """
        NavbarSubItem ga to'g'ridan bog'langan staff ma'lumotlari.
        Staff bo'lmasa — None.
        """
        staff_qs = obj.staff.filter(is_active=True).order_by('-is_head', 'order')
        if not staff_qs.exists():
            return None

        staff = _StaffSerializer(staff_qs, many=True, context=self.context).data
        return {
            'staff': staff,
        }


class PartnerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = ['id', 'image', 'url', 'title', 'order']

    def get_image(self, obj):
        if not obj.image:
            return None
        try:
            image_url = obj.image.url
        except Exception:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(image_url)
        return image_url

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}


class HeroVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroVideo
        fields = ['id', 'title', 'video_url', 'poster_image', 'is_active', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.poster_image:
            try:
                image_url = instance.poster_image.url
            except Exception:
                data['poster_image'] = None
                return data
            if request:
                data['poster_image'] = request.build_absolute_uri(image_url)
            else:
                data['poster_image'] = image_url
        return data


