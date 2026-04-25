from django.urls import path

from .views import (
    AcademyStatListAPIView, AcademyDetailPageAPIView,
    FakultetKafedraListAPIView, FakultetKafedraDetailAPIView,
)

urlpatterns = [
    path('academic/stats/',                          AcademyStatListAPIView.as_view(),      name='academy-stats'),
    path('academic/detail/',                         AcademyDetailPageAPIView.as_view(),    name='academy-detail'),
    path('academic/fakultet-kafedralar/',            FakultetKafedraListAPIView.as_view(),  name='fakultet-kafedra-list'),
    path('academic/fakultet-kafedralar/<slug:slug>/', FakultetKafedraDetailAPIView.as_view(), name='fakultet-kafedra-detail'),
]
