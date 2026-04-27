from django.urls import path

from .views import AxborotSectionListAPIView, AxborotPersonListAPIView

urlpatterns = [
    path('axborot/sections/', AxborotSectionListAPIView.as_view(), name='axborot-sections'),
    path('axborot/persons/',  AxborotPersonListAPIView.as_view(),  name='axborot-persons'),
]
