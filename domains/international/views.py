from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from domains.international.models import ForeignProfessorReview, PartnerOrganization, InternationalPost, InternationalRating
from .serializers import (
    ForeignProfessorReviewSerializer, PartnerOrganizationSerializer,
    InternationalPostSerializer, InternationalRatingSerializer,
)


@extend_schema(tags=['international'], summary="Xorijlik professorlar fikrlari")
class ForeignProfessorReviewListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
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


@extend_schema(tags=['international'], summary="Xalqaro hamkor tashkilotlar")
class PartnerOrganizationListAPIView(generics.ListAPIView):
    """
    ?type=foreign|domestic
    ?lang=uz|ru|en
    """
    serializer_class   = PartnerOrganizationSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx

    def get_queryset(self):
        qs = PartnerOrganization.objects.filter(is_active=True)
        partner_type = self.request.query_params.get('type')
        if partner_type:
            qs = qs.filter(partner_type=partner_type)
        return qs


@extend_schema(tags=['international'], summary="Xalqaro reytinglar ro'yxati")
class InternationalRatingListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = InternationalRatingSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return InternationalRating.objects.filter(is_active=True).prefetch_related('images')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['international'], summary="Xalqaro reyting — slug bo'yicha")
class InternationalRatingDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = InternationalRatingSerializer
    permission_classes = [AllowAny]
    queryset           = InternationalRating.objects.filter(is_active=True).prefetch_related('images')
    lookup_field       = 'slug'

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['international'], summary="Xalqaro bo'lim xabarlari (e'lon, yangilik, malaka oshirish)")
class InternationalPostListAPIView(generics.ListAPIView):
    """
    ?type=announcement|news|training
    ?lang=uz|ru|en
    """
    serializer_class   = InternationalPostSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx

    def get_queryset(self):
        qs = InternationalPost.objects.filter(is_active=True).prefetch_related('images')
        post_type = self.request.query_params.get('type')
        if post_type:
            qs = qs.filter(post_type=post_type)
        return qs
