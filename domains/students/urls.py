from django.urls import path

from .views import (
    PersonCategoryListAPIView,
    PersonListAPIView,
    PersonDetailAPIView,
    PersonGroupedAPIView,
    StudentInfoGroupedAPIView,
)

urlpatterns = [
    path('categories/',          PersonCategoryListAPIView.as_view(), name='person-category-list'),
    path('persons/',             PersonListAPIView.as_view(),         name='person-list'),
    path('persons/grouped/',     PersonGroupedAPIView.as_view(),      name='person-grouped'),
    path('persons/<uuid:pk>/',   PersonDetailAPIView.as_view(),       name='person-detail'),
    path('student-info/',        StudentInfoGroupedAPIView.as_view(), name='student-info-grouped'),
]
