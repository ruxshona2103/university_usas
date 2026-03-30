from django.urls import path

from .views import StructureListAPIView, StaffListAPIView, UnitDetailAPIView


urlpatterns = [
	path('structure/', StructureListAPIView.as_view(), name='structure-list'),
	path('units/<slug:slug>/', UnitDetailAPIView.as_view(), name='unit-detail'),
	path('staff/', StaffListAPIView.as_view(), name='staff-list'),
]
