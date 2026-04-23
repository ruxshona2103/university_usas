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
    path('activities/oquv-faoliyat/',  IlmiyFaoliyatListAPIView.as_view(),   name='oquv-faoliyat-list'),
    path('activities/oquv-faoliyat/<uuid:pk>/', IlmiyFaoliyatDetailAPIView.as_view(), name='oquv-faoliyat-detail'),
]
