from rest_framework import serializers

from ..models import Person, PersonCategory

class PersonCategorySerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = PersonCategory
        fields = ['title', 'slug']

    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru, 'en': obj.title_en}

class PersonSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    tags = PersonCategorySerializer(source='categories', many=True, read_only=True)

    class Meta:
        model = Person
        fields = ['id', 'image', 'full_name', 'description', 'tags']

    def get_full_name(self, obj):
        return {'uz': obj.full_name_uz, 'ru': obj.full_name_ru, 'en': obj.full_name_en}

    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru, 'en': obj.description_en}

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None