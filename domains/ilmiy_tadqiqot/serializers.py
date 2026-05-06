from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from .models import IlmiyTadqiqot, IlmiyTadqiqotFile, IlmiyTadqiqotCategory


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class IlmiyTadqiqotCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyTadqiqotCategory
        fields = ['id', 'slug', 'title', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz


class IlmiyTadqiqotFileSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    file  = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyTadqiqotFile
        fields = ['id', 'title', 'file', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz or ''

    @extend_schema_field(OpenApiTypes.URI)
    def get_file(self, obj):
        return _abs_url(self.context.get('request'), obj.file)


class IlmiyTadqiqotSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    author      = serializers.SerializerMethodField()
    image       = serializers.SerializerMethodField()
    date        = serializers.SerializerMethodField()
    files       = serializers.SerializerMethodField()
    category    = serializers.SerializerMethodField()

    class Meta:
        model  = IlmiyTadqiqot
        fields = [
            'id', 'slug',
            'category',
            'title', 'description', 'author',
            'image', 'files',
            'date',
            'views', 'likes', 'comments',
            'created_at', 'updated_at',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_author(self, obj):
        return {'uz': obj.author_uz, 'ru': obj.author_ru, 'en': obj.author_en}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    @extend_schema_field(OpenApiTypes.DATETIME)
    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S') if obj.date else None

    @extend_schema_field(IlmiyTadqiqotFileSerializer(many=True))
    def get_files(self, obj):
        return IlmiyTadqiqotFileSerializer(
            obj.files.all(), many=True, context=self.context
        ).data

    @extend_schema_field(IlmiyTadqiqotCategorySerializer())
    def get_category(self, obj):
        if obj.category:
            return IlmiyTadqiqotCategorySerializer(obj.category, context=self.context).data
        return None
