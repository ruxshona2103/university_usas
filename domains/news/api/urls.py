from django.urls import path

from .views import NewsListAPIView, EventListAPIView, BlogListAPIView, InformationContentListAPIView

urlpatterns = [
    path('news/',        NewsListAPIView.as_view(),              name='news-list'),
    path('events/',      EventListAPIView.as_view(),             name='events-list'),
    path('blogs/',       BlogListAPIView.as_view(),              name='blogs-list'),
    path('information/', InformationContentListAPIView.as_view(), name='information-list'),
]
