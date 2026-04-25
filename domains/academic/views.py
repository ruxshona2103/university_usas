from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from domains.academic.models import AcademyStat, AcademyDetailPage, FakultetKafedra
from .serializers import (
    AcademyStatSerializer, AcademyDetailPageSerializer,
    FakultetKafedraListSerializer, FakultetKafedraDetailSerializer,
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
        if type_filter in ('fakultet', 'kafedra'):
            qs = qs.filter(type=type_filter)
        return qs


@extend_schema(tags=['academic'], summary="Fakultet/Kafedra batafsil ma'lumoti")
class FakultetKafedraDetailAPIView(generics.RetrieveAPIView):
    serializer_class   = FakultetKafedraDetailSerializer
    permission_classes = [AllowAny]
    queryset           = FakultetKafedra.objects.filter(is_active=True).prefetch_related('publications')
    lookup_field       = 'slug'
