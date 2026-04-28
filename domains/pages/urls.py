from django.urls import path
from .views import (
    ContactConfigAPIView,
    PresidentQuoteListAPIView,
    SocialLinkListAPIView,
    PartnerListAPIView,
    NavbarListAPIView,
    NavbarPageDetailAPIView,
    HeroVideoListAPIView,
    AboutSocialAPIView,
    AboutAcademyAPIView,
    OrgStructureAPIView,
    OrgSectionListAPIView,
    RekvizitAPIView,
)

urlpatterns = [
    path('contact-info/',     ContactConfigAPIView.as_view(),     name='contact-info'),
    path('rekvizit/',         RekvizitAPIView.as_view(),          name='rekvizit'),
    path('president-quotes/', PresidentQuoteListAPIView.as_view(), name='president-quotes'),
    path('social-links/',     SocialLinkListAPIView.as_view(),     name='social-links'),
    path('partners/',         PartnerListAPIView.as_view(),        name='partner-list'),
    path('hero-video/',       HeroVideoListAPIView.as_view(),       name='hero-video-list'),
    path('aboutsocial/',      AboutSocialAPIView.as_view(),         name='about-social'),
    path('about-academy/',    AboutAcademyAPIView.as_view(),        name='about-academy'),
    path('org-structure/',          OrgStructureAPIView.as_view(),     name='org-structure'),
    path('org-structure/sections/', OrgSectionListAPIView.as_view(),   name='org-section-list'),

    # Navbar
    path('navbar/',
         NavbarListAPIView.as_view(),
         name='navbar-list'),

    path('pages/<slug:page_slug>/',
         NavbarPageDetailAPIView.as_view(),
         name='page-detail'),
]
