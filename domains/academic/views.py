from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.http import Http404
from django.db.models import F, Window, Case, When, IntegerField
from django.db.models.functions import RowNumber

from domains.tracker.mixins import ViewsCountMixin
from domains.tracker.views import RecordViewAPIView
from domains.academic.models import AcademyStat, AcademyDetailPage, FakultetKafedra, HuzuridagiTashkilot

from .serializers import (
    AcademyStatSerializer, AcademyDetailPageSerializer,
    FakultetKafedraListSerializer, FakultetKafedraDetailSerializer,
    HuzuridagiTashkilotSerializer, JamoatTashkilotSerializer, JamoatTashkilotDetailSerializer,
)


@extend_schema(tags=['academic'], summary="Akademiya raqamlarda — statistikalar")
class AcademyStatListAPIView(generics.ListAPIView):
    serializer_class   = AcademyStatSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return AcademyStat.objects.filter(is_active=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['academic'], summary="Akademiya raqamlarda — batafsil sahifa")
class AcademyDetailPageAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        lang = request.query_params.get('lang', 'uz')
        if lang not in ('uz', 'ru', 'en'):
            lang = 'uz'
        obj = AcademyDetailPage.objects.first()
        if not obj:
            return Response({})
        return Response(AcademyDetailPageSerializer(obj, context={'lang': lang, 'request': request}).data)


@extend_schema(tags=['academic'], summary="Fakultetlar va kafedralar ro'yxati")
class FakultetKafedraListAPIView(generics.ListAPIView):
    serializer_class   = FakultetKafedraListSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = FakultetKafedra.objects.filter(is_active=True)
        type_filter = self.request.query_params.get('type')
        if type_filter in ('tashkilot', 'fakultet', 'kafedra'):
            qs = qs.filter(type=type_filter)
        # Some environments may contain legacy duplicate slugs.
        # Keep only the first row per slug to avoid duplicate API items.
        return (
            qs.annotate(
                _slug_rank=Window(
                    expression=RowNumber(),
                    partition_by=[F('slug')],
                    order_by=[F('order').asc(), F('created_at').asc(), F('id').asc()],
                ),
                _type_order=Case(
                    When(type='tashkilot', then=0),
                    When(type='fakultet',  then=1),
                    When(type='kafedra',   then=2),
                    default=3,
                    output_field=IntegerField(),
                ),
            )
            .filter(_slug_rank=1)
            .order_by('_type_order', 'order', 'name_uz')
        )


@extend_schema(tags=['academic'], summary="Fakultet/Kafedra batafsil ma'lumoti")
class FakultetKafedraDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    serializer_class   = FakultetKafedraDetailSerializer
    permission_classes = [AllowAny]
    queryset           = FakultetKafedra.objects.filter(is_active=True).prefetch_related('publications', 'xodimlar__person', 'rasmlar')
    lookup_field       = 'slug'

    def get_object(self):
        slug = self.kwargs.get(self.lookup_field)
        obj = (
            self.get_queryset()
            .filter(slug=slug)
            .order_by('order', 'created_at', 'id')
            .first()
        )
        if not obj:
            raise Http404
        return obj


@extend_schema(tags=['academic'], summary="Akademiya huzuridagi tashkilotlar ro'yxati")
class HuzuridagiTashkilotListAPIView(ViewsCountMixin, generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = HuzuridagiTashkilotSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return HuzuridagiTashkilot.objects.filter(is_active=True, org_type='akademiya')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['academic'], summary="Jamoat tashkilotlari ro'yxati")
class JamoatTashkilotlarListAPIView(ViewsCountMixin, generics.ListAPIView):
    """?lang=uz|ru|en — Yoshlar ittifoqi, Kasaba uyushmasi, Xotin-qizlar kengashi"""
    serializer_class   = JamoatTashkilotSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return HuzuridagiTashkilot.objects.filter(is_active=True, org_type='jamoat').order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['academic'], summary="Jamoat tashkiloti batafsil ma'lumoti")
class JamoatTashkilotDetailAPIView(generics.RetrieveAPIView):
    serializer_class   = JamoatTashkilotDetailSerializer
    permission_classes = [AllowAny]
    queryset           = HuzuridagiTashkilot.objects.filter(is_active=True, org_type='jamoat').select_related('person')
    lookup_field       = 'slug'

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


# ── RecordView endpoints ───────────────────────────────────────────────────────

class FakultetKafedraRecordViewAPIView(RecordViewAPIView):
    model_class  = FakultetKafedra
    pk_url_kwarg = 'slug'

    def get_target_object(self):
        slug = self.kwargs.get('slug')
        obj = FakultetKafedra.objects.filter(slug=slug, is_active=True).order_by('order', 'created_at').first()
        if not obj:
            raise FakultetKafedra.DoesNotExist
        return obj
