from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from domains.tracker.mixins import ViewsCountMixin
from domains.tracker.views import RecordViewAPIView
from domains.international.models import (
    ForeignProfessorReview, PartnerOrganization, PartnerPageConfig,
    InternationalPost, InternationalRating,
    InternationalDeptConfig, MemorandumStat, AkademikAlmashinuv,
    XalqaroReytingBolim, XorijlikProfessor,
)
from .serializers import (
    ForeignProfessorReviewSerializer, PartnerOrganizationSerializer, PartnerPageConfigSerializer,
    InternationalPostSerializer, InternationalRatingSerializer,
    InternationalDeptConfigSerializer, MemorandumStatSerializer,
    AkademikAlmashinuvSerializer, XalqaroReytingBolimSerializer,
    XorijlikProfessorSerializer,
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
class InternationalRatingListAPIView(ViewsCountMixin, generics.ListAPIView):
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
class InternationalRatingDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
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
class InternationalPostListAPIView(ViewsCountMixin, generics.ListAPIView):
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


@extend_schema(tags=['international'], summary="Xalqaro bo'lim xabari — ID bo'yicha")
class InternationalPostDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = InternationalPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return InternationalPost.objects.filter(is_active=True).prefetch_related('images')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


# ── RecordView endpoints ───────────────────────────────────────────────────────

class InternationalPostRecordViewAPIView(RecordViewAPIView):
    model_class = InternationalPost

class InternationalRatingRecordViewAPIView(RecordViewAPIView):
    model_class = InternationalRating


@extend_schema(tags=['international'], summary="Akademik almashinuv — bo'limlar va rasmlar")
class AkademikAlmashinuvListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = AkademikAlmashinuvSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return AkademikAlmashinuv.objects.filter(is_active=True).prefetch_related('rasmlar').order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['international'], summary="Xalqaro reyting bo'limlari (sport va professor)")
class XalqaroReytingBolimListAPIView(generics.ListAPIView):
    """
    ?type=sport|professor  — filterlash uchun
    ?lang=uz|ru|en
    """
    serializer_class   = XalqaroReytingBolimSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = XalqaroReytingBolim.objects.filter(is_active=True).order_by('bolim_type', 'order')
        bolim_type = self.request.query_params.get('type')
        if bolim_type in ('sport', 'professor'):
            qs = qs.filter(bolim_type=bolim_type)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        ctx = self.get_serializer_context()
        bolim_type = request.query_params.get('type')
        if bolim_type:
            return Response(XalqaroReytingBolimSerializer(qs, many=True, context=ctx).data)
        sport = qs.filter(bolim_type='sport')
        professor = qs.filter(bolim_type='professor')
        return Response({
            'sport':     XalqaroReytingBolimSerializer(sport, many=True, context=ctx).data,
            'professor': XalqaroReytingBolimSerializer(professor, many=True, context=ctx).data,
        })


from drf_spectacular.utils import extend_schema

@extend_schema(tags=['international'], summary="Xorijlik professor-o'qituvchilar ro'yxati")
class XorijlikProfessorListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = XorijlikProfessorSerializer
    permission_classes = [AllowAny]
    pagination_class   = None
    queryset           = XorijlikProfessor.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(tags=['international'], summary="Xorijlik professor-o'qituvchi detail")
class XorijlikProfessorDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = XorijlikProfessorSerializer
    permission_classes = [AllowAny]
    queryset           = XorijlikProfessor.objects.filter(is_active=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx
