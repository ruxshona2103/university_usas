from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from common.cache_mixin import cached_list

from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from domains.tracker.mixins import ViewsCountMixin
from domains.tracker.views import RecordViewAPIView
from domains.activities.models import (
    ContractPrice,
    ServiceVehicle,
    IlmiyFaoliyat,
    IlmiyFaoliyatCategory,
    IlmiyYonalish,
    IlmiyYonalishItem,
    SportStat,
    SportYonalish,
    SportTadbir,
    AxborotVazifa,
    AxborotXodim,
)
from .serializers import (
    ContractPriceSerializer, ServiceVehicleSerializer,
    IlmiyFaoliyatSerializer,
    IlmiyFaoliyatCategorySimpleSerializer,
    IlmiyFaoliyatCategorySerializer,
    IlmiyFaoliyatCategoryTreeSerializer,
    FaoliyatSubcategoryWriteSerializer,
    IlmiyFaoliyatWriteSerializer,
    IlmiyYonalishListSerializer,
    IlmiyYonalishDetailSerializer,
    SportStatSerializer, SportStatWriteSerializer,
    SportYonalishSerializer, SportYonalishWriteSerializer,
    SportTadbirSerializer, SportTadbirWriteSerializer,
    AxborotVazifaSerializer, AxborotVazifaWriteSerializer,
    AxborotXodimSerializer, AxborotXodimWriteSerializer,
)



def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@cached_list(300)
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


@cached_list(300)
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


@cached_list(120)
@extend_schema(tags=['activities'], summary="Sport statistika")
class SportStatListAPIView(generics.ListAPIView):
    serializer_class = SportStatSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return SportStat.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@cached_list(120)
@extend_schema(tags=['activities'], summary="Sport yo'nalishlari")
class SportYonalishListAPIView(generics.ListAPIView):
    serializer_class = SportYonalishSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return SportYonalish.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@cached_list(60)
@extend_schema(tags=['activities'], summary="Yillik sport tadbirlari")
class SportTadbirListAPIView(ViewsCountMixin, generics.ListAPIView):
    serializer_class = SportTadbirSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return SportTadbir.objects.filter(is_active=True).order_by('order', 'event_date')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(
    tags=['activities'],
    summary="API 1 — Asosiy kategoriyalar ro'yxati",
    description="Faqat ildiz (parent=null) kategoriyalar. Sahifa: /faoliyat/oquv  ?lang=uz|ru|en",
)
class IlmiyFaoliyatCategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        lang = _lang(request)
        context = {'request': request, 'lang': lang}

        stats = SportStatSerializer(
            SportStat.objects.filter(is_active=True).order_by('order'),
            many=True,
            context=context,
        ).data
        yonalishlar = SportYonalishSerializer(
            SportYonalish.objects.filter(is_active=True).order_by('order'),
            many=True,
            context=context,
        ).data
        tadbirlar = SportTadbirSerializer(
            SportTadbir.objects.filter(is_active=True).order_by('order', 'event_date'),
            many=True,
            context=context,
        ).data

        return Response({
            'stats': stats,
            'yonalishlar': yonalishlar,
            'tadbirlar': tadbirlar,
        })


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


@cached_list(120)
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
        from django.db.models import Prefetch
        active_items = IlmiyFaoliyat.objects.filter(is_active=True).order_by('order')
        return (
            IlmiyFaoliyatCategory.objects
            .filter(parent=None)
            .prefetch_related(
                Prefetch('items', queryset=active_items),
                Prefetch('children', queryset=IlmiyFaoliyatCategory.objects.order_by('order')),
                Prefetch('children__items', queryset=active_items),
            )
            .order_by('order')
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@cached_list(120)
@extend_schema(
    tags=['activities'],
    summary="Faoliyat ro'yxati | Yangi item qo'shish",
    description=(
        "GET: ?lang=uz|ru|en & ?category=<kategoriya-slug>\n"
        "POST: yangi faoliyat item yaratish (category, title_uz, file maydonlari)"
    ),
)
class IlmiyFaoliyatListAPIView(ViewsCountMixin, generics.ListCreateAPIView):
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
class IlmiyFaoliyatDetailAPIView(ViewsCountMixin, generics.RetrieveUpdateDestroyAPIView):
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


# ──────────────────── Sport Faoliyat sahifasi viewlari ────────────────────────

@extend_schema(tags=['sport-faoliyat'], summary="Statistika kartochkalari (15+, 500+, 50+)")
class SportStatListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        return SportStatWriteSerializer if self.request.method == 'POST' else SportStatSerializer

    def get_queryset(self):
        return SportStat.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['sport-faoliyat'], summary="Statistika — yangilash / o'chirish")
class SportStatDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset           = SportStat.objects.all()

    def get_serializer_class(self):
        return SportStatSerializer if self.request.method == 'GET' else SportStatWriteSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['sport-faoliyat'], summary="Sport yo'nalishlari (Kurash, Suzish, Atletika…)")
class SportYonalishListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        return SportYonalishWriteSerializer if self.request.method == 'POST' else SportYonalishSerializer

    def get_queryset(self):
        return SportYonalish.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['sport-faoliyat'], summary="Sport yo'nalishi — yangilash / o'chirish")
class SportYonalishDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset           = SportYonalish.objects.all()

    def get_serializer_class(self):
        return SportYonalishSerializer if self.request.method == 'GET' else SportYonalishWriteSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['sport-faoliyat'], summary="Yillik tadbirlar ro'yxati")
class SportTadbirListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        return SportTadbirWriteSerializer if self.request.method == 'POST' else SportTadbirSerializer

    def get_queryset(self):
        return SportTadbir.objects.filter(is_active=True).order_by('order', 'event_date')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['sport-faoliyat'], summary="Tadbir — yangilash / o'chirish")
class SportTadbirDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset           = SportTadbir.objects.all()

    def get_serializer_class(self):
        return SportTadbirSerializer if self.request.method == 'GET' else SportTadbirWriteSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


# ──────────────────────────── Axborot xizmati ────────────────────────────

@extend_schema(tags=['axborot-xizmati'], summary="Axborot xizmati vazifalari ro'yxati")
class AxborotVazifaListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        return AxborotVazifaWriteSerializer if self.request.method == 'POST' else AxborotVazifaSerializer

    def get_queryset(self):
        return AxborotVazifa.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['axborot-xizmati'], summary="Axborot vazifasi — yangilash / o'chirish")
class AxborotVazifaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset           = AxborotVazifa.objects.all()

    def get_serializer_class(self):
        return AxborotVazifaSerializer if self.request.method == 'GET' else AxborotVazifaWriteSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['axborot-xizmati'], summary="Axborot xizmati xodimlari ro'yxati")
class AxborotXodimListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        return AxborotXodimWriteSerializer if self.request.method == 'POST' else AxborotXodimSerializer

    def get_queryset(self):
        return AxborotXodim.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['axborot-xizmati'], summary="Axborot xizmati xodimi — yangilash / o'chirish")
class AxborotXodimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset           = AxborotXodim.objects.all()

    def get_serializer_class(self):
        return AxborotXodimSerializer if self.request.method == 'GET' else AxborotXodimWriteSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


# ── RecordView endpoints ───────────────────────────────────────────────────────

class IlmiyFaoliyatRecordViewAPIView(RecordViewAPIView):
    model_class = IlmiyFaoliyat

class SportTadbirRecordViewAPIView(RecordViewAPIView):
    model_class = SportTadbir

class SportYonalishRecordViewAPIView(RecordViewAPIView):
    model_class = SportYonalish


# ── Ilmiy yo'nalish (yangi sodda model) ───────────────────────────────────────

def _yonalish_lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@cached_list(120)
@extend_schema(tags=['ilmiy-yonalish'], summary="Ilmiy yo'nalishlar ro'yxati (parent)")
class IlmiyYonalishListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en — faqat name + slug."""
    serializer_class   = IlmiyYonalishListSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return IlmiyYonalish.objects.filter(is_active=True).order_by('order', 'name_uz')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _yonalish_lang(self.request)
        return ctx


@extend_schema(tags=['ilmiy-yonalish'], summary="Ilmiy yo'nalish detali (slug bo'yicha) — child elementlar bilan")
class IlmiyYonalishDetailAPIView(generics.RetrieveAPIView):
    """?lang=uz|ru|en — parent + items[]."""
    serializer_class   = IlmiyYonalishDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return IlmiyYonalish.objects.filter(is_active=True).prefetch_related('items')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _yonalish_lang(self.request)
        return ctx


# ── Ilmiy kontent (jurnallar, kengash, loyihalar, maktablar) ────────────────

from domains.activities.models import (
    IlmiyKontentSahifa, IlmiyJurnal, IlmiyKengashSeminar,
    IlmiyLoyiha, IlmiyMaktab, IlmiyKategoriya, IlmiyAnjuman,
)
from .serializers import (
    IlmiyKontentSahifaSerializer,
    IlmiyJurnalSerializer,
    IlmiyKengashSeminarSerializer,
    IlmiyLoyihaSerializer,
    IlmiyMaktabSerializer,
    IlmiyAnjumanSerializer,
)


def _ilmiy_lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


def _get_intro(kategoriya, lang, request):
    sahifa = IlmiyKontentSahifa.objects.filter(kategoriya=kategoriya).first()
    if not sahifa:
        return None
    return IlmiyKontentSahifaSerializer(
        sahifa, context={'lang': lang, 'request': request}
    ).data


@extend_schema(tags=['ilmiy-kontent'], summary="Ilmiy jurnallar")
class IlmiyJurnalListAPIView(APIView):
    """?lang=uz|ru|en — sahifa intro + jurnallar ro'yxati."""
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _ilmiy_lang(request)
        ctx = {'lang': lang, 'request': request}
        items = IlmiyJurnal.objects.filter(is_active=True).order_by('order', '-created_at')
        return Response({
            'sahifa': _get_intro(IlmiyKategoriya.JURNALLAR, lang, request),
            'items': IlmiyJurnalSerializer(items, many=True, context=ctx).data,
        })


