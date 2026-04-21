from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from domains.activities.models import ContractPrice, ServiceVehicle, IlmiyFaoliyat
from .serializers import ContractPriceSerializer, ServiceVehicleSerializer, IlmiyFaoliyatSerializer



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


@extend_schema(tags=['activities'], summary="Ilmiy faoliyat ro'yxati")
class IlmiyFaoliyatListAPIView(generics.ListAPIView):
    """
    ?lang=uz|ru|en
    ?category=article|monograph|manual|report|patent|conference|other
    ?year=2024
    """
    serializer_class   = IlmiyFaoliyatSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = IlmiyFaoliyat.objects.filter(is_active=True)
        category = self.request.query_params.get('category')
        year     = self.request.query_params.get('year')
        if category:
            qs = qs.filter(category=category)
        if year:
            qs = qs.filter(year=year)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['activities'], summary="Ilmiy faoliyat — bitta yozuv")
class IlmiyFaoliyatDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = IlmiyFaoliyatSerializer
    permission_classes = [AllowAny]
    queryset           = IlmiyFaoliyat.objects.filter(is_active=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx
