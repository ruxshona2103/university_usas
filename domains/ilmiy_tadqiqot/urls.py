from django.urls import path

from .views import (
    IlmiyTadqiqotCategoryListAPIView,
    IlmiyTadqiqotListAPIView,
    IlmiyTadqiqotDetailAPIView,
    IlmiyTadqiqotDetailByIdAPIView,
    IlmiyTadqiqotRecordViewAPIView,
)

urlpatterns = [
    # Kategoriyalar
    path('ilmiy-tadqiqot/categories/', IlmiyTadqiqotCategoryListAPIView.as_view(), name='ilmiy-tadqiqot-categories'),

    # Ro'yxat
    path('ilmiy-tadqiqot/', IlmiyTadqiqotListAPIView.as_view(), name='ilmiy-tadqiqot-list'),

    # Slug bo'yicha detail
    path('ilmiy-tadqiqot/<slug:slug>/', IlmiyTadqiqotDetailAPIView.as_view(), name='ilmiy-tadqiqot-detail'),

    # UUID bo'yicha detail
    path('ilmiy-tadqiqot/id/<uuid:pk>/', IlmiyTadqiqotDetailByIdAPIView.as_view(), name='ilmiy-tadqiqot-detail-by-id'),

    # Ko'rishlar soni (tracker)
    path('ilmiy-tadqiqot/<uuid:pk>/view/', IlmiyTadqiqotRecordViewAPIView.as_view(), name='ilmiy-tadqiqot-record-view'),
]
