from rest_framework import serializers

from ..models import Person, PersonCategory, PersonContent


class PersonCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model  = PersonCategory
        fields = ['id', 'title', 'slug']

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}


class PersonContentSerializer(serializers.ModelSerializer):
    tag_slug  = serializers.CharField(source='tag.slug', read_only=True)
    label     = serializers.SerializerMethodField()
    content   = serializers.SerializerMethodField()

    class Meta:
        model  = PersonContent
        fields = ['tag_slug', 'label', 'content', 'order']

    def get_label(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj.tag, f'name_{lang}', '') or obj.tag.name_uz

    def get_content(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'content_{lang}', '') or obj.content_uz


class PersonSerializer(serializers.ModelSerializer):
    full_name   = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image       = serializers.SerializerMethodField()
    category    = PersonCategorySerializer(read_only=True)
    tabs        = PersonContentSerializer(many=True, read_only=True)

    class Meta:
        model  = Person
        fields = ['id', 'image', 'full_name', 'description', 'category', 'tabs']

    def get_full_name(self, obj):
        return {'uz': obj.full_name_uz, 'ru': obj.full_name_ru or obj.full_name_uz, 'en': obj.full_name_en or obj.full_name_uz}

    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    def get_image(self, obj):
        if not obj.image:
            return None
        try:
            url = obj.image.url
        except Exception:
            return None
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url
