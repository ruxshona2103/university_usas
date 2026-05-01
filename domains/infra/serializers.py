from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from .models import (
    SportMajmua, SportMajmuaImage,
    SportMajmuaStat, SportMajmuaSportTuri, SportMajmuaTadbir,
    Sharoit,
)


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class SportMajmuaImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model  = SportMajmuaImage
        fields = ['id', 'url', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class SportMajmuaStatSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model  = SportMajmuaStat
        fields = ['id', 'label', 'value', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_label(self, obj):
        return {'uz': obj.label_uz, 'ru': obj.label_ru or obj.label_uz, 'en': obj.label_en or obj.label_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_value(self, obj):
        return {'uz': obj.value_uz, 'ru': obj.value_ru or obj.value_uz, 'en': obj.value_en or obj.value_uz}


class SportMajmuaSportTuriSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model  = SportMajmuaSportTuri
        fields = ['id', 'name', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz, 'ru': obj.name_ru or obj.name_uz, 'en': obj.name_en or obj.name_uz}


class SportMajmuaTadbirSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model  = SportMajmuaTadbir
        fields = ['id', 'level', 'title', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}


class SportMajmuaSerializer(serializers.ModelSerializer):
    name        = serializers.SerializerMethodField()
    location    = serializers.SerializerMethodField()
    images      = serializers.SerializerMethodField()
    stats       = serializers.SerializerMethodField()
    sport_types = serializers.SerializerMethodField()
    events      = serializers.SerializerMethodField()

    class Meta:
        model  = SportMajmua
        fields = ['id', 'slug', 'name', 'location', 'images', 'stats', 'sport_types', 'events', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz, 'ru': obj.name_ru or obj.name_uz, 'en': obj.name_en or obj.name_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_location(self, obj):
        return {'uz': obj.location_uz, 'ru': obj.location_ru or obj.location_uz, 'en': obj.location_en or obj.location_uz}

    @extend_schema_field(serializers.ListField())
    def get_images(self, obj):
        return SportMajmuaImageSerializer(
            obj.images.order_by('order'), many=True, context=self.context
        ).data

    @extend_schema_field(serializers.ListField())
    def get_stats(self, obj):
        return SportMajmuaStatSerializer(
            obj.stats.order_by('order'), many=True, context=self.context
        ).data

    @extend_schema_field(serializers.ListField())
    def get_sport_types(self, obj):
        return SportMajmuaSportTuriSerializer(
            obj.sport_types.order_by('order'), many=True, context=self.context
        ).data

    @extend_schema_field(serializers.ListField())
    def get_events(self, obj):
        qs = obj.events.order_by('level', 'order')
        return SportMajmuaTadbirSerializer(qs, many=True, context=self.context).data


class SportMajmuaListSerializer(serializers.ModelSerializer):
    name     = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model  = SportMajmua
        fields = ['id', 'slug', 'name', 'location', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz, 'ru': obj.name_ru or obj.name_uz, 'en': obj.name_en or obj.name_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_location(self, obj):
        return {'uz': obj.location_uz, 'ru': obj.location_ru or obj.location_uz, 'en': obj.location_en or obj.location_uz}


class SharoitSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()

    class Meta:
        model  = Sharoit
        fields = ['id', 'category', 'title', 'description', 'image_url', 'icon', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru or obj.description_uz, 'en': obj.description_en or obj.description_uz}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)
