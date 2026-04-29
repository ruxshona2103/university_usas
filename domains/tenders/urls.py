from django.urls import path

from .views import TenderAnnouncementListAPIView, TenderAnnouncementDetailAPIView, TenderRecordViewAPIView

urlpatterns = [
    path('tenders/<uuid:pk>/view/', TenderRecordViewAPIView.as_view(),          name='tender-record-view'),
    path('tenders/<uuid:pk>/',      TenderAnnouncementDetailAPIView.as_view(),  name='tender-detail'),
    path('tenders/',                TenderAnnouncementListAPIView.as_view(),    name='tenders-list'),
]
