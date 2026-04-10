from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from common.pagination import CustomDashboardPagination
from domains.news.models import News, Event, Blog, InformationContent
from .serializers import (
    NewsSerializer, EventSerializer, BlogSerializer,
    InformationContentSerializer,
)


class BaseContentListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class   = CustomDashboardPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['title_uz', 'title_ru', 'title_en']


@extend_schema(tags=['news'], summary="Yangiliklar ro'yxati")
class NewsListAPIView(BaseContentListAPIView):
    """Nashr etilgan yangiliklar. ?search= qidiruv."""
    # News.objects — NewsManager → WHERE article_type='news' AND is_published=True
    queryset         = News.objects.filter(is_published=True).prefetch_related('images')
    serializer_class = NewsSerializer


@extend_schema(tags=['news'], summary="Tadbirlar ro'yxati")
class EventListAPIView(BaseContentListAPIView):
    """Nashr etilgan tadbirlar."""
    queryset         = Event.objects.filter(is_published=True).prefetch_related('images')
    serializer_class = EventSerializer


@extend_schema(tags=['news'], summary="Blog ro'yxati")
class BlogListAPIView(BaseContentListAPIView):
    """Nashr etilgan blog yozuvlari."""
    queryset         = Blog.objects.filter(is_published=True).select_related('author').prefetch_related('images')
    serializer_class = BlogSerializer


@extend_schema(tags=['news'], summary="Axborot xizmati kontenti")
class InformationContentListAPIView(generics.ListAPIView):
    """
    Axborot xizmati kontenti.
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
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
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
