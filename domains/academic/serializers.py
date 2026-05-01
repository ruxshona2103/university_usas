from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.academic.models import AcademyStat, AcademyDetailPage, FakultetKafedra, KafedraPublication, KafedraXodim, KafedraRasm, HuzuridagiTashkilot


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
    """Professor-o'qituvchilar tarkibi — faqat rasm, ism, lavozim."""
    full_name = serializers.SerializerMethodField()
    lavozim   = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model  = KafedraXodim
        fields = ['id', 'full_name', 'lavozim', 'photo_url', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_full_name(self, obj):
        return obj.person.full_name_uz

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_lavozim(self, obj):
        return {
            'uz': obj.person.title_uz or '',
            'ru': obj.person.title_ru or '',
            'en': obj.person.title_en or '',
        }

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
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model  = KafedraPublication
        fields = ['id', 'cover_url', 'order']

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


def _photo_url(request, field):
    if not field:
        return None
    try:
        return request.build_absolute_uri(field.url) if request else field.url
    except Exception:
        return None


class FakultetKafedraDetailSerializer(serializers.ModelSerializer):
    name               = serializers.SerializerMethodField()
    description        = serializers.SerializerMethodField()
    about              = serializers.SerializerMethodField()
    sport_types        = serializers.SerializerMethodField()
    bachelor_subjects  = serializers.SerializerMethodField()
    master_subjects    = serializers.SerializerMethodField()
    dean               = serializers.SerializerMethodField()
    vice_dean          = serializers.SerializerMethodField()
    mudiri             = serializers.SerializerMethodField()
    publications       = KafedraPublicationSerializer(many=True, read_only=True)
    professor_tarkibi  = serializers.SerializerMethodField()
    rasmlar            = KafedraRasmSerializer(many=True, read_only=True)

    class Meta:
        model  = FakultetKafedra
        fields = [
            'id', 'slug', 'type',
            'name', 'description', 'about',
            'decree_info', 'phone', 'email', 'link',
            'sport_types', 'bachelor_subjects', 'master_subjects',
            'dean', 'vice_dean', 'mudiri',
            'publications', 'professor_tarkibi', 'rasmlar',
            'order',
            'created_at', 'updated_at',
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

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_dean(self, obj):
        req = self.context.get('request')
        return {
            'name':      {'uz': obj.dean_name_uz or '', 'ru': obj.dean_name_ru or '', 'en': obj.dean_name_en or ''},
            'photo_url': _photo_url(req, obj.dean_photo),
            'phone':     obj.dean_phone or '',
            'email':     obj.dean_email or '',
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_vice_dean(self, obj):
        req = self.context.get('request')
        return {
            'name':      {'uz': obj.vice_dean_name_uz or '', 'ru': obj.vice_dean_name_ru or '', 'en': obj.vice_dean_name_en or ''},
            'photo_url': _photo_url(req, obj.vice_dean_photo),
            'phone':     obj.vice_dean_phone or '',
            'email':     obj.vice_dean_email or '',
        }

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_mudiri(self, obj):
        req = self.context.get('request')
        return {
            'name':      {'uz': obj.mudiri_name_uz or '', 'ru': obj.mudiri_name_ru or '', 'en': obj.mudiri_name_en or ''},
            'photo_url': _photo_url(req, obj.mudiri_photo),
            'phone':     obj.mudiri_phone or '',
            'email':     obj.mudiri_email or '',
            'degree':    {'uz': obj.mudiri_degree_uz or '', 'ru': obj.mudiri_degree_ru or '', 'en': obj.mudiri_degree_en or ''},
        }

    @extend_schema_field(serializers.ListField())
    def get_professor_tarkibi(self, obj):
        return KafedraXodimSerializer(
            obj.xodimlar.order_by('order').select_related('person'),
            many=True,
            context=self.context,
        ).data


class HuzuridagiTashkilotSerializer(serializers.ModelSerializer):
    name        = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address     = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()

    class Meta:
        model  = HuzuridagiTashkilot
        fields = ['id', 'name', 'description', 'image_url', 'website', 'phone', 'email', 'address', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz, 'ru': obj.name_ru or obj.name_uz, 'en': obj.name_en or obj.name_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru or obj.description_uz, 'en': obj.description_en or obj.description_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_address(self, obj):
        return {'uz': obj.address_uz, 'ru': obj.address_ru or obj.address_uz, 'en': obj.address_en or obj.address_uz}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _photo_url(self.context.get('request'), obj.image)


class JamoatTashkilotSerializer(serializers.ModelSerializer):
    name        = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()

    class Meta:
        model  = HuzuridagiTashkilot
        fields = ['id', 'slug', 'name', 'description', 'image_url', 'website', 'phone', 'email', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz, 'ru': obj.name_ru or obj.name_uz, 'en': obj.name_en or obj.name_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru or obj.description_uz, 'en': obj.description_en or obj.description_uz}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _photo_url(self.context.get('request'), obj.image)


class JamoatTashkilotPersonSerializer(serializers.Serializer):
    id        = serializers.IntegerField(source='person.id')
    full_name = serializers.SerializerMethodField()
    title     = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    phone     = serializers.CharField(source='person.phone', default='')
    email     = serializers.EmailField(source='person.email', default='')

    def get_full_name(self, obj):
        p = obj.person
        return {'uz': p.full_name_uz, 'ru': p.full_name_ru or p.full_name_uz, 'en': p.full_name_en or p.full_name_uz}

    def get_title(self, obj):
        p = obj.person
        return {'uz': p.title_uz or '', 'ru': p.title_ru or '', 'en': p.title_en or ''}

    def get_photo_url(self, obj):
        return _photo_url(self.context.get('request'), obj.person.image)


class JamoatTashkilotDetailSerializer(serializers.ModelSerializer):
    name        = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    about       = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()
    person      = serializers.SerializerMethodField()

    class Meta:
        model  = HuzuridagiTashkilot
        fields = ['id', 'slug', 'name', 'description', 'about', 'image_url', 'website', 'phone', 'email', 'person', 'order', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_name(self, obj):
        return {'uz': obj.name_uz, 'ru': obj.name_ru or obj.name_uz, 'en': obj.name_en or obj.name_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru or obj.description_uz, 'en': obj.description_en or obj.description_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_about(self, obj):
        return {'uz': obj.about_uz or '', 'ru': obj.about_ru or '', 'en': obj.about_en or ''}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _photo_url(self.context.get('request'), obj.image)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_person(self, obj):
        if not obj.person_id:
            return None
        p = obj.person
        return {
            'id':        p.id,
            'full_name': {'uz': p.full_name_uz, 'ru': p.full_name_ru or p.full_name_uz, 'en': p.full_name_en or p.full_name_uz},
            'title':     {'uz': p.title_uz or '', 'ru': p.title_ru or '', 'en': p.title_en or ''},
            'photo_url': _photo_url(self.context.get('request'), p.image),
            'phone':     p.phone or '',
            'email':     str(p.email) if p.email else '',
        }
