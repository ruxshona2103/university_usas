from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from common.pagination import CustomDashboardPagination
from domains.contact.models import FAQ, RectorAppeal
from .serializers import FAQSerializer, FAQCreateSerializer, RectorAppealSerializer


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(tags=['contact'], summary="Savol-javob ro'yxati")
class FAQListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = FAQSerializer
    permission_classes = [AllowAny]
    pagination_class   = CustomDashboardPagination

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        return FAQ.objects.filter(is_published=True).order_by('-vote_count', '-created_at')


@extend_schema(tags=['contact'], summary="Savol yuborish")
class FAQCreateAPIView(generics.CreateAPIView):
    serializer_class   = FAQCreateSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['contact'], summary="Savolga ovoz berish")
class FAQVoteAPIView(APIView):
    """POST /api/faq/{id}/vote/"""
    permission_classes = [AllowAny]

    def post(self, request, pk):
        try:
            faq = FAQ.objects.get(pk=pk, is_published=True)
        except FAQ.DoesNotExist:
            return Response({'detail': 'Topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        FAQ.objects.filter(pk=pk).update(vote_count=faq.vote_count + 1)
        new_count = faq.vote_count + 1
        return Response({'vote_count': new_count, 'likes': new_count})


@extend_schema(tags=['contact'], summary="Rektorga murojaat yuborish")
class RectorAppealCreateAPIView(generics.CreateAPIView):
    serializer_class   = RectorAppealSerializer
    permission_classes = [AllowAny]
