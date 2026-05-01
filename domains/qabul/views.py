from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter

from common.cache_mixin import cached_list

from .models import (
    QabulBolim, QabulKomissiyaTarkibi, QabulKuni,
    CallCenter, QabulYangilik, QabulNarx, QabulHujjat,
    QabulNavbar,
)
from .serializers import (
    QabulBolimSerializer,
    QabulKomissiyaTarkibiSerializer,
    QabulKuniSerializer,
    CallCenterSerializer,
    QabulYangilikSerializer,
    QabulNarxSerializer,
    QabulHujjatSerializer,
    QabulNavbarSerializer,
)


def _ctx(request):
    lang = request.query_params.get('lang', 'uz')
    if lang not in ('uz', 'ru', 'en'):
        lang = 'uz'
    return {'request': request, 'lang': lang}


# ─────────────── Qabul Bo'limlari ───────────────

@cached_list(120)
@extend_schema(
    tags=['qabul'],
    summary="Qabul bo'limlari ro'yxati (items bilan)",
    parameters=[
        OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en']),
        OpenApiParameter('bolim_type', str, OpenApiParameter.QUERY,
                         description="bakalavr | magistratura | xorijiy | turar_joy | komissiya"),
    ],
)
class QabulBolimListAPIView(generics.ListAPIView):
    serializer_class   = QabulBolimSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = QabulBolim.objects.filter(is_active=True).prefetch_related('items')
        bolim_type = self.request.query_params.get('bolim_type')
        if bolim_type:
            qs = qs.filter(bolim_type=bolim_type)
        return qs

    def get_serializer_context(self):
        return _ctx(self.request)


@extend_schema(
    tags=['qabul'],
    summary="Qabul bo'limi detail (slug bo'yicha)",
    parameters=[OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en'])],
)
class QabulBolimDetailAPIView(generics.RetrieveAPIView):
    serializer_class   = QabulBolimSerializer
    permission_classes = [AllowAny]
    queryset           = QabulBolim.objects.filter(is_active=True).prefetch_related('items')
    lookup_field       = 'slug'

    def get_serializer_context(self):
        return _ctx(self.request)


# ─────────────── Komissiya Tarkibi ───────────────

@cached_list(300)
@extend_schema(
    tags=['qabul'],
    summary="Qabul komissiyasi tarkibi",
    parameters=[OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en'])],
)
class QabulKomissiyaTarkibiListAPIView(generics.ListAPIView):
    serializer_class   = QabulKomissiyaTarkibiSerializer
    permission_classes = [AllowAny]
    queryset           = QabulKomissiyaTarkibi.objects.filter(is_active=True)

    def get_serializer_context(self):
        return _ctx(self.request)


# ─────────────── Qabul Kunlari ───────────────

@cached_list(120)
@extend_schema(
    tags=['qabul'],
    summary="Qabul kunlari jadvali",
    parameters=[
        OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en']),
        OpenApiParameter('qabul_type', str, OpenApiParameter.QUERY,
                         description="bakalavr | magistratura | xorijiy"),
    ],
)
class QabulKuniListAPIView(generics.ListAPIView):
    serializer_class   = QabulKuniSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = QabulKuni.objects.filter(is_active=True)
        qabul_type = self.request.query_params.get('qabul_type')
        if qabul_type:
            qs = qs.filter(qabul_type=qabul_type)
        return qs

    def get_serializer_context(self):
        return _ctx(self.request)


# ─────────────── Call Center ───────────────

@cached_list(300)
@extend_schema(
    tags=['qabul'],
    summary="Call-center raqamlari",
    parameters=[OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en'])],
)
class CallCenterListAPIView(generics.ListAPIView):
    serializer_class   = CallCenterSerializer
    permission_classes = [AllowAny]
    queryset           = CallCenter.objects.filter(is_active=True)

    def get_serializer_context(self):
        return _ctx(self.request)


# ─────────────── Yangiliklar ───────────────

@cached_list(60)
@extend_schema(
    tags=['qabul'],
    summary="Qabul yangiliklari ro'yxati",
    parameters=[OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en'])],
)
class QabulYangilikListAPIView(generics.ListAPIView):
    serializer_class   = QabulYangilikSerializer
    permission_classes = [AllowAny]
    queryset           = QabulYangilik.objects.filter(is_published=True)

    def get_serializer_context(self):
        return _ctx(self.request)


@extend_schema(
    tags=['qabul'],
    summary="Qabul yangiligi detail",
    parameters=[OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en'])],
)
class QabulYangilikDetailAPIView(generics.RetrieveAPIView):
    serializer_class   = QabulYangilikSerializer
    permission_classes = [AllowAny]
    queryset           = QabulYangilik.objects.filter(is_published=True)

    def get_serializer_context(self):
        return _ctx(self.request)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)


# ─────────────── Kontrakt Narxlari ───────────────

@cached_list(300)
@extend_schema(
    tags=['qabul'],
    summary="Kontrakt narxlari",
    parameters=[
        OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en']),
        OpenApiParameter('edu_type', str, OpenApiParameter.QUERY,
                         description="bakalavr | magistratura | xorijiy"),
        OpenApiParameter('year', int, OpenApiParameter.QUERY),
    ],
)
class QabulNarxListAPIView(generics.ListAPIView):
    serializer_class   = QabulNarxSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = QabulNarx.objects.filter(is_active=True)
        edu_type = self.request.query_params.get('edu_type')
        year     = self.request.query_params.get('year')
        if edu_type:
            qs = qs.filter(edu_type=edu_type)
        if year:
            qs = qs.filter(year=year)
        return qs

    def get_serializer_context(self):
        return _ctx(self.request)


# ─────────────── Hujjatlar ───────────────

@cached_list(120)
@extend_schema(
    tags=['qabul'],
    summary="Qabul hujjatlari ro'yxati",
    parameters=[
        OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en']),
        OpenApiParameter('hujjat_type', str, OpenApiParameter.QUERY,
                         description="bakalavr | magistratura | xorijiy | umumiy"),
    ],
)
class QabulHujjatListAPIView(generics.ListAPIView):
    serializer_class   = QabulHujjatSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = QabulHujjat.objects.filter(is_active=True)
        hujjat_type = self.request.query_params.get('hujjat_type')
        if hujjat_type:
            qs = qs.filter(hujjat_type=hujjat_type)
        return qs

    def get_serializer_context(self):
        return _ctx(self.request)


# ─────────────── Qabul Navbar ───────────────

@cached_list(300)
@extend_schema(
    tags=['qabul'],
    summary="Qabul navbar (kategoriyalar va submenu itemlar)",
    parameters=[OpenApiParameter('lang', str, OpenApiParameter.QUERY, enum=['uz', 'ru', 'en'])],
)
class QabulNavbarListAPIView(generics.ListAPIView):
    serializer_class   = QabulNavbarSerializer
    permission_classes = [AllowAny]
    queryset           = QabulNavbar.objects.filter(is_active=True).prefetch_related('items')

    def get_serializer_context(self):
        return _ctx(self.request)
