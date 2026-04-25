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
    OrgStructureAPIView,
)

urlpatterns = [
    path('contact-info/',     ContactConfigAPIView.as_view(),     name='contact-info'),
    path('president-quotes/', PresidentQuoteListAPIView.as_view(), name='president-quotes'),
    path('social-links/',     SocialLinkListAPIView.as_view(),     name='social-links'),
    path('partners/',         PartnerListAPIView.as_view(),        name='partner-list'),
    path('hero-video/',       HeroVideoListAPIView.as_view(),       name='hero-video-list'),
    path('aboutsocial/',      AboutSocialAPIView.as_view(),         name='about-social'),
    path('org-structure/',    OrgStructureAPIView.as_view(),        name='org-structure'),

    # Navbar
    path('navbar/',
         NavbarListAPIView.as_view(),
         name='navbar-list'),

    path('pages/<slug:page_slug>/',
         NavbarPageDetailAPIView.as_view(),
         name='page-detail'),
]
