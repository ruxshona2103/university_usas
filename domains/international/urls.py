from django.urls import path
from .views import (
    ForeignProfessorReviewListAPIView,
    PartnerOrganizationListAPIView,
    InternationalPostListAPIView,
)

urlpatterns = [
    path('foreign-reviews/',    ForeignProfessorReviewListAPIView.as_view(), name='foreign-reviews-list'),
    path('partners/',           PartnerOrganizationListAPIView.as_view(),    name='international-partners'),
    path('international-posts/', InternationalPostListAPIView.as_view(),     name='international-posts'),
]
