from rest_framework import serializers
from domains.news.models import News, Event, Blog


class NewsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'image', 'title', 'excerpt', 'date', 'slug', 'badgeCategory', 'views']

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

    def get_excerpt(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    def get_badgeCategory(self, obj):
        return 'news'


class EventSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'image', 'title', 'excerpt', 'location', 'date', 'start_time', 'slug', 'badgeCategory', 'views']

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

    def get_excerpt(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    def get_location(self, obj):
        return {'uz': obj.location_uz, 'ru': obj.location_ru, 'en': obj.location_en}

    def get_badgeCategory(self, obj):
        return 'events'


class BlogSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'image', 'title', 'excerpt', 'date', 'slug', 'badgeCategory', 'author_name', 'views']

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

    def get_excerpt(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    def get_badgeCategory(self, obj):
        return 'blog'

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return None
