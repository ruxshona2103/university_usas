from django.urls import path

from .views import (
    ContractPriceListAPIView,
    ServiceVehicleListAPIView,
    IlmiyFaoliyatListAPIView,
    IlmiyFaoliyatDetailAPIView,
)

urlpatterns = [
    path('activities/contract-prices/', ContractPriceListAPIView.as_view(),    name='contract-prices'),
    path('activities/vehicles/',        ServiceVehicleListAPIView.as_view(),   name='service-vehicles'),
    path('activities/ilmiy-faoliyat/',  IlmiyFaoliyatListAPIView.as_view(),   name='ilmiy-faoliyat-list'),
    path('activities/ilmiy-faoliyat/<int:pk>/', IlmiyFaoliyatDetailAPIView.as_view(), name='ilmiy-faoliyat-detail'),
]
