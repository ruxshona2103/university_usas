from rest_framework import serializers
from domains.news.models import News, Event, Blog


class PublishableMixin:
    # frontendchi xoxlagan metodda jsonni chiqarib berish uchun uchta classga mixin >> DRY

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_date(self, obj):
        if not obj.date:
            return None
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')


class NewsSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'image', 'title', 'description', 'date', 'slug', 'badgeCategory', 'views']

    def get_badgeCategory(self, obj):
        return 'news'


class EventSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    location      = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'image', 'title', 'description', 'location', 'date', 'start_time', 'slug', 'badgeCategory', 'views']

    def get_location(self, obj):
        return {'uz': obj.location_uz, 'ru': obj.location_ru, 'en': obj.location_en}

    def get_badgeCategory(self, obj):
        return 'events'


class BlogSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    author_name   = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'image', 'title', 'description', 'date', 'slug', 'badgeCategory', 'author_name', 'views']

    def get_badgeCategory(self, obj):
        return 'blog'

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return None
