from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, filters

from common.pagination import CustomDashboardPagination
from ..models import Person, PersonCategory
from .serializers import PersonSerializer, PersonCategorySerializer


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(tags=['people'], summary="Shaxslar kategoriyalari ro'yxati")
class PersonCategoryListAPIView(generics.ListAPIView):
    """
    Barcha kategoriyalar.
    Admin o'zi qo'shgan: Rektorat, Faxrlarimiz, Bitiruvchilar...
    """
    serializer_class = PersonCategorySerializer
    queryset         = PersonCategory.objects.all().order_by('order')
    pagination_class = None


@extend_schema(tags=['people'], summary="Shaxslar ro'yxati")
class PersonListAPIView(generics.ListAPIView):
    """
    Faol shaxslar ro'yxati.
    ?category=rektorat    → faqat rektorat
    ?category=faxrlarimiz → faqat faxrlarimiz
    ?is_head=1            → bo'lim boshliqlar
    ?search=              → ism bo'yicha qidiruv
    ?lang=uz|ru|en
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
