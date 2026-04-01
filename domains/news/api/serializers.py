from rest_framework import serializers

from domains.news.models import News, Event, Blog, InformationContent, InformationImage


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class PublishableMixin:
    """DRY mixin — News, Event, Blog uchun umumiy maydonlar."""

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    def get_date(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S') if obj.date else None


class NewsSerializer(PublishableMixin, serializers.ModelSerializer):
    title         = serializers.SerializerMethodField()
    description   = serializers.SerializerMethodField()
    image         = serializers.SerializerMethodField()
    date          = serializers.SerializerMethodField()
    badgeCategory = serializers.SerializerMethodField()

    class Meta:
        model  = News
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
        model  = Event
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
        model  = Blog
        fields = ['id', 'image', 'title', 'description', 'date', 'slug', 'badgeCategory', 'author_name', 'views']

    def get_badgeCategory(self, obj):
        return 'blog'

    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return None


class InformationImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = InformationImage
        fields = ['id', 'image', 'order']

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class InformationContentSerializer(serializers.ModelSerializer):
    """
    Axborot xizmati kontent — rektor tadbirlari, brifinglar,
    tanlovlar, matbuot xizmati, fotogalereya, videogalereya.
    """
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
            'views', 'images',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}') or obj.description_uz

    def get_images(self, obj):
        return InformationImageSerializer(
            obj.images.all(), many=True, context=self.context
        ).data
