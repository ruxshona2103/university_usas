from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes

from common.cache_mixin import cached_list
from common.pagination import CustomDashboardPagination
from domains.tracker.mixins import ViewsCountMixin
from domains.tracker.views import RecordViewAPIView

from .models import IlmiyTadqiqot, IlmiyTadqiqotCategory
from .serializers import IlmiyTadqiqotSerializer, IlmiyTadqiqotCategorySerializer


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


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
_CATEGORY_PARAM = OpenApiParameter(
    name='category', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
    description="Kategoriya slug'i bo'yicha filter",
    required=False,
)


@extend_schema(tags=['ilmiy-tadqiqot'], summary="Ilmiy tadqiqot kategoriyalari ro'yxati")
class IlmiyTadqiqotCategoryListAPIView(generics.ListAPIView):
    serializer_class   = IlmiyTadqiqotCategorySerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return IlmiyTadqiqotCategory.objects.all().order_by('order', 'title_uz')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@cached_list(60)
@extend_schema(
    tags=['ilmiy-tadqiqot'],
    summary="Ilmiy tadqiqotlar ro'yxati",
    parameters=[_LANG_PARAM, _CATEGORY_PARAM, _DATE_FROM_PARAM, _DATE_TO_PARAM],
)
class IlmiyTadqiqotListAPIView(ViewsCountMixin, generics.ListAPIView):
    serializer_class   = IlmiyTadqiqotSerializer
    permission_classes = [AllowAny]
    pagination_class   = CustomDashboardPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['title_uz', 'title_ru', 'title_en', 'author_uz']

    def get_queryset(self):
        qs = (
            IlmiyTadqiqot.objects
            .filter(is_published=True)
            .select_related('category')
            .prefetch_related('files')
            .order_by('-date', '-created_at')
        )
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(category__slug=cat)
        date_from = self.request.query_params.get('date_from')
        date_to   = self.request.query_params.get('date_to')
        if date_from:
            qs = qs.filter(date__date__gte=date_from)
        if date_to:
            qs = qs.filter(date__date__lte=date_to)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['ilmiy-tadqiqot'], summary="Ilmiy tadqiqot — slug bo'yicha")
class IlmiyTadqiqotDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    serializer_class   = IlmiyTadqiqotSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return (
            IlmiyTadqiqot.objects
            .filter(is_published=True)
            .select_related('category')
            .prefetch_related('files')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['ilmiy-tadqiqot'], summary="Ilmiy tadqiqot — ID bo'yicha")
class IlmiyTadqiqotDetailByIdAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    serializer_class   = IlmiyTadqiqotSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            IlmiyTadqiqot.objects
            .filter(is_published=True)
            .select_related('category')
            .prefetch_related('files')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


class IlmiyTadqiqotRecordViewAPIView(RecordViewAPIView):
    model_class = IlmiyTadqiqot
