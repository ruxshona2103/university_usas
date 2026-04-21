from rest_framework import serializers
from domains.international.models import ForeignProfessorReview, PartnerOrganization, InternationalPost


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

    def get_position(self, obj):
        lang = self._lang()
        return getattr(obj, f'position_{lang}') or obj.position_uz

    def get_review(self, obj):
        lang = self._lang()
        return getattr(obj, f'review_{lang}') or obj.review_uz

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

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_country(self, obj):
        lang = self._lang()
        return getattr(obj, f'country_{lang}') or obj.country_uz

    def get_logo(self, obj):
        return _abs_url(self.context.get('request'), obj.logo)

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class InternationalPostSerializer(serializers.ModelSerializer):
    title      = serializers.SerializerMethodField()
    content    = serializers.SerializerMethodField()
    image      = serializers.SerializerMethodField()
    type_label = serializers.CharField(source='get_post_type_display', read_only=True)

    class Meta:
        model  = InternationalPost
        fields = ['id', 'post_type', 'type_label', 'title', 'content', 'image', 'date', 'order']

    def _lang(self):
        return self.context.get('lang', 'uz')

    def get_title(self, obj):
        lang = self._lang()
        return getattr(obj, f'title_{lang}') or obj.title_uz

    def get_content(self, obj):
        lang = self._lang()
        return getattr(obj, f'content_{lang}') or obj.content_uz

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)
