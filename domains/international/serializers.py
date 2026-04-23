from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.openapi import OpenApiTypes

from domains.international.models import (
    ForeignProfessorReview, PartnerOrganization,
    InternationalPost, InternationalPostImage,
    InternationalRating, InternationalRatingImage,
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
