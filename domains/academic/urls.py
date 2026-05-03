from django.urls import path

from .views import (
    AcademyStatListAPIView, AcademyDetailPageAPIView,
    FakultetKafedraListAPIView, FakultetKafedraDetailAPIView,
    HuzuridagiTashkilotListAPIView, HuzuridagiTashkilotDetailAPIView,
    JamoatTashkilotlarListAPIView, JamoatTashkilotDetailAPIView,
    AkademiyaKengashiListAPIView, AkademiyaKengashiDetailAPIView,
    TashkiliyTuzilmaListAPIView, TashkiliyTuzilmaDetailAPIView,
    FakultetKafedraRecordViewAPIView,
)

urlpatterns = [
    path('academic/stats/',                                    AcademyStatListAPIView.as_view(),          name='academy-stats'),
    path('academic/detail/',                                   AcademyDetailPageAPIView.as_view(),         name='academy-detail'),
    path('academic/fakultet-kafedralar/',                      FakultetKafedraListAPIView.as_view(),       name='fakultet-kafedra-list'),
    path('academic/fakultet-kafedralar/<slug:slug>/view/',     FakultetKafedraRecordViewAPIView.as_view(), name='fakultet-kafedra-record-view'),
    path('academic/fakultet-kafedralar/<slug:slug>/',          FakultetKafedraDetailAPIView.as_view(),     name='fakultet-kafedra-detail'),
    path('academic/huzuridagi-tashkilotlar/',                  HuzuridagiTashkilotListAPIView.as_view(),   name='huzuridagi-tashkilot-list'),
    path('academic/huzuridagi-tashkilotlar/<slug:slug>/',      HuzuridagiTashkilotDetailAPIView.as_view(), name='huzuridagi-tashkilot-detail'),
    path('academic/jamoat-tashkilotlar/',                      JamoatTashkilotlarListAPIView.as_view(),    name='jamoat-tashkilot-list'),
    path('academic/jamoat-tashkilotlar/<slug:slug>/',          JamoatTashkilotDetailAPIView.as_view(),     name='jamoat-tashkilot-detail'),
    path('academic/kengashlar/',                               AkademiyaKengashiListAPIView.as_view(),     name='akademiya-kengashi-list'),
    path('academic/kengashlar/<slug:slug>/',                   AkademiyaKengashiDetailAPIView.as_view(),   name='akademiya-kengashi-detail'),
    path('academic/tashkiliy-tuzilma/',                        TashkiliyTuzilmaListAPIView.as_view(),      name='tashkiliy-tuzilma-list'),
    path('academic/tashkiliy-tuzilma/<slug:slug>/',            TashkiliyTuzilmaDetailAPIView.as_view(),    name='tashkiliy-tuzilma-detail'),
]
