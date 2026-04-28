from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.academic.models import AcademyStat, AcademyDetailPage, FakultetKafedra, KafedraPublication, KafedraXodim, KafedraRasm


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
            'id', 'resource_center',
            'edu_direction_count', 'sport_type_count', 'masters_count', 'auditorium_count',
            'detail',
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_resource_center(self, obj):
        return {'uz': obj.resource_center_uz or '', 'ru': obj.resource_center_ru or '', 'en': obj.resource_center_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_detail(self, obj):
        return {'uz': obj.detail_uz or '', 'ru': obj.detail_ru or '', 'en': obj.detail_en or ''}


def _split_lines(text):
    """Newline-separated text → non-empty list."""
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


class KafedraRasmSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    caption   = serializers.SerializerMethodField()

    class Meta:
        model  = KafedraRasm
        fields = ['id', 'image_url', 'caption', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            try:
                return request.build_absolute_uri(obj.image.url) if request else obj.image.url
            except Exception:
                return None
        return None

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_caption(self, obj):
        return {'uz': obj.caption_uz or '', 'ru': obj.caption_ru or '', 'en': obj.caption_en or ''}


class KafedraXodimSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position  = serializers.SerializerMethodField()
    email     = serializers.SerializerMethodField()
    phone     = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model  = KafedraXodim
        fields = ['id', 'full_name', 'position', 'email', 'phone', 'photo_url', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        return obj.person.full_name_uz

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_position(self, obj):
        return {
            'uz': obj.person.title_uz or '',
            'ru': obj.person.title_ru or '',
            'en': obj.person.title_en or '',
        }

    @extend_schema_field(OpenApiTypes.STR)
    def get_email(self, obj):
        return obj.person.email or ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_phone(self, obj):
        return obj.person.phone or ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.person.image:
            try:
                return request.build_absolute_uri(obj.person.image.url) if request else obj.person.image.url
            except Exception:
                return None
        return None


class KafedraPublicationSerializer(serializers.ModelSerializer):
    title    = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model  = KafedraPublication
        fields = ['id', 'title', 'author', 'pub_type', 'cover_url', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.STR)
    def get_cover_url(self, obj):
        request = self.context.get('request')
        if obj.cover:
            try:
                return request.build_absolute_uri(obj.cover.url) if request else obj.cover.url
            except Exception:
                return None
        return None


class FakultetKafedraListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model  = FakultetKafedra
        fields = ['id', 'slug', 'type', 'name', 'link', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz or '', 'ru': obj.name_ru or '', 'en': obj.name_en or ''}


class FakultetKafedraDetailSerializer(serializers.ModelSerializer):
    name               = serializers.SerializerMethodField()
    description        = serializers.SerializerMethodField()
    about              = serializers.SerializerMethodField()
    sport_types        = serializers.SerializerMethodField()
    bachelor_subjects  = serializers.SerializerMethodField()
    master_subjects    = serializers.SerializerMethodField()
    publications       = KafedraPublicationSerializer(many=True, read_only=True)
    xodimlar           = KafedraXodimSerializer(many=True, read_only=True)
    rasmlar            = KafedraRasmSerializer(many=True, read_only=True)

    class Meta:
        model  = FakultetKafedra
        fields = [
            'id', 'slug', 'type',
            'name', 'description', 'about',
            'decree_info', 'phone', 'email', 'link',
            'sport_types', 'bachelor_subjects', 'master_subjects',
            'publications', 'xodimlar', 'rasmlar',
            'order',
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz or '', 'ru': obj.name_ru or '', 'en': obj.name_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_about(self, obj):
        return {'uz': obj.about_uz or '', 'ru': obj.about_ru or '', 'en': obj.about_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_sport_types(self, obj):
        return {
            'uz': _split_lines(obj.sport_types_uz),
            'ru': _split_lines(obj.sport_types_ru),
            'en': _split_lines(obj.sport_types_en),
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_bachelor_subjects(self, obj):
        return {
            'uz': _split_lines(obj.bachelor_subjects_uz),
            'ru': _split_lines(obj.bachelor_subjects_ru),
            'en': _split_lines(obj.bachelor_subjects_en),
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_master_subjects(self, obj):
        return {
            'uz': _split_lines(obj.master_subjects_uz),
            'ru': _split_lines(obj.master_subjects_ru),
            'en': _split_lines(obj.master_subjects_en),
        }
