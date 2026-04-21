from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from common.pagination import CustomDashboardPagination
from domains.news.models import News, Event, Blog, InformationContent, NewsCategory
from .serializers import (
    NewsSerializer, EventSerializer, BlogSerializer,
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


@extend_schema(tags=['news'], summary="Yangilik kategoriyalari ro'yxati")
class NewsCategoryListAPIView(generics.ListAPIView):
    """Barcha yangilik kategoriyalari."""
    serializer_class   = NewsCategorySerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return NewsCategory.objects.all().order_by('order', 'title_uz')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['news'], summary="Yangiliklar ro'yxati")
class NewsListAPIView(BaseContentListAPIView):
    """Nashr etilgan yangiliklar. ?search= qidiruv. ?category=<slug> filter."""
    serializer_class = NewsSerializer

    def get_queryset(self):
        qs = News.objects.filter(is_published=True).prefetch_related('images', 'categories')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(categories__slug=cat)
        return qs


@extend_schema(tags=['news'], summary="Tadbirlar ro'yxati")
class EventListAPIView(BaseContentListAPIView):
    """Nashr etilgan tadbirlar. ?category=<slug> filter."""
    serializer_class = EventSerializer

    def get_queryset(self):
        qs = Event.objects.filter(is_published=True).prefetch_related('images', 'categories')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(categories__slug=cat)
        return qs


@extend_schema(tags=['news'], summary="Blog ro'yxati")
class BlogListAPIView(BaseContentListAPIView):
    """Nashr etilgan blog yozuvlari. ?category=<slug> filter."""
    serializer_class = BlogSerializer

    def get_queryset(self):
        qs = Blog.objects.filter(is_published=True).select_related('author').prefetch_related('images', 'categories')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(categories__slug=cat)
        return qs


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
