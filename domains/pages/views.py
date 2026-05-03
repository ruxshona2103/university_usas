from django.db import models
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes

from common.cache_mixin import cached_list
from domains.pages.models import (
    ContactConfig, ContactLocation, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo,
    AboutSocial, AboutSocialSection, AboutSocialExtraTask,
    AboutAcademy, AboutAcademySection, AboutAcademySectionItem, AboutAcademyProgram, AboutAcademyImage,
    OrgNode, OrgSection, Rekvizit, InteraktivXizmat,
    Markaz,
)
from .serializers import (
    ContactConfigSerializer,
    ContactLocationSerializer,
    PresidentQuoteSerializer,
    SocialLinkSerializer,
    NavbarPageSerializer,
    PartnerSerializer,
    HeroVideoSerializer,
    OrgNodeSerializer,
    OrgSectionSerializer,
    RekvizitSerializer,
    AboutAcademyProgramSerializer,
    InteraktivXizmatSerializer,
    MarkazListSerializer,
    MarkazDetailSerializer,
)
from domains.tracker.mixins import ViewsCountMixin
from domains.tracker.views import RecordViewAPIView


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


def _abs_url(request, field):
    if not field:
        return None
    try:
        return request.build_absolute_uri(field.url) if request else field.url
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Site-wide endpoints
# ──────────────────────────────────────────────────────────────────────────────

@extend_schema(tags=['pages'], summary="Aloqa ma'lumotlari")
class ContactConfigAPIView(generics.RetrieveAPIView):
    """Yagona aloqa konfiguratsiyasi (singleton)."""
    serializer_class   = ContactConfigSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return ContactConfig.get_solo()


@cached_list(300)
@extend_schema(
    tags=['pages'],
    summary="Aloqa joylari ro'yxati (Bosh ofis, Qabul komissiyasi...)",
    description="?lang=uz|ru|en",
)
class ContactLocationListAPIView(generics.ListAPIView):
    serializer_class   = ContactLocationSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return ContactLocation.objects.filter(is_active=True).order_by('order')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx


@extend_schema(tags=['pages'], summary="Tashkilot rekvizitlari")
class RekvizitAPIView(generics.RetrieveAPIView):
    """Tashkilot to'liq nomi, qisqartma, email, telefon, manzil (singleton)."""
    serializer_class   = RekvizitSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Rekvizit.get_solo()


@cached_list(300)
@extend_schema(tags=['pages'], summary="Prezident iqtiboSlari")
class PresidentQuoteListAPIView(generics.ListAPIView):
    """Faol prezident iqtiboslari ro'yxati."""
    serializer_class   = PresidentQuoteSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return PresidentQuote.objects.filter(is_active=True)


@cached_list(300)
@extend_schema(tags=['pages'], summary="Ijtimoiy tarmoq havolalari")
class SocialLinkListAPIView(generics.ListAPIView):
    """Faol ijtimoiy tarmoq havolalari."""
    serializer_class   = SocialLinkSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return SocialLink.objects.filter(is_active=True)


@cached_list(300)
@extend_schema(tags=['pages'], summary="Hamkorlar")
class PartnerListAPIView(generics.ListAPIView):
    """Faol hamkorlar ro'yxati."""
    serializer_class   = PartnerSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return Partner.objects.filter(is_active=True)


@cached_list(300)
@extend_schema(tags=['pages'], summary="Hero videolar")
class HeroVideoListAPIView(generics.ListAPIView):
    """Bosh sahifa hero video ro'yxati."""
    serializer_class   = HeroVideoSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return HeroVideo.objects.filter(is_active=True)


# ──────────────────────────────────────────────────────────────────────────────
# Navbar tree
# ──────────────────────────────────────────────────────────────────────────────

@extend_schema(tags=['navbar'], summary="Navbar daraxti (uz/ru/en)")
class NavbarListAPIView(APIView):
    """
    To'liq navbar tuzilmasi uchta tilda.
    Javob: { uz: [...], ru: [...], en: [...] }
    """
    permission_classes = [AllowAny]

    def get(self, request):
        categories = (
            NavbarCategory.objects
            .filter(is_active=True)
            .prefetch_related(
                models.Prefetch(
                    'items',
                    queryset=NavbarSubItem.objects.filter(is_active=True).order_by('order'),
                )
            )
            .order_by('order')
        )
        result = {'uz': [], 'ru': [], 'en': []}
        for lang in ('uz', 'ru', 'en'):
            for cat in categories:
                children = []
                for item in cat.items.all():
                    children.append({
                        'id':           str(item.id),
                        'name':         getattr(item, f'name_{lang}') or item.name_uz,
                        'slug':         item.slug,
                        'url':          item.direct_url or f'/page/{item.slug}',
                        'page_type':    item.page_type,
                        'redirect_url': item.redirect_url or None,
                        'order':        item.order,
                    })
                result[lang].append({
                    'key':          cat.slug,
                    'slug':         cat.slug,
                    'label':        getattr(cat, f'name_{lang}') or cat.name_uz,
                    'order':        cat.order,
                    'has_children': bool(children),
                    'url':          cat.direct_url or f'/page/{cat.slug}',
                    'children':     children,
                })
        return Response(result)


# ──────────────────────────────────────────────────────────────────────────────
# Universal page detail
# ──────────────────────────────────────────────────────────────────────────────

@extend_schema(tags=['navbar'], summary="Sahifa kontenti (slug bo'yicha)")
class NavbarPageDetailAPIView(generics.RetrieveAPIView):
    """
    /api/pages/{slug}/ — universal endpoint.
    NavbarSubItem ga bog'liq barcha kontent qaytariladi:
    staff, content_blocks, link_blocks, information, foreign_reviews.
    ?lang=uz|ru|en (default: uz)
    """
    serializer_class   = NavbarPageSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_object(self):
        slug = self.kwargs.get('page_slug')
        try:
            return (
                NavbarSubItem.objects
                .select_related('category')
                .prefetch_related(
                    'contentblock_items__images',
                    'contentblock_items__tags',
                    'linkblock_items',
                )
                .get(slug=slug, is_active=True)
            )
        except NavbarSubItem.DoesNotExist:
            raise NotFound(detail="Sahifa topilmadi.")


# ──────────────────────────────────────────────────────────────────────────────
# About Social — Axborot xizmati
# ──────────────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=['pages'],
    summary="Axborot xizmati vazifalari va funksiyalari",
    parameters=[
        OpenApiParameter(
            name='lang', type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Til: uz | ru | en (default: uz)",
            required=False,
        )
    ],
)
class AboutSocialAPIView(APIView):
    """
    /api/aboutsocial/
    Axborot xizmatining asosiy vazifalari va funksiyalari sahifasi.
    Javob: { title, section_5: {title, items}, section_6: {title, items}, extra_tasks: [...] }
    """
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _lang(request)
        solo = AboutSocial.get_solo()

        sections = (
            AboutSocialSection.objects
            .filter(about_social=solo)
            .prefetch_related('items')
        )
        extra_tasks = AboutSocialExtraTask.objects.filter(about_social=solo)

        result = {
            'title': getattr(solo, f'title_{lang}') or solo.title_uz,
        }
        for section in sections:
            items = [
                getattr(item, f'text_{lang}') or item.text_uz
                for item in section.items.all()
            ]
            result[section.key] = {
                'title': getattr(section, f'title_{lang}') or section.title_uz,
                'items': items,
            }
        result['extra_tasks'] = [
            getattr(task, f'text_{lang}') or task.text_uz
            for task in extra_tasks
        ]
        return Response(result)


# ──────────────────────────────────────────────────────────────────────────────
# About Academy — Akademiya haqida
# ──────────────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=['pages'],
    summary="Akademiya haqida",
    parameters=[
        OpenApiParameter(
            name='lang', type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Til: uz | ru | en (default: uz)",
            required=False,
        )
    ],
)
class AboutAcademyAPIView(APIView):
    """
    /api/about-academy/
    Akademiya haqida to'liq ma'lumot:
    tavsif, bo'limlar (maqsad, vazifalar, tizim, ...), ta'lim dasturlari.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _lang(request)
        solo = AboutAcademy.get_solo()

        sections = (
            AboutAcademySection.objects
            .filter(about=solo)
            .prefetch_related('items')
        )
        programs = AboutAcademyProgram.objects.filter(about=solo)

        result = {
            'logo_url':   _abs_url(request, solo.logo),
            'image_url':  _abs_url(request, solo.image),
            'description': getattr(solo, f'description_{lang}') or solo.description_uz,
            'sections': {},
        }

        for section in sections:
            items = [
                getattr(item, f'text_{lang}') or item.text_uz
                for item in section.items.all()
            ]
            result['sections'][section.key] = {
                'title': getattr(section, f'title_{lang}') or section.title_uz,
                'items': items,
            }

        ctx = {'lang': lang, 'request': request}
        result['programs'] = {
            'bachelor': AboutAcademyProgramSerializer(
                programs.filter(program_type='bachelor'), many=True, context=ctx
            ).data,
            'master': AboutAcademyProgramSerializer(
                programs.filter(program_type='master'), many=True, context=ctx
            ).data,
        }

        gallery = AboutAcademyImage.objects.filter(about=solo, is_active=True)
        result['images'] = [
            {
                'id':         str(img.pk),
                'image_url':  _abs_url(request, img.image),
                'caption':    getattr(img, f'caption_{lang}') or img.caption_uz,
                'order':      img.order,
            }
            for img in gallery
        ]

        return Response(result)


# ──────────────────────────────────────────────────────────────────────────────
# Universitet hayoti — Gallery rasmlari
# ──────────────────────────────────────────────────────────────────────────────

@cached_list(300)
@extend_schema(
    tags=['pages'],
    summary="Universitet hayoti — gallery rasmlari",
    parameters=[
        OpenApiParameter('lang', OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Til: uz | ru | en (default: uz)'),
    ],
)
class UniversitetHayotiGalleryAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_class(self):
        return None

    def list(self, request, *args, **kwargs):
        lang    = _lang(request)
        solo    = AboutAcademy.get_solo()
        gallery = AboutAcademyImage.objects.filter(about=solo, is_active=True).order_by('order')
        data = [
            {
                'id':        str(img.pk),
                'image_url': _abs_url(request, img.image),
                'caption':   getattr(img, f'caption_{lang}') or img.caption_uz or '',
                'order':     img.order,
            }
            for img in gallery
        ]
        return Response(data)


# ──────────────────────────────────────────────────────────────────────────────
# Org Structure — Tashkiliy tuzilma
# ──────────────────────────────────────────────────────────────────────────────

_LANG_PARAM_ORG = OpenApiParameter(
    name='lang', type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    description='Til: uz | ru | en (default: uz)',
    required=False,
)


@extend_schema(
    tags=['pages'],
    summary="Tashkiliy tuzilma daraxti",
    parameters=[_LANG_PARAM_ORG],
)
class OrgStructureAPIView(APIView):
    """
    /api/org-structure/
    To'liq tashkiliy tuzilma daraxti.
    Faqat ildiz tugunlar qaytariladi; har birida children[] ichida bola tugunlar.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _lang(request)
        roots = (
            OrgNode.objects
            .filter(parent=None, is_active=True)
            .prefetch_related('children__children__children__children')
            .order_by('order', 'title_uz')
        )
        ctx = {'lang': lang, 'request': request}
        data = OrgNodeSerializer(roots, many=True, context=ctx).data
        return Response(data)


@extend_schema(
    tags=['pages'],
    summary="Tashkiliy tuzilma — sektsiyalar (frontend karta ko'rinishi)",
)
class OrgSectionListAPIView(APIView):
    """
    /api/org-structure/sections/
    Frontend uchun: har bir sektsiya o'z card-larini qaytaradi.
    ?lang=uz|ru|en
    """
    permission_classes = [AllowAny]

    def get(self, request):
        lang = _lang(request)
        sections = (
            OrgSection.objects
            .filter(is_active=True)
            .prefetch_related('nodes')
            .order_by('order')
        )
        ctx = {'lang': lang, 'request': request}
        data = OrgSectionSerializer(sections, many=True, context=ctx).data
        return Response(data)


@cached_list(300)
@extend_schema(tags=['pages'], summary="Interaktiv xizmatlar ro'yxati")
class InteraktivXizmatListAPIView(generics.ListAPIView):
    """?lang=uz|ru|en"""
    serializer_class   = InteraktivXizmatSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return InteraktivXizmat.objects.filter(is_active=True)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


# ──────────────────────────────────────────────────────────────────────────────
# Markazlar
# ──────────────────────────────────────────────────────────────────────────────

