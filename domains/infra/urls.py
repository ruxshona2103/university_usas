from django.urls import path

from .views import SportMajmuaListAPIView, SportMajmuaDetailAPIView

urlpatterns = [
    path('infra/sport-majmua/',             SportMajmuaListAPIView.as_view(),   name='sport-majmua-list'),
    path('infra/sport-majmua/<slug:slug>/', SportMajmuaDetailAPIView.as_view(), name='sport-majmua-detail'),
]
