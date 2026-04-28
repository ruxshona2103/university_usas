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
    IlmiyFaoliyatCategoryTreeSerializer,
    FaoliyatSubcategoryWriteSerializer,
    IlmiyFaoliyatWriteSerializer,
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
    summary="API 2 — Kategoriya bolalari (sub-kategoriyalar) | Yangi sub-kategoriya qo'shish",
    description=(
        "GET: berilgan slug bo'yicha sub-kategoriyalar ro'yxati. ?lang=uz|ru|en\n"
        "POST: yangi sub-kategoriya yaratish (title_uz, icon, order, description_uz majburiy/ixtiyoriy)"
    ),
    responses={200: IlmiyFaoliyatCategorySimpleSerializer(many=True)},
)
class IlmiyFaoliyatCategoryChildrenAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FaoliyatSubcategoryWriteSerializer
        return IlmiyFaoliyatCategorySimpleSerializer

    def get_queryset(self):
        parent = get_object_or_404(IlmiyFaoliyatCategory, slug=self.kwargs['slug'])
        return IlmiyFaoliyatCategory.objects.filter(parent=parent).order_by('order')

    def perform_create(self, serializer):
        parent = get_object_or_404(IlmiyFaoliyatCategory, slug=self.kwargs['slug'])
        serializer.save(parent=parent)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['activities'],
    summary="API 3 — Kategoriya fayllari (leaf items)",
    description="Berilgan slug kategoriyasiga tegishli fayllar. Sahifa: /page/<slug> (leaf)  ?lang=uz|ru|en",
    responses={200: IlmiyFaoliyatSerializer(many=True)},
)
class IlmiyFaoliyatCategoryItemsAPIView(generics.ListAPIView):
    serializer_class   = IlmiyFaoliyatSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        category = get_object_or_404(IlmiyFaoliyatCategory, slug=self.kwargs['slug'])
        # Agar kategoriyaning o'z itemlari bo'lsa → o'zini qaytaradi
        # Agar yo'q bo'lsa (root/ota) → bolalari ichidagi itemlarni qaytaradi
        direct_items = IlmiyFaoliyat.objects.filter(category=category)
        if direct_items.exists():
            return direct_items.order_by('order')
        child_ids = IlmiyFaoliyatCategory.objects.filter(parent=category).values_list('id', flat=True)
        return IlmiyFaoliyat.objects.filter(category__in=child_ids).order_by('category__order', 'order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['activities'],
    summary="API 4 — Barcha kategoriyalar (sub-kategoriya + fayllar bilan)",
    description="Bir so'rovda: barcha root kategoriyalar → har birining sub-kategoriyalari → fayllar. ?lang=uz|ru|en",
)
class IlmiyFaoliyatCategoryFullListAPIView(generics.ListAPIView):
    serializer_class   = IlmiyFaoliyatCategoryTreeSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return (
            IlmiyFaoliyatCategory.objects
            .filter(parent=None)
            .prefetch_related('children__items', 'items')
            .order_by('order')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['activities'],
    summary="Faoliyat ro'yxati | Yangi item qo'shish",
    description=(
        "GET: ?lang=uz|ru|en & ?category=<kategoriya-slug>\n"
        "POST: yangi faoliyat item yaratish (category, title_uz, file maydonlari)"
    ),
)
class IlmiyFaoliyatListAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IlmiyFaoliyatWriteSerializer
        return IlmiyFaoliyatSerializer

    def get_queryset(self):
        qs = IlmiyFaoliyat.objects.filter(is_active=True)
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['activities'], summary="Faoliyat — bitta yozuv (o'qish / yangilash / o'chirish)")
class IlmiyFaoliyatDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """?lang=uz|ru|en"""
    permission_classes = [AllowAny]
    queryset           = IlmiyFaoliyat.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IlmiyFaoliyatSerializer
        return IlmiyFaoliyatWriteSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['activities'],
    summary="Sub-kategoriya — yangilash / o'chirish",
    description="PUT / PATCH / DELETE — sub-kategoriyani uuid bo'yicha tahrirlash yoki o'chirish",
)
class FaoliyatSubcategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset           = IlmiyFaoliyatCategory.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IlmiyFaoliyatCategorySimpleSerializer
        return FaoliyatSubcategoryWriteSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx
