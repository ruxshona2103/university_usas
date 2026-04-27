from django.db import models
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes

from domains.pages.models import (
    ContactConfig, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo,
    AboutSocial, AboutSocialSection, AboutSocialExtraTask,
    OrgNode, Rekvizit,
)
from .serializers import (
    ContactConfigSerializer,
    PresidentQuoteSerializer,
    SocialLinkSerializer,
    NavbarPageSerializer,
    PartnerSerializer,
    HeroVideoSerializer,
    OrgNodeSerializer,
    RekvizitSerializer,
)


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


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


@extend_schema(tags=['pages'], summary="Tashkilot rekvizitlari")
class RekvizitAPIView(generics.RetrieveAPIView):
    """Tashkilot to'liq nomi, qisqartma, email, telefon, manzil (singleton)."""
    serializer_class   = RekvizitSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Rekvizit.get_solo()


@extend_schema(tags=['pages'], summary="Prezident iqtiboSlari")
class PresidentQuoteListAPIView(generics.ListAPIView):
    """Faol prezident iqtiboslari ro'yxati."""
    serializer_class   = PresidentQuoteSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return PresidentQuote.objects.filter(is_active=True)


@extend_schema(tags=['pages'], summary="Ijtimoiy tarmoq havolalari")
class SocialLinkListAPIView(generics.ListAPIView):
    """Faol ijtimoiy tarmoq havolalari."""
    serializer_class   = SocialLinkSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return SocialLink.objects.filter(is_active=True)


@extend_schema(tags=['pages'], summary="Hamkorlar")
class PartnerListAPIView(generics.ListAPIView):
    """Faol hamkorlar ro'yxati."""
    serializer_class   = PartnerSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_queryset(self):
        return Partner.objects.filter(is_active=True)


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
        import traceback
        lang = _lang(request)
        try:
            roots = (
                OrgNode.objects
                .filter(parent=None, is_active=True)
                .prefetch_related(
                    'children__children__children__children',
                )
                .order_by('order', 'name_uz')
            )
            ctx = {'lang': lang, 'request': request}
            data = OrgNodeSerializer(roots, many=True, context=ctx).data
            return Response(data)
        except Exception as e:
            return Response({'error': str(e), 'trace': traceback.format_exc()}, status=500)
