from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from .models import SportMajmua
from .serializers import SportMajmuaSerializer, SportMajmuaListSerializer


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(
    tags=['infra'],
    summary="Sport majmualari ro'yxati",
    description="?lang=uz|ru|en",
)
class SportMajmuaListAPIView(generics.ListAPIView):
    serializer_class   = SportMajmuaListSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return SportMajmua.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['infra'],
    summary="Sport majmuasi pasporti (slug bo'yicha)",
    description="Barcha texnik ko'rsatkichlar, sport turlari va tadbirlar. ?lang=uz|ru|en",
)
class SportMajmuaDetailAPIView(generics.RetrieveAPIView):
    serializer_class   = SportMajmuaSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return SportMajmua.objects.filter(is_active=True).prefetch_related(
            'images', 'stats', 'sport_types', 'events'
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx
