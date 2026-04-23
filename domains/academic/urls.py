from django.urls import path

from .views import AcademyStatListAPIView, AcademyDetailPageAPIView

urlpatterns = [
    path('academic/stats/',  AcademyStatListAPIView.as_view(),   name='academy-stats'),
    path('academic/detail/', AcademyDetailPageAPIView.as_view(), name='academy-detail'),
]
