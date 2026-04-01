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
    """Barcha shaxs kategoriyalari (Faxrli ustozlar, Bitiruvchilar va h.k.)."""
    serializer_class = PersonCategorySerializer
    queryset         = PersonCategory.objects.all().order_by('order')
    pagination_class = None


@extend_schema(tags=['people'], summary="Shaxslar ro'yxati")
class PersonListAPIView(generics.ListAPIView):
    """
    Faol shaxslar ro'yxati.
    ?category=<slug> — kategoriya bo'yicha filter
    ?search= — ism bo'yicha qidiruv
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
            .prefetch_related('tabs__tag')
        )
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs
