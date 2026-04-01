from rest_framework import serializers

from domains.academic.models import Staff, StaffContent


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class StaffSerializer(serializers.ModelSerializer):
    """Staff ro'yxati uchun — sahifa (list view)."""
    title     = serializers.SerializerMethodField()
    position  = serializers.SerializerMethodField()
    image     = serializers.SerializerMethodField()
    page_slug = serializers.SerializerMethodField()
    page_url  = serializers.SerializerMethodField()

    class Meta:
        model  = Staff
        fields = [
            'id', 'is_head', 'role',
            'title', 'full_name', 'position',
            'image', 'address', 'reception',
            'phone', 'fax', 'email',
            'order', 'page_slug', 'page_url',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    def get_page_slug(self, obj):
        return obj.navbar_item.slug if obj.navbar_item_id else None

    def get_page_url(self, obj):
        return f'/page/{obj.navbar_item.slug}' if obj.navbar_item_id else None


class StaffTabSerializer(serializers.ModelSerializer):
    """Xodim detail sahifasidagi tab."""
    tag_slug = serializers.CharField(source='tag.slug')
    label    = serializers.SerializerMethodField()
    content  = serializers.SerializerMethodField()

    class Meta:
        model  = StaffContent
        fields = ['tag_slug', 'label', 'content', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_label(self, obj):
        lang = self._lang()
        return getattr(obj.tag, f'name_{lang}') or obj.tag.name_uz

    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}') or obj.content_uz


class StaffDetailSerializer(serializers.ModelSerializer):
    title     = serializers.SerializerMethodField()
    position  = serializers.SerializerMethodField()
    image     = serializers.SerializerMethodField()
    page_slug = serializers.SerializerMethodField()
    page_url  = serializers.SerializerMethodField()
    tabs      = serializers.SerializerMethodField()

    class Meta:
        model  = Staff
        fields = [
            'id', 'is_head', 'role',
            'title', 'full_name', 'position',
            'image', 'address', 'reception',
            'phone', 'fax', 'email',
            'page_slug', 'page_url',
            'tabs',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    def get_page_slug(self, obj):
        return obj.navbar_item.slug if obj.navbar_item_id else None

    def get_page_url(self, obj):
        return f'/page/{obj.navbar_item.slug}' if obj.navbar_item_id else None

    def get_tabs(self, obj):
        tabs = obj.tabs.select_related('tag').order_by('order')
        return StaffTabSerializer(tabs, many=True, context=self.context).data
