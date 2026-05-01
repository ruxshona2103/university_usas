from django.urls import path
from .views import (
    QabulBolimListAPIView, QabulBolimDetailAPIView,
    QabulKomissiyaTarkibiListAPIView,
    QabulKuniListAPIView,
    CallCenterListAPIView,
    QabulYangilikListAPIView, QabulYangilikDetailAPIView,
    QabulNarxListAPIView,
    QabulHujjatListAPIView,
    QabulNavbarListAPIView,
)

urlpatterns = [
    # Bo'limlar
    path('qabul/bolimlar/',              QabulBolimListAPIView.as_view(),             name='qabul-bolim-list'),
    path('qabul/bolimlar/<slug:slug>/',  QabulBolimDetailAPIView.as_view(),           name='qabul-bolim-detail'),

    # Komissiya
    path('qabul/komissiya-tarkibi/',     QabulKomissiyaTarkibiListAPIView.as_view(),  name='qabul-komissiya'),

    # Qabul kunlari
    path('qabul/kunlari/',               QabulKuniListAPIView.as_view(),              name='qabul-kunlari'),

    # Call-center
    path('qabul/call-center/',           CallCenterListAPIView.as_view(),             name='qabul-call-center'),

    # Yangiliklar
    path('qabul/yangiliklar/',           QabulYangilikListAPIView.as_view(),          name='qabul-yangilik-list'),
    path('qabul/yangiliklar/<uuid:pk>/', QabulYangilikDetailAPIView.as_view(),        name='qabul-yangilik-detail'),

    # Kontrakt narxlari
    path('qabul/narxlar/',               QabulNarxListAPIView.as_view(),              name='qabul-narxlar'),

    # Hujjatlar
    path('qabul/hujjatlar/',             QabulHujjatListAPIView.as_view(),            name='qabul-hujjatlar'),

    # Navbar
    path('qabul/navbar/',                QabulNavbarListAPIView.as_view(),            name='qabul-navbar'),
]
