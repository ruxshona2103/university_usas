from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from .models import AxborotSection
from .serializers import AxborotSectionSerializer
from domains.students.models import Person
from domains.students.serializers import PersonSerializer


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(
    tags=['axborot'],
    summary="Axborot xizmati vazifalari — barcha bo'limlar",
    description="Har bir bo'lim o'z vazifalar ro'yxati bilan qaytariladi. ?lang=uz|ru|en",
)
class AxborotSectionListAPIView(generics.ListAPIView):
    serializer_class   = AxborotSectionSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return (
            AxborotSection.objects
            .filter(is_active=True)
            .prefetch_related('items')
            .order_by('order', 'number')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['axborot'],
    summary="Axborot xizmati xodimlari",
    description="Axborot xizmati bo'limiga tegishli xodimlar. ?lang=uz|ru|en",
)
class AxborotPersonListAPIView(generics.ListAPIView):
    serializer_class   = PersonSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return (
            Person.objects
            .filter(is_active=True, category__slug='axborot-xizmati')
            .select_related('category')
            .prefetch_related('images', 'tabs__tags')
            .order_by('order', '-id')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx
