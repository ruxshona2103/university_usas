from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from common.models import ContentImage
from domains.news.models import Article, News, Event, Blog, Korrupsiya, InformationContent, InformationImage, NewsCategory



def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class NewsCategorySerializer(serializers.ModelSerializer):
    title    = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model  = NewsCategory
        fields = ['id', 'slug', 'title', 'order', 'children']

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(serializers.ListField())
    def get_children(self, obj):
        qs = obj.children.order_by('order')
        return NewsCategorySerializer(qs, many=True, context=self.context).data



class ContentImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = ContentImage
        fields = ['id', 'image', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class PublishableMixin:
    """DRY mixin — News, Event, Blog uchun umumiy maydonlar."""

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_tavsif(self, obj):
        return {'uz': obj.tavsif_uz, 'ru': obj.tavsif_ru, 'en': obj.tavsif_en}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    @extend_schema_field(OpenApiTypes.DATETIME)
    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S') if obj.date else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_badgeCategory(self, obj):
        return obj.get_content_type()

    @extend_schema_field(ContentImageSerializer(many=True))
    def get_images(self, obj):
        return ContentImageSerializer(
            obj.images.all(), many=True, context=self.context
        ).data

    @extend_schema_field(NewsCategorySerializer(many=True))
    def get_categories(self, obj):
        return NewsCategorySerializer(
            obj.categories.all(), many=True, context=self.context
        ).data


class NewsSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    tavsif        = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    images        = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()
    categories    = serializers.SerializerMethodField()

    class Meta:
        model  = News
        fields = [
            'id', 'image', 'images',
            'title', 'description', 'tavsif',
            'date', 'slug',
            'badgeCategory', 'categories',
            'views', 'likes', 'comments',
            'created_at', 'updated_at',
        ]


class EventSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    tavsif        = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    images        = serializers.SerializerMethodField()
    location      = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()
    categories    = serializers.SerializerMethodField()

    class Meta:
        model  = Event
        fields = [
            'id', 'image', 'images',
            'title', 'description', 'tavsif', 'location',
            'date', 'start_time', 'slug',
            'event_status',
            'badgeCategory', 'categories',
            'views', 'likes', 'comments',
            'created_at', 'updated_at',
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_location(self, obj):
        return {'uz': obj.location_uz, 'ru': obj.location_ru, 'en': obj.location_en}


class BlogSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    tavsif        = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    images        = serializers.SerializerMethodField()
    author_name   = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()
    categories    = serializers.SerializerMethodField()

    class Meta:
        model  = Blog
        fields = [
            'id', 'image', 'images',
            'title', 'description', 'tavsif',
            'date', 'slug',
            'badgeCategory', 'categories',
            'author_name',
            'views', 'likes', 'comments',
            'created_at', 'updated_at',
        ]

    @extend_schema_field(OpenApiTypes.STR)
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return None


class KorrupsiyaSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    tavsif        = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    images        = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()
    categories    = serializers.SerializerMethodField()

    class Meta:
        model  = Korrupsiya
        fields = [
            'id', 'image', 'images',
            'title', 'description', 'tavsif',
            'date', 'slug',
            'badgeCategory', 'categories',
            'views', 'likes', 'comments',
            'created_at', 'updated_at',
        ]


class InformationImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = InformationImage
        fields = ['id', 'image', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class InformationContentSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images      = serializers.SerializerMethodField()
    type_label  = serializers.CharField(source='get_content_type_display', read_only=True)

    class Meta:
        model  = InformationContent
        fields = [
            'id', 'content_type', 'type_label',
            'title', 'description',
            'date', 'video_url', 'external_url',
            'views', 'likes', 'comments',
            'images',
            'created_at', 'updated_at',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}') or obj.description_uz

    @extend_schema_field(InformationImageSerializer(many=True))
    def get_images(self, obj):
        return InformationImageSerializer(
            obj.images.all(), many=True, context=self.context
        ).data
