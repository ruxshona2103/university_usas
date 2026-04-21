from django.urls import path

from .views import ContractPriceListAPIView, ServiceVehicleListAPIView

urlpatterns = [
    path('activities/contract-prices/', ContractPriceListAPIView.as_view(),  name='contract-prices'),
    path('activities/vehicles/',        ServiceVehicleListAPIView.as_view(), name='service-vehicles'),
]
