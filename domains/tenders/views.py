from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from common.pagination import CustomDashboardPagination
from domains.tenders.models import TenderAnnouncement
from .serializers import TenderAnnouncementSerializer


@extend_schema(tags=['tenders'], summary="Tenderlar va e'lonlar")
class TenderAnnouncementListAPIView(generics.ListAPIView):
    """
    ?search= — sarlavha bo'yicha qidiruv
    ?lang=uz|ru|en
    """
    serializer_class   = TenderAnnouncementSerializer
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
        return (
            TenderAnnouncement.objects
            .filter(is_published=True)
            .prefetch_related('images')
            .order_by('-date')
        )
