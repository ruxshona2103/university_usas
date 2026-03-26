from django.db import models
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from domains.pages.models import ContactConfig, PresidentQuote, SocialLink, NavbarCategory, NavbarSubItem, Partner
from .serializers import (
    ContactConfigSerializer,
    PresidentQuoteSerializer,
    SocialLinkSerializer,
    NavbarPageSerializer,
    PartnerSerializer,
)


@extend_schema(tags=['pages'])
class ContactConfigAPIView(generics.RetrieveAPIView):
    serializer_class = ContactConfigSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return ContactConfig.get_solo()


@extend_schema(tags=['pages'])
class PresidentQuoteListAPIView(generics.ListAPIView):
    serializer_class = PresidentQuoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return PresidentQuote.objects.filter(is_active=True)


@extend_schema(tags=['pages'])
class SocialLinkListAPIView(generics.ListAPIView):
    serializer_class = SocialLinkSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return SocialLink.objects.filter(is_active=True)


@extend_schema(tags=['pages'])
class PartnerListAPIView(generics.ListAPIView):
    serializer_class = PartnerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Partner.objects.filter(is_active=True)


# ----------------------------------------------NAVBAR---------------------------------------------------------
@extend_schema(tags=['navbar'])
class NavbarListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = (
            NavbarCategory.objects
            .filter(is_active=True)
            .prefetch_related(
                models.Prefetch(
                    'items',
                    queryset=NavbarSubItem.objects.filter(is_active=True).order_by('order')
                )
            )
            .order_by('order')
        )
        result = {'uz': [], 'ru': [], 'en': []}
        for lang in ('uz', 'ru', 'en'):
            for cat in categories:
                children = []
                for item in cat.items.all():
                    if item.page_type == NavbarSubItem.PageType.REDIRECT:
                        url = item.redirect_url or ''
                    else:
                        url = f'/page/{item.slug}'
                    children.append({
                        'id':    str(item.id),
                        'name':  getattr(item, f'name_{lang}') or item.name_uz,
                        'slug':  item.slug,
                        'url':   url,
                        'order': item.order,
                    })

                has_children = len(children) > 0
                url = cat.direct_url or f'/page/{cat.slug}'

                cat_entry = {
                    'key':          cat.slug,
                    'slug':         cat.slug,
                    'label':        getattr(cat, f'name_{lang}') or cat.name_uz,
                    'order':        cat.order,
                    'has_children': has_children,
                    'url':          url,
                    'children':     children,
                }
                result[lang].append(cat_entry)
        return Response(result)


@extend_schema(tags=['navbar'])
class NavbarPageDetailAPIView(generics.RetrieveAPIView):
    serializer_class = NavbarPageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        page_slug = self.kwargs.get('page_slug')
        try:
            return (
                NavbarSubItem.objects
                .select_related('category')
                .get(slug=page_slug, is_active=True)
            )
        except NavbarSubItem.DoesNotExist:
            raise NotFound(detail="Sahifa topilmadi.")
