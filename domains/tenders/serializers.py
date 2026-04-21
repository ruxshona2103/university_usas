from rest_framework import serializers

from domains.tenders.models import TenderAnnouncement, TenderImage


def _abs_url(request, field):
    if not field:
        return None
    try:
        url = field.url
    except Exception:
        return None
    return request.build_absolute_uri(url) if request else url


class TenderImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model  = TenderImage
        fields = ['id', 'image', 'order']

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class TenderAnnouncementSerializer(serializers.ModelSerializer):
    title       = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images      = serializers.SerializerMethodField()

    class Meta:
        model  = TenderAnnouncement
        fields = [
            'id', 'title', 'description',
            'date', 'address', 'email', 'phone',
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
        return TenderImageSerializer(obj.images.all(), many=True, context=self.context).data
