from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.international.models import (
    ForeignProfessorReview, PartnerOrganization, PartnerPageConfig,
    InternationalPost, InternationalPostImage,
    InternationalRating, InternationalRatingImage,
    InternationalDeptConfig, MemorandumStat,
    AkademikAlmashinuv, AkademikAlmashinuvRasm,
    XalqaroReytingBolim,
)


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class ForeignProfessorReviewSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    review   = serializers.SerializerMethodField()
    photo    = serializers.SerializerMethodField()

    class Meta:
        model  = ForeignProfessorReview
        fields = ['id', 'full_name', 'position', 'country', 'photo', 'review', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_review(self, obj):
        lang = self._lang()
        return getattr(obj, f'review_{lang}') or obj.review_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_photo(self, obj):
        return _abs_url(self.context.get('request'), obj.photo)


class PartnerOrganizationSerializer(serializers.ModelSerializer):
    title   = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    logo    = serializers.SerializerMethodField()
    image   = serializers.SerializerMethodField()

    class Meta:
        model  = PartnerOrganization
        fields = ['id', 'partner_type', 'title', 'country', 'logo', 'image', 'website', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_country(self, obj):
        lang = self._lang()
        return getattr(obj, f'country_{lang}') or obj.country_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_logo(self, obj):
        return _abs_url(self.context.get('request'), obj.logo)

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class PartnerPageConfigSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model  = PartnerPageConfig
        fields = ['title', 'description']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz or '', 'ru': obj.title_ru or '', 'en': obj.title_en or ''}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz or '', 'ru': obj.description_ru or '', 'en': obj.description_en or ''}


class InternationalDeptConfigSerializer(serializers.ModelSerializer):
    head_name     = serializers.SerializerMethodField()
    head_position = serializers.SerializerMethodField()
    tasks         = serializers.SerializerMethodField()
    head_photo    = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalDeptConfig
        fields = [
            'slug',
            'head_name', 'head_position', 'head_working_hours',
            'head_phone', 'head_email', 'head_photo', 'tasks',
        ]

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_head_name(self, obj):
        return getattr(obj, f'head_name_{self._lang()}') or obj.head_name_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_head_position(self, obj):
        return getattr(obj, f'head_position_{self._lang()}') or obj.head_position_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_head_photo(self, obj):
        return _abs_url(self.context.get('request'), obj.head_photo)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_tasks(self, obj):
        raw = getattr(obj, f'tasks_{self._lang()}') or obj.tasks_uz or ''
        return [line.strip() for line in raw.splitlines() if line.strip()]


class MemorandumStatSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    class Meta:
        model  = MemorandumStat
        fields = ['id', 'organization', 'foreign_count', 'domestic_count', 'order']

    @extend_schema_field(OpenApiTypes.STR)
    def get_organization(self, obj):
        lang = self.context.get('lang', 'uz')
        return getattr(obj, f'organization_{lang}') or obj.organization_uz


class InternationalPostImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalPostImage
        fields = ['id', 'image', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class InternationalRatingImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalRatingImage
        fields = ['id', 'image', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class InternationalRatingSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    cover       = serializers.SerializerMethodField()
    images      = serializers.SerializerMethodField()

    class Meta:
        model  = InternationalRating
        fields = ['id', 'slug', 'title', 'description', 'cover', 'images', 'date', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, obj):
        return getattr(obj, f'title_{self._lang()}') or obj.title_uz

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj):
        return getattr(obj, f'description_{self._lang()}') or obj.description_uz

    @extend_schema_field(OpenApiTypes.URI)
    def get_cover(self, obj):
        return _abs_url(self.context.get('request'), obj.cover)

    @extend_schema_field(InternationalRatingImageSerializer(many=True))
    def get_images(self, obj):
        qs = obj.images.all().order_by('order')
        return InternationalRatingImageSerializer(qs, many=True, context=self.context).data


class InternationalPostSerializer(serializers.ModelSerializer):
    title      = serializers.SerializerMethodField()
    content    = serializers.SerializerMethodField()
    image      = serializers.SerializerMethodField()
    images     = serializers.SerializerMethodField()
    type_label = serializers.CharField(source='get_post_type_display', read_only=True)

    class Meta:
        model  = InternationalPost
        fields = ['id', 'post_type', 'type_label', 'title', 'content', 'image', 'images', 'date', 'order']

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

    @extend_schema_field(OpenApiTypes.URI)
    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    @extend_schema_field(InternationalPostImageSerializer(many=True))
    def get_images(self, obj):
        qs = obj.images.all().order_by('order')
        return InternationalPostImageSerializer(qs, many=True, context=self.context).data


class AkademikAlmashinuvRasmSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    caption   = serializers.SerializerMethodField()

    class Meta:
        model  = AkademikAlmashinuvRasm
        fields = ['id', 'image_url', 'caption', 'order']

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_caption(self, obj):
        return {'uz': obj.caption_uz, 'ru': obj.caption_ru or obj.caption_uz, 'en': obj.caption_en or obj.caption_uz}


class AkademikAlmashinuvSerializer(serializers.ModelSerializer):
    title  = serializers.SerializerMethodField()
    body   = serializers.SerializerMethodField()
    rasmlar = serializers.SerializerMethodField()

    class Meta:
        model  = AkademikAlmashinuv
        fields = ['id', 'title', 'body', 'rasmlar', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_body(self, obj):
        return {'uz': obj.body_uz, 'ru': obj.body_ru or obj.body_uz, 'en': obj.body_en or obj.body_uz}

    @extend_schema_field(AkademikAlmashinuvRasmSerializer(many=True))
    def get_rasmlar(self, obj):
        return AkademikAlmashinuvRasmSerializer(
            obj.rasmlar.all(), many=True, context=self.context
        ).data


class XalqaroReytingBolimSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image_url   = serializers.SerializerMethodField()

    class Meta:
        model  = XalqaroReytingBolim
        fields = ['id', 'bolim_type', 'title', 'description', 'image_url', 'link', 'order']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_title(self, obj):
        return {'uz': obj.title_uz, 'ru': obj.title_ru or obj.title_uz, 'en': obj.title_en or obj.title_uz}

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_description(self, obj):
        return {'uz': obj.description_uz, 'ru': obj.description_ru or obj.description_uz, 'en': obj.description_en or obj.description_uz}

    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self, obj):
        return _abs_url(self.context.get('request'), obj.image)
