from django.db import models
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from domains.pages.models import (
    ContactConfig, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo,
)
from .serializers import (
    ContactConfigSerializer,
    PresidentQuoteSerializer,
    SocialLinkSerializer,
    NavbarPageSerializer,
    PartnerSerializer,
    HeroVideoSerializer,
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
                    url = item.redirect_url if item.page_type == NavbarSubItem.PageType.REDIRECT else f'/page/{item.slug}'
                    children.append({
                        'id':    str(item.id),
                        'name':  getattr(item, f'name_{lang}') or item.name_uz,
                        'slug':  item.slug,
                        'url':   url,
                        'order': item.order,
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
                    'staff',
                    'contentblock_items__images',
                    'contentblock_items__tags',
                    'linkblock_items',
                    'information_items__images',
                    'foreign_reviews',
                )
                .get(slug=slug, is_active=True)
            )
        except NavbarSubItem.DoesNotExist:
            raise NotFound(detail="Sahifa topilmadi.")
