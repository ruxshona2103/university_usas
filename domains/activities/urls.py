from django.urls import path

from .views import (
    ContractPriceListAPIView,
    ServiceVehicleListAPIView,
    IlmiyFaoliyatCategoryListAPIView,
    IlmiyFaoliyatCategoryChildrenAPIView,
    IlmiyFaoliyatCategoryItemsAPIView,
    IlmiyFaoliyatCategoryFullListAPIView,
    IlmiyFaoliyatListAPIView,
    IlmiyFaoliyatDetailAPIView,
    FaoliyatSubcategoryDetailAPIView,
    SportStatListCreateAPIView,
    SportStatDetailAPIView,
    SportYonalishListCreateAPIView,
    SportYonalishDetailAPIView,
    SportTadbirListCreateAPIView,
    SportTadbirDetailAPIView,
)

urlpatterns = [
    path('activities/contract-prices/',  ContractPriceListAPIView.as_view(),  name='contract-prices'),
    path('activities/vehicles/',         ServiceVehicleListAPIView.as_view(), name='service-vehicles'),

    # ── Sport faoliyat sahifasi ──────────────────────────────────────────────
    path('activities/sport/stats/',                    SportStatListCreateAPIView.as_view(),    name='sport-stats'),
    path('activities/sport/stats/<uuid:pk>/',          SportStatDetailAPIView.as_view(),        name='sport-stat-detail'),
    path('activities/sport/yonalishlar/',              SportYonalishListCreateAPIView.as_view(), name='sport-yonalishlar'),
    path('activities/sport/yonalishlar/<uuid:pk>/',    SportYonalishDetailAPIView.as_view(),     name='sport-yonalish-detail'),
    path('activities/sport/tadbirlar/',                SportTadbirListCreateAPIView.as_view(),   name='sport-tadbirlar'),
    path('activities/sport/tadbirlar/<uuid:pk>/',      SportTadbirDetailAPIView.as_view(),       name='sport-tadbir-detail'),

    # ── Faoliyat kategoriyalar ───────────────────────────────────────────────
    path('activities/faoliyat/categories/',                      IlmiyFaoliyatCategoryListAPIView.as_view(),     name='faoliyat-categories'),
    path('activities/faoliyat/categories/full/',                 IlmiyFaoliyatCategoryFullListAPIView.as_view(), name='faoliyat-categories-full'),
    path('activities/faoliyat/categories/<slug:slug>/children/', IlmiyFaoliyatCategoryChildrenAPIView.as_view(), name='faoliyat-category-children'),
    path('activities/faoliyat/categories/<slug:slug>/items/',    IlmiyFaoliyatCategoryItemsAPIView.as_view(),    name='faoliyat-category-items'),

    # ── Faoliyat itemlar ─────────────────────────────────────────────────────
    path('activities/faoliyat/',             IlmiyFaoliyatListAPIView.as_view(),         name='faoliyat-list'),
    path('activities/faoliyat/<uuid:pk>/',   IlmiyFaoliyatDetailAPIView.as_view(),       name='faoliyat-detail'),
    path('activities/faoliyat/subcategories/<uuid:pk>/', FaoliyatSubcategoryDetailAPIView.as_view(), name='faoliyat-subcategory-detail'),
]
