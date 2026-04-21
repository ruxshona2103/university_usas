from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from domains.academic.models import AcademyStat
from .serializers import AcademyStatSerializer


@extend_schema(tags=['academic'], summary="Akademiya raqamlarda")
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
