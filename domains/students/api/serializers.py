from rest_framework import serializers

from ..models import Person, PersonCategory, PersonContent, PersonImage


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class PersonCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model  = PersonCategory
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        return {
            'uz': obj.title_uz,
            'ru': obj.title_ru or obj.title_uz,
            'en': obj.title_en or obj.title_uz,
        }


class PersonImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = PersonImage
        fields = ['id', 'image', 'order']

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class PersonContentSerializer(serializers.ModelSerializer):
    tags    = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model  = PersonContent
        fields = ['tags', 'content', 'order']

    def get_tags(self, obj):
        lang = self.context.get('lang', 'uz')
        return [
            {'slug': t.slug, 'name': getattr(t, f'name_{lang}', '') or t.name_uz}
            for t in obj.tags.all()
        ]

    def get_content(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'content_{lang}', '') or obj.content_uz


class PersonSerializer(serializers.ModelSerializer):
    full_name   = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image       = serializers.SerializerMethodField()
    images      = serializers.SerializerMethodField()
    title       = serializers.SerializerMethodField()
    position    = serializers.SerializerMethodField()
    category    = PersonCategorySerializer(read_only=True)
    tabs        = PersonContentSerializer(many=True, read_only=True)

    class Meta:
        model  = Person
        fields = [
            'id', 'category',
            'image', 'images',
            'full_name', 'description',
            'title', 'position',
            'phone', 'fax', 'email', 'address', 'reception',
            'is_head', 'order',
            'tabs',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_full_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'full_name_{lang}') or obj.full_name_uz

    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}') or obj.description_uz

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    def get_images(self, obj):
        return PersonImageSerializer(
            obj.images.all(), many=True, context=self.context
        ).data

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz
