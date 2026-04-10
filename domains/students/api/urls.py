from django.urls import path

from .views import PersonCategoryListAPIView, PersonListAPIView, PersonDetailAPIView

urlpatterns = [
    path('categories/', PersonCategoryListAPIView.as_view(), name='person-category-list'),
    path('persons/',    PersonListAPIView.as_view(),         name='person-list'),
    path('persons/<uuid:pk>/', PersonDetailAPIView.as_view(), name='person-detail'),
]