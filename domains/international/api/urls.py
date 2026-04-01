from django.urls import path
from .views import ForeignProfessorReviewListAPIView

urlpatterns = [
    path('foreign-reviews/', ForeignProfessorReviewListAPIView.as_view(), name='foreign-reviews-list'),
]
