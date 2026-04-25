from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from .models import Person, PersonCategory, PersonContent, PersonImage, StudentInfoCategory, StudentInfo, OlimpiyaChempion, MagistrGroup, MagistrStudent


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class PersonCategorySerializer(serializers.ModelSerializer):
    title    = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model  = PersonCategory
        fields = ['id', 'title', 'slug', 'children']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {
            'uz': obj.title_uz,
            'ru': obj.title_ru or obj.title_uz,
            'en': obj.title_en or obj.title_uz,
        }

    @extend_schema_field(serializers.ListField())
    def get_children(self, obj):
        qs = obj.children.order_by('order')
        return PersonCategorySerializer(qs, many=True, context=self.context).data


class PersonImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = PersonImage
        fields = ['id', 'image', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class PersonContentSerializer(serializers.ModelSerializer):
    tags    = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model  = PersonContent
        fields = ['tags', 'content', 'order']

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_tags(self, obj):
        lang = self.context.get('lang', 'uz')
        return [
            {'slug': t.slug, 'name': getattr(t, f'name_{lang}', '') or t.name_uz}
            for t in obj.tags.all()
        ]

    @extend_schema_field(OpenApiTypes.STR)
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

    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        lang = self._lang()
        return getattr(obj, f'full_name_{lang}') or obj.full_name_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        lang = self._lang()
        return getattr(obj, f'description_{lang}') or obj.description_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    @extend_schema_field(PersonImageSerializer(many=True))
    def get_images(self, obj):
        return PersonImageSerializer(
            obj.images.all(), many=True, context=self.context
        ).data

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz


class PersonCategoryWithPersonsSerializer(serializers.ModelSerializer):
    """Kategoriya + ichida o'sha kategoriyaga tegishli shaxslar + children."""
    title    = serializers.SerializerMethodField()
    persons  = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model  = PersonCategory
        fields = ['id', 'title', 'slug', 'children', 'persons']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(serializers.ListField())
    def get_children(self, obj):
        qs = obj.children.order_by('order')
        return PersonCategoryWithPersonsSerializer(qs, many=True, context=self.context).data

    @extend_schema_field(PersonSerializer(many=True))
    def get_persons(self, obj):
        qs = obj.persons.filter(is_active=True).prefetch_related('images', 'tabs__tags').order_by('order', '-id')
        return PersonSerializer(qs, many=True, context=self.context).data


class StudentInfoSerializer(serializers.ModelSerializer):
    title   = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model  = StudentInfo
        fields = ['id', 'title', 'content', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}') or obj.content_uz


class StudentInfoCategorySerializer(serializers.ModelSerializer):
    """Kategoriya + ichida o'sha kategoriyaga tegishli ma'lumotlar + children."""
    title    = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    items    = serializers.SerializerMethodField()

    class Meta:
        model  = StudentInfoCategory
        fields = ['id', 'title', 'slug', 'children', 'items']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(serializers.ListField())
    def get_children(self, obj):
        qs = obj.children.order_by('order')
        return StudentInfoCategorySerializer(qs, many=True, context=self.context).data

    @extend_schema_field(StudentInfoSerializer(many=True))
    def get_items(self, obj):
        qs = obj.items.filter(is_active=True).order_by('order')
        return StudentInfoSerializer(qs, many=True, context=self.context).data


class OlimpiyaChempionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = OlimpiyaChempion
        fields = ['id', 'full_name', 'image_url', 'yonalish', 'guruh', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class MagistrStudentSerializer(serializers.ModelSerializer):
    dissertation_topic = serializers.SerializerMethodField()
    supervisor_info    = serializers.SerializerMethodField()

    class Meta:
        model  = MagistrStudent
        fields = ['order', 'student_name', 'dissertation_topic', 'supervisor_name', 'supervisor_info']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_dissertation_topic(self, obj):
        return getattr(obj, f'dissertation_topic_{self._lang()}') or obj.dissertation_topic_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_supervisor_info(self, obj):
        return getattr(obj, f'supervisor_info_{self._lang()}') or obj.supervisor_info_uz


class MagistrGroupSerializer(serializers.ModelSerializer):
    specialty_name = serializers.SerializerMethodField()
    students       = serializers.SerializerMethodField()

    class Meta:
        model  = MagistrGroup
        fields = ['id', 'specialty_code', 'specialty_name', 'education_lang', 'year', 'order', 'students']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_specialty_name(self, obj):
        return getattr(obj, f'specialty_name_{self._lang()}') or obj.specialty_name_uz

    @extend_schema_field(MagistrStudentSerializer(many=True))
    def get_students(self, obj):
        qs = obj.students.order_by('order')
        return MagistrStudentSerializer(qs, many=True, context=self.context).data
