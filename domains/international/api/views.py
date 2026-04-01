from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from domains.international.models import ForeignProfessorReview
from .serializers import ForeignProfessorReviewSerializer


@extend_schema(tags=['international'], summary="Xorijlik professorlar fikrlari")
class ForeignProfessorReviewListAPIView(generics.ListAPIView):
    """
    Faol xorijlik professor fikrlari.
    ?lang=uz|ru|en
    """
    serializer_class   = ForeignProfessorReviewSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx

    def get_queryset(self):
        return ForeignProfessorReview.objects.filter(is_active=True).order_by('order', '-created_at')
