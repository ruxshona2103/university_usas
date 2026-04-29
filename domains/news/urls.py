from django.urls import path

from .views import (
    NewsCategoryListAPIView, NewsCategoryDetailAPIView,
    NewsListAPIView, NewsDetailAPIView, NewsDetailByIdAPIView,
    EventListAPIView, EventDetailAPIView, EventDetailByIdAPIView,
    BlogListAPIView, BlogDetailAPIView, BlogDetailByIdAPIView,
    KorrupsiyaListAPIView, KorrupsiyaDetailAPIView, KorrupsiyaDetailByIdAPIView,
    ElonListAPIView, ElonDetailAPIView,
    InformationContentListAPIView,
    NewsRecordViewAPIView, EventRecordViewAPIView, BlogRecordViewAPIView,
    KorrupsiyaRecordViewAPIView, ElonRecordViewAPIView,
)

urlpatterns = [
    path('news/categories/',            NewsCategoryListAPIView.as_view(),    name='news-categories'),
    path('news/categories/<slug:slug>/', NewsCategoryDetailAPIView.as_view(), name='news-category-detail'),
    path('news/<uuid:pk>/view/',        NewsRecordViewAPIView.as_view(),      name='news-record-view'),
    path('news/<uuid:pk>/',             NewsDetailByIdAPIView.as_view(),      name='news-detail-id'),
    path('news/<slug:slug>/',           NewsDetailAPIView.as_view(),          name='news-detail'),
    path('news/',                       NewsListAPIView.as_view(),            name='news-list'),
    path('events/<uuid:pk>/view/',      EventRecordViewAPIView.as_view(),     name='event-record-view'),
    path('events/<uuid:pk>/',           EventDetailByIdAPIView.as_view(),     name='event-detail-id'),
    path('events/<slug:slug>/',         EventDetailAPIView.as_view(),         name='event-detail'),
    path('events/',                     EventListAPIView.as_view(),           name='events-list'),
    path('blogs/<uuid:pk>/view/',       BlogRecordViewAPIView.as_view(),      name='blog-record-view'),
    path('blogs/<uuid:pk>/',            BlogDetailByIdAPIView.as_view(),      name='blog-detail-id'),
    path('blogs/<slug:slug>/',          BlogDetailAPIView.as_view(),          name='blog-detail'),
    path('blogs/',                      BlogListAPIView.as_view(),            name='blogs-list'),
    path('korrupsiya/<uuid:pk>/view/',  KorrupsiyaRecordViewAPIView.as_view(), name='korrupsiya-record-view'),
    path('korrupsiya/<uuid:pk>/',       KorrupsiyaDetailByIdAPIView.as_view(), name='korrupsiya-detail-id'),
    path('korrupsiya/<slug:slug>/',     KorrupsiyaDetailAPIView.as_view(),    name='korrupsiya-detail'),
    path('korrupsiya/',                 KorrupsiyaListAPIView.as_view(),      name='korrupsiya-list'),
    path('elon/<uuid:pk>/view/',        ElonRecordViewAPIView.as_view(),      name='elon-record-view'),
    path('elon/<uuid:pk>/',             ElonDetailAPIView.as_view(),          name='elon-detail'),
    path('elon/',                       ElonListAPIView.as_view(),            name='elon-list'),
    path('information/',                InformationContentListAPIView.as_view(), name='information-list'),
]
