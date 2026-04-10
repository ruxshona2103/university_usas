from django.urls import path

from .views import AcademyStatListAPIView

urlpatterns = [
    path('academic/stats/', AcademyStatListAPIView.as_view(), name='academy-stats'),
]
