from django.urls import path

from .views import StaffListAPIView, StaffDetailAPIView

urlpatterns = [
    path('staff/',       StaffListAPIView.as_view(),   name='staff-list'),
    path('staff/<uuid:pk>/', StaffDetailAPIView.as_view(), name='staff-detail'),
]
