from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from domains.activities.models import ContractPrice, ServiceVehicle, IlmiyFaoliyat, IlmiyFaoliyatCategory
from .serializers import ContractPriceSerializer, ServiceVehicleSerializer, IlmiyFaoliyatSerializer, IlmiyFaoliyatCategorySerializer



def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(tags=['activities'], summary="To'lov-kontrakt narxlari")
class ContractPriceListAPIView(generics.ListAPIView):
    """
    ?lang=uz|ru|en
    ?education_type=bachelor|master
    ?education_form=daytime|evening|distance
    """
    serializer_class   = ContractPriceSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = ContractPrice.objects.filter(is_active=True)
        edu_type = self.request.query_params.get('education_type')
        edu_form = self.request.query_params.get('education_form')
        if edu_type:
            qs = qs.filter(education_type=edu_type)
        if edu_form:
            qs = qs.filter(education_form=edu_form)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['activities'], summary="Xizmat avtomototransport vositalari")
class ServiceVehicleListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = ServiceVehicleSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return ServiceVehicle.objects.filter(is_active=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['activities'], summary="Faoliyat kategoriyalari ro'yxati (ierarxik)")
class IlmiyFaoliyatCategoryListAPIView(generics.ListAPIView):
    """
    ?lang=uz|ru|en
    Faqat ildiz kategoriyalar qaytadi; har birining ichida children[] va items[] bo'ladi.
    """
    serializer_class   = IlmiyFaoliyatCategorySerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return (
            IlmiyFaoliyatCategory.objects
            .filter(parent=None)
            .prefetch_related('children', 'items')
            .order_by('order')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['activities'], summary="Faoliyat kategoriyasi — slug bo'yicha")
class IlmiyFaoliyatCategoryDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en  — kategoriya + children + items"""
    serializer_class   = IlmiyFaoliyatCategorySerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return IlmiyFaoliyatCategory.objects.prefetch_related('children', 'items')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['activities'],
    summary="Faoliyat ro'yxati",
    description="?lang=uz|ru|en  &  ?category=<kategoriya-slug>",
)
class IlmiyFaoliyatListAPIView(generics.ListAPIView):
    serializer_class   = IlmiyFaoliyatSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = IlmiyFaoliyat.objects.all()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['activities'], summary="Faoliyat — bitta yozuv")
class IlmiyFaoliyatDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = IlmiyFaoliyatSerializer
    permission_classes = [AllowAny]
    queryset           = IlmiyFaoliyat.objects.all()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx
