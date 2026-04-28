from django.urls import path

from .views import AxborotSectionListAPIView, AxborotPersonListAPIView, AxborotXizmatiPageAPIView

urlpatterns = [
    path('axborot/sections/',    AxborotSectionListAPIView.as_view(),  name='axborot-sections'),
    path('axborot/persons/',     AxborotPersonListAPIView.as_view(),   name='axborot-persons'),
    path('axborot/aov-xizmat/',  AxborotXizmatiPageAPIView.as_view(),  name='axborot-aov-xizmat'),
]
