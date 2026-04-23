from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.views import APIView
from domains.academic.models import AcademyStat, AcademyDetailPage
from .serializers import AcademyStatSerializer, AcademyDetailPageSerializer


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
    """?lang=uz|ru|en — yagona yozuv qaytaradi"""
    permission_classes = [AllowAny]

    def get(self, request):
        lang = request.query_params.get('lang', 'uz')
        if lang not in ('uz', 'ru', 'en'):
            lang = 'uz'
        obj = AcademyDetailPage.objects.first()
        if not obj:
            return Response({})
        serializer = AcademyDetailPageSerializer(obj, context={'lang': lang, 'request': request})
        return Response(serializer.data)
