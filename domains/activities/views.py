from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from domains.activities.models import ContractPrice, ServiceVehicle, IlmiyFaoliyat, IlmiyFaoliyatCategory
from .serializers import (
    ContractPriceSerializer, ServiceVehicleSerializer,
    IlmiyFaoliyatSerializer,
    IlmiyFaoliyatCategorySimpleSerializer,
    IlmiyFaoliyatCategorySerializer,
)



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


@extend_schema(
    tags=['activities'],
    summary="API 1 — Asosiy kategoriyalar ro'yxati",
    description="Faqat ildiz (parent=null) kategoriyalar. Sahifa: /faoliyat/oquv  ?lang=uz|ru|en",
)
class IlmiyFaoliyatCategoryListAPIView(generics.ListAPIView):
    serializer_class   = IlmiyFaoliyatCategorySimpleSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return (
            IlmiyFaoliyatCategory.objects
            .filter(parent=None)
            .order_by('order')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['activities'],
    summary="API 2 — Kategoriya bolalari (sub-kategoriyalar)",
    description="Berilgan slug bo'yicha to'g'ridan-to'g'ri bolalar. Sahifa: /page/<slug>  ?lang=uz|ru|en",
)
class IlmiyFaoliyatCategoryChildrenAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        parent = get_object_or_404(IlmiyFaoliyatCategory, slug=slug)
        children = IlmiyFaoliyatCategory.objects.filter(parent=parent).order_by('order')
        serializer = IlmiyFaoliyatCategorySimpleSerializer(
            children, many=True, context={'request': request, 'lang': _lang(request)}
        )
        return Response(serializer.data)


@extend_schema(
    tags=['activities'],
    summary="API 3 — Kategoriya fayllari (leaf items)",
    description="Berilgan slug kategoriyasiga tegishli fayllar. Sahifa: /page/<slug> (leaf)  ?lang=uz|ru|en",
)
class IlmiyFaoliyatCategoryItemsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = get_object_or_404(IlmiyFaoliyatCategory, slug=slug)
        items = IlmiyFaoliyat.objects.filter(category=category).order_by('order')
        serializer = IlmiyFaoliyatSerializer(
            items, many=True, context={'request': request, 'lang': _lang(request)}
        )
        return Response(serializer.data)


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
