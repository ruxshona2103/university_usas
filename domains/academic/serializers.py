from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.academic.models import AcademyStat, AcademyDetailPage


class AcademyStatSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model  = AcademyStat
        fields = ['id', 'label', 'value', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_label(self, obj):
        return {'uz': obj.label_uz or '', 'ru': obj.label_ru or '', 'en': obj.label_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_value(self, obj):
        return {'uz': obj.value_uz or '', 'ru': obj.value_ru or '', 'en': obj.value_en or ''}


class AcademyDetailPageSerializer(serializers.ModelSerializer):
    resource_center = serializers.SerializerMethodField()
    detail          = serializers.SerializerMethodField()

    class Meta:
        model  = AcademyDetailPage
        fields = [
            'id',
            'resource_center',
            'edu_direction_count',
            'sport_type_count',
            'masters_count',
            'auditorium_count',
            'detail',
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_resource_center(self, obj):
        return {
            'uz': obj.resource_center_uz or '',
            'ru': obj.resource_center_ru or '',
            'en': obj.resource_center_en or '',
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_detail(self, obj):
        return {
            'uz': obj.detail_uz or '',
            'ru': obj.detail_ru or '',
            'en': obj.detail_en or '',
        }
