from django.urls import path

from .views import (
    TenderAnnouncementListAPIView, TenderAnnouncementDetailAPIView,
    TenderAnnouncementDetailBySlugAPIView,
    TanlovListAPIView, TanlovDetailAPIView, TanlovDetailBySlugAPIView,
    TenderRecordViewAPIView,
)

urlpatterns = [
    path('tenders/<uuid:pk>/view/',      TenderRecordViewAPIView.as_view(),              name='tender-record-view'),
    path('tenders/slug/<slug:slug>/',    TenderAnnouncementDetailBySlugAPIView.as_view(), name='tender-detail-slug'),
    path('tenders/<uuid:pk>/',           TenderAnnouncementDetailAPIView.as_view(),       name='tender-detail'),
    path('tenders/',                     TenderAnnouncementListAPIView.as_view(),         name='tenders-list'),
    path('tanlovlar/slug/<slug:slug>/',  TanlovDetailBySlugAPIView.as_view(),             name='tanlov-detail-slug'),
    path('tanlovlar/<uuid:pk>/',         TanlovDetailAPIView.as_view(),                   name='tanlov-detail'),
    path('tanlovlar/',                   TanlovListAPIView.as_view(),                     name='tanlov-list'),
]
