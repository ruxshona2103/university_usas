from django.urls import path

from .views import TenderAnnouncementListAPIView

urlpatterns = [
    path('tenders/', TenderAnnouncementListAPIView.as_view(), name='tenders-list'),
]
