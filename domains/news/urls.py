from django.urls import path

from .views import (
    NewsCategoryListAPIView, NewsCategoryDetailAPIView,
    NewsListAPIView, NewsDetailAPIView, NewsDetailByIdAPIView,
    EventListAPIView, EventDetailAPIView, EventDetailByIdAPIView,
    BlogListAPIView, BlogDetailAPIView, BlogDetailByIdAPIView,
    InformationContentListAPIView,
)

urlpatterns = [
    path('news/categories/',            NewsCategoryListAPIView.as_view(),    name='news-categories'),
    path('news/categories/<slug:slug>/', NewsCategoryDetailAPIView.as_view(), name='news-category-detail'),
    path('news/<uuid:pk>/',             NewsDetailByIdAPIView.as_view(),      name='news-detail-id'),
    path('news/<slug:slug>/',           NewsDetailAPIView.as_view(),          name='news-detail'),
    path('news/',                       NewsListAPIView.as_view(),            name='news-list'),
    path('events/<uuid:pk>/',           EventDetailByIdAPIView.as_view(),     name='event-detail-id'),
    path('events/<slug:slug>/',         EventDetailAPIView.as_view(),         name='event-detail'),
    path('events/',                     EventListAPIView.as_view(),           name='events-list'),
    path('blogs/<uuid:pk>/',            BlogDetailByIdAPIView.as_view(),      name='blog-detail-id'),
    path('blogs/<slug:slug>/',          BlogDetailAPIView.as_view(),          name='blog-detail'),
    path('blogs/',                      BlogListAPIView.as_view(),            name='blogs-list'),
    path('information/',                InformationContentListAPIView.as_view(), name='information-list'),
]
