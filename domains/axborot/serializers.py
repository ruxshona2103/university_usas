from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from .models import AxborotSection, AxborotVazifa


class AxborotVazifaSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()

    class Meta:
        model  = AxborotVazifa
        fields = ['id', 'body', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_body(self, obj):
        return {'uz': obj.body_uz, 'ru': obj.body_ru or obj.body_uz, 'en': obj.body_en or obj.body_uz}


class AxborotSectionSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model  = AxborotSection
        fields = ['id', 'number', 'title', 'order', 'items', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}

    @extend_schema_field(serializers.ListField())
    def get_items(self, obj):
        qs = obj.items.filter(is_active=True).order_by('order')
        return AxborotVazifaSerializer(qs, many=True, context=self.context).data
