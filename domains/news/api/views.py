from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from domains.news.models import News, Event, Blog
from .serializers import NewsSerializer, EventSerializer, BlogSerializer


@extend_schema(tags=['news'])
class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['events'])
class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.filter(is_published=True)
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['blog'])
class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=True).select_related('author')
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
