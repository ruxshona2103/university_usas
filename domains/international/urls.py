from django.urls import path
from .views import (
    ForeignProfessorReviewListAPIView,
    PartnerOrganizationListAPIView,
    InternationalPostListAPIView,
    InternationalRatingListAPIView,
    InternationalRatingDetailAPIView,
)

urlpatterns = [
    path('foreign-reviews/',                   ForeignProfessorReviewListAPIView.as_view(),  name='foreign-reviews-list'),
    path('partner-organizations/',             PartnerOrganizationListAPIView.as_view(),     name='international-partners'),
    path('international-posts/',               InternationalPostListAPIView.as_view(),       name='international-posts'),
    path('international-ratings/',             InternationalRatingListAPIView.as_view(),     name='international-ratings-list'),
    path('international-ratings/<slug:slug>/', InternationalRatingDetailAPIView.as_view(),   name='international-ratings-detail'),
]
