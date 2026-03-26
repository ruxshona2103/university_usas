from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from domains.news.models import News, Event, Blog
from .serializers import NewsSerializer, EventSerializer, BlogSerializer
from common.pagination import CustomDashboardPagination

class BaseContentListAPIView(generics.ListAPIView):
    # DRY method -- kodlaar takrorlanishini oldini olish uchun.
    permission_classes = [AllowAny]
    pagination_class = CustomDashboardPagination
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['title_uz', 'title_ru', 'title_en']
    

@extend_schema(tags=['news'])
class NewsListAPIView(BaseContentListAPIView):
    queryset = News.objects.filter(is_published=True).order_by('-date')
    serializer_class = NewsSerializer

@extend_schema(tags=['events'])
class EventListAPIView(BaseContentListAPIView):
    queryset = Event.objects.filter(is_published=True).order_by('-date')
    serializer_class = EventSerializer

@extend_schema(tags=['blog'])
class BlogListAPIView(BaseContentListAPIView):
    queryset = Blog.objects.filter(is_published=True).select_related('author').order_by('-date')
    serializer_class = BlogSerializer