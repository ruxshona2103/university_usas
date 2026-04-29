from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from domains.international.models import (
    ForeignProfessorReview, PartnerOrganization, PartnerPageConfig,
    InternationalPost, InternationalRating,
    InternationalDeptConfig, MemorandumStat,
)
from .serializers import (
    ForeignProfessorReviewSerializer, PartnerOrganizationSerializer, PartnerPageConfigSerializer,
    InternationalPostSerializer, InternationalRatingSerializer,
    InternationalDeptConfigSerializer, MemorandumStatSerializer,
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
    ?category=xalqaro|mahalliy  (yoki ?type=foreign|domestic)
    ?lang=uz|ru|en
    Filter qilinmasa — ikkala kategoriya guruhlanib qaytadi
    """
    serializer_class   = PartnerOrganizationSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    # category param → partner_type mapping
    _CATEGORY_MAP = {
        'xalqaro':  'foreign',
        'mahalliy': 'domestic',
        'foreign':  'foreign',
        'domestic': 'domestic',
    }

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx

    def _resolve_type(self):
        raw = (
            self.request.query_params.get('category') or
            self.request.query_params.get('type')
        )
        return self._CATEGORY_MAP.get(raw) if raw else None

    def get_queryset(self):
        qs = PartnerOrganization.objects.filter(is_active=True)
        partner_type = self._resolve_type()
        if partner_type:
            qs = qs.filter(partner_type=partner_type)
        return qs

    def list(self, request, *args, **kwargs):
        ctx          = self.get_serializer_context()
        config       = PartnerPageConfig.load()
        partner_type = self._resolve_type()
        base_qs      = PartnerOrganization.objects.filter(is_active=True)

        if partner_type:
            # Bitta kategoriya so'raldi — tekis list qaytariladi
            items = PartnerOrganizationSerializer(
                base_qs.filter(partner_type=partner_type), many=True, context=ctx
            ).data
            return Response({
                'title':       PartnerPageConfigSerializer(config, context=ctx).data['title'],
                'description': PartnerPageConfigSerializer(config, context=ctx).data['description'],
                'category':    partner_type,
                'items':       items,
            })

        # Filter yo'q — ikkala guruh alohida qaytariladi
        return Response({
            'title':       PartnerPageConfigSerializer(config, context=ctx).data['title'],
            'description': PartnerPageConfigSerializer(config, context=ctx).data['description'],
            'xalqaro': PartnerOrganizationSerializer(
                base_qs.filter(partner_type='foreign'), many=True, context=ctx
            ).data,
            'mahalliy': PartnerOrganizationSerializer(
                base_qs.filter(partner_type='domestic'), many=True, context=ctx
            ).data,
        })


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


@extend_schema(tags=['international'], summary="Xalqaro hamkorlik bo'limi konfiguratsiyasi")
class InternationalDeptConfigAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = InternationalDeptConfigSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return InternationalDeptConfig.load()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['international'], summary="Memorandumlar statistikasi")
class MemorandumStatListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = MemorandumStatSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return MemorandumStat.objects.all()

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
