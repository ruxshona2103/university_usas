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
)

urlpatterns = [
    path('activities/contract-prices/',                          ContractPriceListAPIView.as_view(),          name='contract-prices'),
    path('activities/vehicles/',                                 ServiceVehicleListAPIView.as_view(),         name='service-vehicles'),

    # API 1 — asosiy kategoriyalar (parent=null)
    path('activities/faoliyat/categories/',                      IlmiyFaoliyatCategoryListAPIView.as_view(),     name='faoliyat-categories'),

    # API 4 — barcha kategoriyalar + sub-kategoriyalar + fayllar (bir so'rovda)
    path('activities/faoliyat/categories/full/',                 IlmiyFaoliyatCategoryFullListAPIView.as_view(), name='faoliyat-categories-full'),

    # API 2 — kategoriya bolalari (sub-kategoriyalar)
    path('activities/faoliyat/categories/<slug:slug>/children/', IlmiyFaoliyatCategoryChildrenAPIView.as_view(), name='faoliyat-category-children'),

    # API 3 — kategoriya fayllari (leaf items)
    path('activities/faoliyat/categories/<slug:slug>/items/',    IlmiyFaoliyatCategoryItemsAPIView.as_view(),    name='faoliyat-category-items'),

    path('activities/faoliyat/',                                 IlmiyFaoliyatListAPIView.as_view(),          name='faoliyat-list'),
    path('activities/faoliyat/<uuid:pk>/',                       IlmiyFaoliyatDetailAPIView.as_view(),        name='faoliyat-detail'),
]