@cached_list(120)
@extend_schema(
    tags=['pages'],
    summary="Markazlar ro'yxati",
    parameters=[
        OpenApiParameter('lang', OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Til: uz | ru | en', required=False),
    ],
)
class MarkazListAPIView(ViewsCountMixin, generics.ListAPIView):
    """?lang=uz|ru|en — barcha markazlar (sub-bo'limlarsiz)."""
    serializer_class   = MarkazListSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return Markaz.objects.filter(is_active=True).prefetch_related('sub_bolimlar')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


@extend_schema(
    tags=['pages'],
    summary="Markaz detali (slug bo'yicha)",
    parameters=[
        OpenApiParameter('lang', OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Til: uz | ru | en', required=False),
    ],
)
class MarkazDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
    """Markaz + sub-bo'limlari bilan. ?lang=uz|ru|en"""
    serializer_class   = MarkazDetailSerializer
    permission_classes = [AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return Markaz.objects.filter(is_active=True).prefetch_related('sub_bolimlar')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        lang = self.request.query_params.get('lang', 'uz')
        ctx['lang'] = lang if lang in ('uz', 'ru', 'en') else 'uz'
        return ctx


# ──────────────────────────────────────────────────────────────────────────────
# Me'yoriy hujjatlar — faqat fayllar
# ──────────────────────────────────────────────────────────────────────────────

@extend_schema(
    tags=['pages'],
    summary="Me'yoriy hujjatlar fayllari",
    parameters=[
        OpenApiParameter('lang', OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description='Til: uz | ru | en', required=False),
        OpenApiParameter('page_slug', OpenApiTypes.STR, OpenApiParameter.QUERY,
                         description="Sahifa slug (default: academy-regulations)", required=False),
    ],
)
class MeyoriyHujjatDownloadAPIView(APIView):
    """
    /api/meyoriy-hujjatlar/<id>/download/
    Faylni backend orqali yuklab beradi — ImageKit 403 muammosini hal qiladi.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        import requests as req
        from django.http import HttpResponse
        from domains.pages.models import LinkBlock

        try:
            obj = LinkBlock.objects.get(id=pk, is_active=True)
        except LinkBlock.DoesNotExist:
            return Response({'detail': 'Topilmadi'}, status=404)

        url = None
        if obj.document_file:
            try:
                url = obj.document_file.url
            except Exception:
                pass
        if not url and obj.link:
            url = obj.link

        if not url:
            return Response({'detail': 'Fayl mavjud emas'}, status=404)

        try:
            resp = req.get(url, timeout=30, stream=True)
            resp.raise_for_status()
        except Exception:
            return Response({'detail': 'Fayl yuklanmadi'}, status=502)

        filename = url.split('/')[-1].split('?')[0]
        content_type = resp.headers.get('Content-Type', 'application/octet-stream')
        response = HttpResponse(resp.content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class MeyoriyHujjatlarAPIView(APIView):
    """
    /api/meyoriy-hujjatlar/?page_slug=academy-regulations
    Sahifadagi file-list bloklar → faqat fayl URL ro'yxati.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        from domains.pages.models import LinkBlock
        lang      = _lang(request)
        page_slug = request.query_params.get('page_slug', 'academy-regulations')

        try:
            page = NavbarSubItem.objects.get(slug=page_slug, is_active=True)
        except NavbarSubItem.DoesNotExist:
            return Response([])

        qs = (
            page.linkblock_items
            .filter(is_active=True, block_type='file-list')
            .order_by('order', 'created_at')
        )

        result = []
        for lb in qs:
            file_url = None
            if lb.document_file:
                try:
                    file_url = request.build_absolute_uri(lb.document_file.url)
                except Exception:
                    pass
            if not file_url and lb.link:
                file_url = lb.link
            download_url = request.build_absolute_uri(f'/api/meyoriy-hujjatlar/{lb.id}/download/')
            result.append({
                'id':           str(lb.id),
                'title':        getattr(lb, f'title_{lang}') or lb.title_uz,
                'file_url':     file_url,
                'download_url': download_url,
                'order':        lb.order,
            })

        return Response(result)


class MarkazRecordViewAPIView(RecordViewAPIView):
    model_class  = Markaz
    pk_url_kwarg = 'slug'

    def get_target_object(self):
        slug = self.kwargs.get('slug')
        return Markaz.objects.get(slug=slug, is_active=True)
