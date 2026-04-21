from django.urls import path
from .views import FAQListAPIView, FAQCreateAPIView, FAQVoteAPIView, RectorAppealCreateAPIView

urlpatterns = [
    path('faq/',                FAQListAPIView.as_view(),            name='faq-list'),
    path('faq/submit/',         FAQCreateAPIView.as_view(),          name='faq-create'),
    path('faq/<uuid:pk>/vote/', FAQVoteAPIView.as_view(),            name='faq-vote'),
    path('rector-appeal/',      RectorAppealCreateAPIView.as_view(), name='rector-appeal'),
]
