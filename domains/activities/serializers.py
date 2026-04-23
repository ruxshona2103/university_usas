from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.activities.models import ContractPrice, ServiceVehicle, IlmiyFaoliyat, IlmiyFaoliyatCategory


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
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category    = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()
    url         = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyat
        fields = ['id', 'title', 'description', 'category', 'image_url', 'url', 'order']

    def _req(self):
        return self.context.get('request')

    def _build_url(self, field):
        if not field:
            return None
        req = self._req()
        return req.build_absolute_uri(field.url) if req else field.url

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_category(self, obj):
        if not obj.category:
            return None
        return {
            'slug':  obj.category.slug,
            'title': {'uz': obj.category.title_uz or '', 'ru': obj.category.title_ru or '', 'en': obj.category.title_en or ''},
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return self._build_url(obj.image)

    @extend_schema_field(OpenApiTypes.URI)
    def get_url(self, obj):
        return self._build_url(obj.file)


class IlmiyFaoliyatCategorySerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    children    = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'description', 'order', 'children']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}

    @extend_schema_field(serializers.ListField())
    def get_children(self, obj):
        result = []

        # Sub-kategoriyalar (type: category)
        for cat in obj.children.order_by('order'):
            result.append({
                'type': 'category',
                **IlmiyFaoliyatCategorySerializer(cat, context=self.context).data,
            })

        # Itemlar (type: item)
        for item in obj.items.filter(is_active=True).order_by('order'):
            data = IlmiyFaoliyatSerializer(item, context=self.context).data
            data['type'] = 'item'
            result.append(data)

        return result
