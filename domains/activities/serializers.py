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


class IlmiyFaoliyatCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyatCategory
        fields = ['id', 'slug', 'title', 'order', 'items']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(serializers.ListField())
    def get_items(self, obj):
        qs = obj.items.filter(is_active=True).order_by('order')
        return IlmiyFaoliyatSerializer(qs, many=True, context=self.context).data


class IlmiyFaoliyatSerializer(serializers.ModelSerializer):
    title     = serializers.SerializerMethodField()
    category  = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    file_url  = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyFaoliyat
        fields = ['id', 'title', 'category', 'image_url', 'file_url', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    def _req(self):
        return self.context.get('request')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        return getattr(obj, f'title_{self._lang()}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_category(self, obj):
        if not obj.category:
            return None
        return {
            'slug':  obj.category.slug,
            'title': getattr(obj.category, f'title_{self._lang()}') or obj.category.title_uz,
        }

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        if not obj.image:
            return None
        req = self._req()
        return req.build_absolute_uri(obj.image.url) if req else obj.image.url

    @extend_schema_field(OpenApiTypes.URI)
    def get_file_url(self, obj):
        if not obj.file:
            return None
        req = self._req()
        return req.build_absolute_uri(obj.file.url) if req else obj.file.url
