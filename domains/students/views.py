from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.pagination import CustomDashboardPagination
from .models import Person, PersonCategory, StudentInfoCategory, StudentInfo, OlimpiyaChempion, MagistrGroup, Stipendiya
from .serializers import (
    PersonSerializer, PersonCategorySerializer, StudentInfoSerializer,
    PersonCategoryWithPersonsSerializer, StudentInfoCategorySerializer,
    OlimpiyaChempionSerializer, MagistrGroupSerializer, StipendiyaSerializer,
)


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(tags=['people'], summary="Shaxslar kategoriyalari ro'yxati (ierarxik)")
class PersonCategoryListAPIView(generics.ListAPIView):
    """Faqat ildiz kategoriyalar; har birida children[] ichida bola kategoriyalar."""
    serializer_class = PersonCategorySerializer
    pagination_class = None

    def get_queryset(self):
        return (
            PersonCategory.objects
            .filter(parent=None)
            .prefetch_related('children')
            .order_by('order')
        )


@extend_schema(tags=['people'], summary="Shaxslar ro'yxati")
class PersonListAPIView(generics.ListAPIView):
    """
    ?category=rektorat  ?is_head=1  ?search=  ?lang=uz|ru|en
    """
    serializer_class = PersonSerializer
    pagination_class = CustomDashboardPagination
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    search_fields    = ['full_name_uz', 'full_name_ru', 'full_name_en']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        qs = (
            Person.objects
            .filter(is_active=True)
            .select_related('category')
            .prefetch_related('images', 'tabs__tags')
            .order_by('order', '-id')
        )
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        is_head = self.request.query_params.get('is_head')
        if is_head in ('1', 'true', 'yes'):
            qs = qs.filter(is_head=True)

        return qs


@extend_schema(tags=['people'], summary="Shaxs detali")
class PersonDetailAPIView(generics.RetrieveAPIView):
    """Bitta shaxsning to'liq ma'lumoti (tablar, rasmlar bilan)."""
    serializer_class = PersonSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        return (
            Person.objects
            .filter(is_active=True)
            .select_related('category')
            .prefetch_related('images', 'tabs__tags')
        )


@extend_schema(tags=['people'], summary="Shaxslar kategoriya bo'yicha guruhlangan (ierarxik)")
class PersonGroupedAPIView(generics.ListAPIView):
    """
    Faqat ildiz kategoriyalar; har birida children[] va persons[] bilan.
    ?lang=uz|ru|en
    """
    serializer_class = PersonCategoryWithPersonsSerializer
    pagination_class = None

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        return (
            PersonCategory.objects
            .filter(parent=None)
            .prefetch_related('children', 'persons__images', 'persons__tabs__tags')
            .order_by('order')
        )


@extend_schema(tags=['people'], summary="Kategoriya slug bo'yicha shaxslar")
class PersonCategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Bitta PersonCategory va uning barcha aktiv shaxslari.
    /api/persons/categories/<slug>/  ?lang=uz|ru|en
    """
    serializer_class = PersonCategoryWithPersonsSerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        return (
            PersonCategory.objects
            .prefetch_related('persons__images', 'persons__tabs__tags')
        )


@extend_schema(tags=['students'], summary="Talaba ma'lumotlari kategoriya bo'yicha guruhlangan (ierarxik)")
class StudentInfoGroupedAPIView(generics.ListAPIView):
    """
    Faqat ildiz kategoriyalar; har birida children[] va items[] bilan.
    ?lang=uz|ru|en
    """
    serializer_class = StudentInfoCategorySerializer
    pagination_class = None

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        return (
            StudentInfoCategory.objects
            .filter(parent=None)
            .prefetch_related('children', 'items')
            .order_by('order')
        )


@extend_schema(tags=['students'], summary="StudentInfo kategoriya slug bo'yicha")
class StudentInfoCategoryDetailAPIView(generics.RetrieveAPIView):
    """
    Bitta StudentInfoCategory va uning barcha aktiv itemlari.
    /api/student-info/<slug>/  ?lang=uz|ru|en
    """
    serializer_class = StudentInfoCategorySerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        return StudentInfoCategory.objects.prefetch_related('items')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.slug == 'stipendiyalar':
            stipendiya_qs = Stipendiya.objects.filter(is_active=True).order_by('order')
            data['stipendiya_table'] = StipendiyaSerializer(
                stipendiya_qs, many=True, context=self.get_serializer_context()
            ).data
        return Response(data)


@extend_schema(
    tags=['students'],
    summary="Magistratura talabalari ro'yxati (guruh + dissertatsiya + rahbar)",
    description="?year=2025-2026  ?specialty_code=71010301  ?lang=uz|ru|en",
)
class MagistrGroupListAPIView(generics.ListAPIView):
    serializer_class   = MagistrGroupSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        qs = MagistrGroup.objects.filter(is_active=True).prefetch_related('students')
        year             = self.request.query_params.get('year')
        specialty_code   = self.request.query_params.get('specialty_code')
        if year:
            qs = qs.filter(year=year)
        if specialty_code:
            qs = qs.filter(specialty_code=specialty_code)
        return qs.order_by('year', 'order')


@extend_schema(
    tags=['people'],
    summary="Stipendiyalar miqdori jadvali",
    description="Akademiyada tayinlanadigan stipendiyalar ro'yxati. ?lang=uz|ru|en",
)
class StipendiyaListAPIView(generics.ListAPIView):
    serializer_class   = StipendiyaSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return Stipendiya.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['people'], summary="Olimpiya chempionlari ro'yxati")
class OlimpiyaChempionListAPIView(generics.ListAPIView):
    """
    ?yonalish=<sport>   — sport turi bo'yicha filter
    ?guruh=<guruh>      — guruh bo'yicha filter
    """
    serializer_class   = OlimpiyaChempionSerializer
    pagination_class   = None

    def get_queryset(self):
        qs = OlimpiyaChempion.objects.filter(is_active=True)
        yonalish = self.request.query_params.get('yonalish')
        guruh    = self.request.query_params.get('guruh')
        if yonalish:
            qs = qs.filter(yonalish__icontains=yonalish)
        if guruh:
            qs = qs.filter(guruh__icontains=guruh)
        return qs
