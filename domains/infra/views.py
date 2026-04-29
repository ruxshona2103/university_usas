from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from domains.tracker.mixins import ViewsCountMixin
from domains.tracker.views import RecordViewAPIView
from .models import SportMajmua, Sharoit
from .serializers import SportMajmuaSerializer, SportMajmuaListSerializer, SharoitSerializer


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(
    tags=['infra'],
    summary="Sport majmualari ro'yxati",
    description="?lang=uz|ru|en",
)
class SportMajmuaListAPIView(ViewsCountMixin, generics.ListAPIView):
    serializer_class   = SportMajmuaListSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return SportMajmua.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['infra'],
    summary="Sport majmuasi pasporti (slug bo'yicha)",
    description="Barcha texnik ko'rsatkichlar, sport turlari va tadbirlar. ?lang=uz|ru|en",
)
class SportMajmuaDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    serializer_class   = SportMajmuaSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return SportMajmua.objects.filter(is_active=True).prefetch_related(
            'images', 'stats', 'sport_types', 'events'
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


_CATEGORY_MAP = {
    'sport':  'sport',
    'talim':  'talim',
    "ta'lim": 'talim',
}


@extend_schema(
    tags=['infra'],
    summary="Yaratilgan sharoit va imkoniyatlar",
    description="?category=sport|talim  Filtrsiz — ikkala bo'lim alohida qaytadi. ?lang=uz|ru|en",
)
class SharoitListAPIView(generics.ListAPIView):
    serializer_class   = SharoitSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = Sharoit.objects.filter(is_active=True)
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(category=_CATEGORY_MAP.get(cat.lower(), cat))
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def list(self, request, *args, **kwargs):
        ctx       = self.get_serializer_context()
        cat_param = request.query_params.get('category')
        resolved  = _CATEGORY_MAP.get(cat_param.lower(), cat_param) if cat_param else None
        base_qs   = Sharoit.objects.filter(is_active=True)

        if resolved:
            items = SharoitSerializer(
                base_qs.filter(category=resolved), many=True, context=ctx
            ).data
            return Response({'category': resolved, 'items': items})

        return Response({
            'sport': SharoitSerializer(
                base_qs.filter(category='sport'), many=True, context=ctx
            ).data,
            'talim': SharoitSerializer(
                base_qs.filter(category='talim'), many=True, context=ctx
            ).data,
        })


# ── RecordView endpoints ───────────────────────────────────────────────────────

class SportMajmuaRecordViewAPIView(RecordViewAPIView):
    model_class  = SportMajmua
    pk_url_kwarg = 'slug'

    def get_target_object(self):
        slug = self.kwargs.get('slug')
        return SportMajmua.objects.get(slug=slug)
