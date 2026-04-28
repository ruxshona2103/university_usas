from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.activities.models import ContractPrice, ServiceVehicle, IlmiyFaoliyat, IlmiyFaoliyatCategory


def _safe_file_url(field, request=None):
    """
    Return a robust URL for FileField values.
    - Accepts already-absolute names (legacy seeded data).
    - Avoids crashing when storage backends fail to resolve malformed names.
    """
    if not field:
        return None

    name = (getattr(field, 'name', '') or '').strip()
    if name.startswith(('http://', 'https://')):
        return name

    try:
        url = field.url
    except Exception:
        if not name:
            return None
        return request.build_absolute_uri(name) if request else name

    if request and not str(url).startswith(('http://', 'https://')):
        return request.build_absolute_uri(url)
    return url


class ContractPriceSerializer(serializers.ModelSerializer):
    specialty_name = serializers.SerializerMethodField()
    education_type = serializers.CharField(source='get_education_type_display')
    education_form = serializers.CharField(source='get_education_form_display')

    class Meta:
        model  = ContractPrice
        fields = [
            'id', 'specialty_code', 'specialty_name',
            'education_type', 'education_form',
            'price', 'order',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_specialty_name(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'specialty_name_{lang}') or obj.specialty_name_uz


class ServiceVehicleSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.SerializerMethodField()
    fuel_type    = serializers.CharField(source='get_fuel_type_display')

    class Meta:
        model  = ServiceVehicle
        fields = [
            'id', 'name', 'vehicle_type',
            'manufactured_year', 'fuel_type', 'order',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_vehicle_type(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'vehicle_type_{lang}') or obj.vehicle_type_uz


class IlmiyFaoliyatSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    url   = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyat
        fields = ['id', 'title', 'url', 'order']

    def _req(self):
        return self.context.get('request')

    def _build_url(self, field):
        return _safe_file_url(field, self._req())

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.URI)
    def get_url(self, obj):
        return self._build_url(obj.file)


class IlmiyFaoliyatItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    url   = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyat
        fields = ['id', 'title', 'url', 'order']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_url(self, obj):
        return _safe_file_url(obj.file, self.context.get('request'))


class IlmiyFaoliyatSubCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'order', 'items']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_items(self, obj):
        qs = obj.items.filter(is_active=True).order_by('order')
        return IlmiyFaoliyatItemSerializer(qs, many=True, context=self.context).data


class IlmiyFaoliyatCategoryTreeSerializer(serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    items         = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'order', 'subcategories', 'items']

    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_subcategories(self, obj):
        qs = obj.children.order_by('order')
        return IlmiyFaoliyatSubCategorySerializer(qs, many=True, context=self.context).data

    def get_items(self, obj):
        # Faqat to'g'ridan-to'g'ri bog'liq itemlar (sub-kategoriyasiz)
        qs = obj.items.filter(is_active=True).order_by('order')
        return IlmiyFaoliyatItemSerializer(qs, many=True, context=self.context).data


class IlmiyFaoliyatCategorySimpleSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'description', 'icon', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}


class FaoliyatSubcategoryWriteSerializer(serializers.ModelSerializer):
    """Subcategory yaratish/yangilash uchun."""

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = [
            'id', 'parent',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'icon', 'order',
        ]
        read_only_fields = ['id']


class IlmiyFaoliyatWriteSerializer(serializers.ModelSerializer):
    """IlmiyFaoliyat item yaratish/yangilash uchun."""

    class Meta:
        model  = IlmiyFaoliyat
        fields = [
            'id', 'category',
            'title_uz', 'title_ru', 'title_en',
            'description_uz', 'description_ru', 'description_en',
            'image', 'file', 'order', 'is_active',
        ]
        read_only_fields = ['id']


class IlmiyFaoliyatCategorySerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    blocks      = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'description', 'order', 'blocks']

    def _item_url(self, item):
        return _safe_file_url(item.file, self.context.get('request'))

    def _item_to_link(self, item):
        return {
            'label': {'uz': item.title_uz or '', 'ru': item.title_ru or '', 'en': item.title_en or ''},
            'url': self._item_url(item),
            'order': item.order,
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}

    @extend_schema_field(serializers.ListField())
    def get_blocks(self, obj):
        result = []

        # Sub-kategoriyalar → har biri structure-links blok
        for cat in obj.children.order_by('order'):
            links = [self._item_to_link(item) for item in cat.items.order_by('order')]
            result.append({
                'type': 'structure-links',
                'data': {
                    'title': {'uz': cat.title_uz or '', 'ru': cat.title_ru or '', 'en': cat.title_en or ''},
                    'links': links,
                },
            })

        # To'g'ridan-to'g'ri itemlar → title bo'yicha guruhlash → har bir guruh bitta blok
        groups: dict = {}
        for item in obj.items.order_by('order'):
            key = (item.title_uz or '', item.title_ru or '', item.title_en or '')
            if key not in groups:
                groups[key] = {
                    'title': {'uz': item.title_uz or '', 'ru': item.title_ru or '', 'en': item.title_en or ''},
                    'links': [],
                }
            groups[key]['links'].append(self._item_to_link(item))

        for group in groups.values():
            result.append({'type': 'structure-links', 'data': group})

        return result
