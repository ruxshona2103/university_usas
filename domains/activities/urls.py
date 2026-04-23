from django.urls import path

from .views import (
    ContractPriceListAPIView,
    ServiceVehicleListAPIView,
    IlmiyFaoliyatCategoryListAPIView,
    IlmiyFaoliyatListAPIView,
    IlmiyFaoliyatDetailAPIView,
)

urlpatterns = [
    path('activities/contract-prices/',      ContractPriceListAPIView.as_view(),         name='contract-prices'),
    path('activities/vehicles/',             ServiceVehicleListAPIView.as_view(),        name='service-vehicles'),
    path('activities/faoliyat/categories/',  IlmiyFaoliyatCategoryListAPIView.as_view(), name='faoliyat-categories'),
    path('activities/faoliyat/',             IlmiyFaoliyatListAPIView.as_view(),         name='faoliyat-list'),
    path('activities/faoliyat/<uuid:pk>/',   IlmiyFaoliyatDetailAPIView.as_view(),       name='faoliyat-detail'),
]
