from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from common.pagination import CustomDashboardPagination
from domains.tenders.models import TenderAnnouncement
from .serializers import TenderAnnouncementSerializer
from domains.tracker.mixins import ViewsCountMixin
from domains.tracker.views import RecordViewAPIView


@extend_schema(tags=['tenders'], summary="Tenderlar va e'lonlar")
class TenderAnnouncementListAPIView(ViewsCountMixin, generics.ListAPIView):
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


@extend_schema(tags=['tenders'], summary="Tender — ID bo'yicha")
class TenderAnnouncementDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    serializer_class   = TenderAnnouncementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return TenderAnnouncement.objects.filter(is_published=True).prefetch_related('images')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['tenders'], summary="Tanlovlar (e'lonlar) ro'yxati")
class TanlovListAPIView(ViewsCountMixin, generics.ListAPIView):
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
            .filter(is_published=True, announcement_type='tanlov')
            .prefetch_related('images')
            .order_by('-date')
        )


@extend_schema(tags=['tenders'], summary="Tanlov — ID bo'yicha")
class TanlovDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    serializer_class   = TenderAnnouncementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return TenderAnnouncement.objects.filter(is_published=True, announcement_type='tanlov').prefetch_related('images')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


class TenderRecordViewAPIView(RecordViewAPIView):
    model_class = TenderAnnouncement
