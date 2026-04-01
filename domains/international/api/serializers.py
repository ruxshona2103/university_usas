from rest_framework import serializers
from domains.international.models import ForeignProfessorReview


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
