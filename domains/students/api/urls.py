from django.urls import path 
from .views import PersonListAPIView, PersonCategoryListAPIView

urlpatterns = [
    path('categories/', PersonCategoryListAPIView.as_view(), name='person-category-list'),
    path('persons/', PersonListAPIView.as_view(), name='person-list'),

]