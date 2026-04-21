from django.urls import path

from .views import (
    PersonCategoryListAPIView,
    PersonListAPIView,
    PersonDetailAPIView,
    PersonGroupedAPIView,
    PersonCategoryDetailAPIView,
    StudentInfoGroupedAPIView,
    StudentInfoCategoryDetailAPIView,
    OlimpiyaChempionListAPIView,
)

urlpatterns = [
    # ── Kategoriyalar ──────────────────────────────────────────────────────
    path('categories/',                      PersonCategoryListAPIView.as_view(),    name='person-category-list'),
    path('categories/<slug:slug>/',          PersonCategoryDetailAPIView.as_view(),  name='person-category-detail'),

    # ── Shaxslar ───────────────────────────────────────────────────────────
    path('persons/',                         PersonListAPIView.as_view(),            name='person-list'),
    path('persons/grouped/',                 PersonGroupedAPIView.as_view(),         name='person-grouped'),
    path('persons/<uuid:pk>/',               PersonDetailAPIView.as_view(),          name='person-detail'),

    # ── Talaba ma'lumotlari ────────────────────────────────────────────────
    path('student-info/',                    StudentInfoGroupedAPIView.as_view(),    name='student-info-grouped'),
    path('student-info/<slug:slug>/',        StudentInfoCategoryDetailAPIView.as_view(), name='student-info-category-detail'),

    # ── Olimpiya chempionlari ──────────────────────────────────────────────
    path('olimpiya/',                        OlimpiyaChempionListAPIView.as_view(), name='olimpiya-chempion-list'),
]

