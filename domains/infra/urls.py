from django.urls import path

from .views import SportMajmuaListAPIView, SportMajmuaDetailAPIView, SharoitListAPIView, SportMajmuaRecordViewAPIView

urlpatterns = [
    path('infra/sport-majmua/<slug:slug>/view/', SportMajmuaRecordViewAPIView.as_view(), name='sport-majmua-record-view'),
    path('infra/sport-majmua/',                  SportMajmuaListAPIView.as_view(),       name='sport-majmua-list'),
    path('infra/sport-majmua/<slug:slug>/',       SportMajmuaDetailAPIView.as_view(),     name='sport-majmua-detail'),
    path('infra/sharoitlar/',                     SharoitListAPIView.as_view(),           name='sharoit-list'),
]
