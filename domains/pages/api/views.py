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
    NavbarCategorySerializer,
    NavbarLanguageGroupedSerializer,
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
        serializer = NavbarLanguageGroupedSerializer()
        return Response(serializer.to_representation(categories))


@extend_schema(tags=['navbar'])
class NavbarCategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = NavbarCategorySerializer
    permission_classes = [AllowAny]

    def get_object(self):
        category_slug = self.kwargs.get('category_slug')
        try:
            return (
                NavbarCategory.objects
                .prefetch_related(
                    models.Prefetch(
                        'items',
                        queryset=NavbarSubItem.objects.filter(is_active=True).order_by('order')
                    )
                )
                .get(slug=category_slug, is_active=True)
            )
        except NavbarCategory.DoesNotExist:
            raise NotFound(detail="Bo'lim topilmadi.")


@extend_schema(tags=['navbar'])
class NavbarPageDetailAPIView(generics.RetrieveAPIView):
    serializer_class = NavbarPageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        category_slug = self.kwargs.get('category_slug')
        page_slug = self.kwargs.get('page_slug')
        try:
            return (
                NavbarSubItem.objects
                .select_related('category')
                .get(
                    slug=page_slug,
                    category__slug=category_slug,
                    is_active=True,
                )
            )
        except NavbarSubItem.DoesNotExist:
            raise NotFound(detail="Sahifa topilmadi.")
