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
    MagistrGroupListAPIView,
    MagistrTalabaListAPIView,
    MagistrTalabaDetailAPIView,
    MagistrTalabaRecordViewAPIView,
    MagistrPageAPIView,
    StipendiyaListAPIView,
    PersonRecordViewAPIView,
)

urlpatterns = [
    # ── Kategoriyalar ──────────────────────────────────────────────────────
    path('categories/',                      PersonCategoryListAPIView.as_view(),    name='person-category-list'),
    path('categories/<slug:slug>/',          PersonCategoryDetailAPIView.as_view(),  name='person-category-detail'),

    # ── Shaxslar ───────────────────────────────────────────────────────────
    path('persons/',                         PersonListAPIView.as_view(),            name='person-list'),
    path('persons/grouped/',                 PersonGroupedAPIView.as_view(),         name='person-grouped'),
    path('persons/<uuid:pk>/view/',          PersonRecordViewAPIView.as_view(),      name='person-record-view'),
    path('persons/<uuid:pk>/',               PersonDetailAPIView.as_view(),          name='person-detail'),

    # ── Talaba ma'lumotlari ────────────────────────────────────────────────
    path('student-info/',                    StudentInfoGroupedAPIView.as_view(),    name='student-info-grouped'),
    path('student-info/<slug:slug>/',        StudentInfoCategoryDetailAPIView.as_view(), name='student-info-category-detail'),

    # ── Olimpiya chempionlari ──────────────────────────────────────────────
    path('olimpiya/',                        OlimpiyaChempionListAPIView.as_view(), name='olimpiya-chempion-list'),

    # ── Magistratura guruhlari (eski) ──────────────────────────────────────
    path('magistr-students/',               MagistrGroupListAPIView.as_view(),    name='magistr-students'),

    # ── Magistratura talabalari (yangi — Person FK bilan) ──────────────────
    path('magistr-talabalar/page/',            MagistrPageAPIView.as_view(),             name='magistr-page'),
    path('magistr-talabalar/<uuid:pk>/view/', MagistrTalabaRecordViewAPIView.as_view(), name='magistr-talaba-record-view'),
    path('magistr-talabalar/<uuid:pk>/',      MagistrTalabaDetailAPIView.as_view(),     name='magistr-talaba-detail'),
    path('magistr-talabalar/',                MagistrTalabaListAPIView.as_view(),       name='magistr-talaba-list'),

    # ── Stipendiyalar ──────────────────────────────────────────────────────────
    path('stipendiya/',                     StipendiyaListAPIView.as_view(),      name='stipendiya-list'),
]