@extend_schema(tags=['ilmiy-kontent'], summary="Ilmiy kengash va seminar")
class IlmiyKengashSeminarListAPIView(APIView):
    """?lang=uz|ru|en — kengash va seminar ro'yxati (alohida)."""
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _ilmiy_lang(request)
        ctx = {'lang': lang, 'request': request}
        all_items = IlmiyKengashSeminar.objects.filter(is_active=True).order_by('order', '-created_at')
        kengashlar = [i for i in all_items if i.tipi == 'kengash']
        seminarlar = [i for i in all_items if i.tipi == 'seminar']
        return Response({
            'sahifa': _get_intro(IlmiyKategoriya.KENGASH, lang, request),
            'kengashlar': IlmiyKengashSeminarSerializer(kengashlar, many=True, context=ctx).data,
            'seminarlar': IlmiyKengashSeminarSerializer(seminarlar, many=True, context=ctx).data,
        })


@extend_schema(tags=['ilmiy-kontent'], summary="Ilmiy loyihalar")
class IlmiyLoyihaListAPIView(APIView):
    """?lang=uz|ru|en"""
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _ilmiy_lang(request)
        ctx = {'lang': lang, 'request': request}
        items = IlmiyLoyiha.objects.filter(is_active=True).order_by('order', '-created_at')
        return Response({
            'sahifa': _get_intro(IlmiyKategoriya.LOYIHALAR, lang, request),
            'items': IlmiyLoyihaSerializer(items, many=True, context=ctx).data,
        })


@extend_schema(tags=['ilmiy-kontent'], summary="Ilmiy maktablar")
class IlmiyMaktabListAPIView(APIView):
    """?lang=uz|ru|en"""
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _ilmiy_lang(request)
        ctx = {'lang': lang, 'request': request}
        items = IlmiyMaktab.objects.filter(is_active=True).order_by('order', '-created_at')
        return Response({
            'sahifa': _get_intro(IlmiyKategoriya.MAKTABLAR, lang, request),
            'items': IlmiyMaktabSerializer(items, many=True, context=ctx).data,
        })


@extend_schema(tags=['ilmiy-kontent'], summary="Ilmiy anjuman va konferensiyalar")
class IlmiyAnjumanlarListAPIView(APIView):
    """
    ?lang=uz|ru|en
    ?status=upcoming|ongoing|past  — filtrlash (ixtiyoriy)
    ?turi=republic|international|seminar|roundtable|webinar  — filtrlash (ixtiyoriy)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _ilmiy_lang(request)
        ctx = {'lang': lang, 'request': request}
        qs = IlmiyAnjuman.objects.filter(is_active=True).order_by('-date', 'order')

        status = request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)

        turi = request.query_params.get('turi')
        if turi:
            qs = qs.filter(turi=turi)

        return Response({
            'sahifa': {
                'title': {
                    'uz': "Ilmiy anjuman va konferensiyalar",
                    'ru': "Научные конференции и семинары",
                    'en': "Scientific Conferences and Seminars",
                }.get(lang, "Ilmiy anjuman va konferensiyalar"),
                'intro': {
                    'uz': "Akademiyada o'tkazilgan va rejalashtirilgan ilmiy anjumanlar",
                    'ru': "Прошедшие и предстоящие научные мероприятия Академии",
                    'en': "Past and upcoming scientific events of the Academy",
                }.get(lang, ""),
            },
            'items': IlmiyAnjumanSerializer(qs, many=True, context=ctx).data,
        })


# ── Sport natijalari va kalendar ─────────────────────────────────────────────

from domains.activities.models import SportNatija, SportKalendar
from .serializers import SportNatijaSerializer, SportKalendarSerializer


@extend_schema(tags=['sport-faoliyat'], summary="Sport natijalari (medallar jadvali)")
class SportNatijaListAPIView(generics.ListAPIView):
    """
    ?lang=uz|ru|en
    ?bosqich=1|2|magistr|para  — filtrlash uchun
    """
    serializer_class   = SportNatijaSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = SportNatija.objects.order_by('bosqich', 'order')
        bosqich = self.request.query_params.get('bosqich')
        if bosqich:
            qs = qs.filter(bosqich=bosqich)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['sport-faoliyat'], summary="Sport kalendari (rejalashtirilgan tadbirlar)")
class SportKalendarListAPIView(generics.ListAPIView):
    """
    ?lang=uz|ru|en
    ?yil=2026  — yil bo'yicha filtrlash
    """
    serializer_class   = SportKalendarSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        qs = SportKalendar.objects.order_by('-yil', 'order')
        yil = self.request.query_params.get('yil')
        if yil:
            qs = qs.filter(yil=yil)
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx
