from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes

from common.pagination import CustomDashboardPagination
from rest_framework.generics import get_object_or_404
from domains.news.models import News, Event, Blog, Korrupsiya, InformationContent, NewsCategory
from .serializers import (
    NewsSerializer, EventSerializer, BlogSerializer, KorrupsiyaSerializer,
    InformationContentSerializer, NewsCategorySerializer,
)


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


class BaseContentListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class   = CustomDashboardPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['title_uz', 'title_ru', 'title_en']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Yangilik kategoriyalari ro'yxati (ierarxik)")
class NewsCategoryListAPIView(generics.ListAPIView):
    """Faqat ildiz kategoriyalar; har birida children[] ichida bola kategoriyalar."""
    serializer_class   = NewsCategorySerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return (
            NewsCategory.objects
            .filter(parent=None)
            .prefetch_related('children')
            .order_by('order', 'title_uz')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


_CATEGORY_PARAM = OpenApiParameter(
    name='category', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
    description="Kategoriya slug'i bo'yicha filter (masalan: sport, ilmiy)",
    required=False,
)
_LANG_PARAM = OpenApiParameter(
    name='lang', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
    description="Til: uz | ru | en (default: uz)",
    required=False,
)
_DATE_FROM_PARAM = OpenApiParameter(
    name='date_from', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY,
    description="Boshlanish sanasi (YYYY-MM-DD)",
    required=False,
)
_DATE_TO_PARAM = OpenApiParameter(
    name='date_to', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY,
    description="Tugash sanasi (YYYY-MM-DD)",
    required=False,
)


@extend_schema(tags=['news'], summary="Yangiliklar ro'yxati", parameters=[_CATEGORY_PARAM, _LANG_PARAM, _DATE_FROM_PARAM, _DATE_TO_PARAM])
class NewsListAPIView(BaseContentListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        qs = News.objects.filter(is_published=True).prefetch_related('images', 'categories')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(categories__slug=cat).distinct()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(date__date__gte=date_from)
        if date_to:
            qs = qs.filter(date__date__lte=date_to)
        return qs


_STATUS_PARAM = OpenApiParameter(
    name='status', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
    description="Holat bo'yicha filter: upcoming (kutilayotgan) | completed (tugallangan)",
    required=False,
    enum=['upcoming', 'completed'],
)

@extend_schema(tags=['news'], summary="Tadbirlar ro'yxati", parameters=[_CATEGORY_PARAM, _LANG_PARAM, _STATUS_PARAM])
class EventListAPIView(BaseContentListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        qs = Event.objects.filter(is_published=True).prefetch_related('images', 'categories')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(categories__slug=cat)
        status = self.request.query_params.get('status')
        if status in ('upcoming', 'completed'):
            qs = qs.filter(event_status=status)
        return qs


@extend_schema(tags=['news'], summary="Blog ro'yxati", parameters=[_CATEGORY_PARAM, _LANG_PARAM])
class BlogListAPIView(BaseContentListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        qs = Blog.objects.filter(is_published=True).select_related('author').prefetch_related('images', 'categories')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(categories__slug=cat)
        return qs


@extend_schema(tags=['korrupsiya'], summary="Korrupsiyaga qarshi kurash — ro'yxat")
class KorrupsiyaListAPIView(BaseContentListAPIView):
    serializer_class = KorrupsiyaSerializer

    def get_queryset(self):
        qs = Korrupsiya.objects.filter(is_published=True).prefetch_related('images', 'categories')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(categories__slug=cat)
        return qs


@extend_schema(tags=['korrupsiya'], summary="Korrupsiyaga qarshi kurash — slug bo'yicha")
class KorrupsiyaDetailAPIView(generics.RetrieveAPIView):
    serializer_class   = KorrupsiyaSerializer
    permission_classes = [AllowAny]
    queryset           = Korrupsiya.objects.filter(is_published=True).prefetch_related('images', 'categories')
    lookup_field       = 'slug'

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['korrupsiya'], summary="Korrupsiyaga qarshi kurash — ID bo'yicha")
class KorrupsiyaDetailByIdAPIView(generics.RetrieveAPIView):
    serializer_class   = KorrupsiyaSerializer
    permission_classes = [AllowAny]
    queryset           = Korrupsiya.objects.filter(is_published=True).prefetch_related('images', 'categories')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Yangilik kategoriyasi — slug bo'yicha")
class NewsCategoryDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = NewsCategorySerializer
    permission_classes = [AllowAny]
    queryset           = NewsCategory.objects.all()
    lookup_field       = 'slug'

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Bitta yangilik — slug bo'yicha")
class NewsDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return News.objects.filter(is_published=True).prefetch_related('images', 'categories')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Bitta yangilik — ID bo'yicha")
class NewsDetailByIdAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = NewsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return News.objects.filter(is_published=True).prefetch_related('images', 'categories')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Bitta tadbir — slug bo'yicha")
class EventDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = EventSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return Event.objects.filter(is_published=True).prefetch_related('images', 'categories')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Bitta tadbir — ID bo'yicha")
class EventDetailByIdAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Event.objects.filter(is_published=True).prefetch_related('images', 'categories')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Bitta blog — slug bo'yicha")
class BlogDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related('author').prefetch_related('images', 'categories')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Bitta blog — ID bo'yicha")
class BlogDetailByIdAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = BlogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related('author').prefetch_related('images', 'categories')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Axborot xizmati kontenti")
class InformationContentListAPIView(generics.ListAPIView):
    """
    ?type=rector|briefing|contest|press|photo|video
    ?lang=uz|ru|en
    """
    serializer_class   = InformationContentSerializer
    permission_classes = [AllowAny]
    pagination_class   = CustomDashboardPagination
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['title_uz', 'title_ru', 'title_en']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        qs = (
            InformationContent.objects
            .filter(is_published=True)
            .prefetch_related('images')
            .order_by('-date', '-created_at')
        )
        content_type = self.request.query_params.get('type')
        if content_type:
            qs = qs.filter(content_type=content_type)
        return qs
