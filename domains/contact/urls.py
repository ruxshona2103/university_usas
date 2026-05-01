from django.urls import path
from .views import (
    FAQListAPIView, FAQCreateAPIView, FAQVoteAPIView,
    RectorAppealCreateAPIView, RectorAppealExtraFieldListAPIView,
    QabulRaqamiListAPIView, ContactMessageCreateAPIView,
)

urlpatterns = [
    path('faq/',                        FAQListAPIView.as_view(),                    name='faq-list'),
    path('faq/submit/',                 FAQCreateAPIView.as_view(),                  name='faq-create'),
    path('faq/<uuid:pk>/vote/',         FAQVoteAPIView.as_view(),                    name='faq-vote'),
    path('rector-appeal/extra-fields/', RectorAppealExtraFieldListAPIView.as_view(), name='rector-appeal-extra-fields'),
    path('rector-appeal/',              RectorAppealCreateAPIView.as_view(),          name='rector-appeal'),
    path('contact/',                    ContactMessageCreateAPIView.as_view(),        name='contact-message'),
    path('qabul-raqamlari/',            QabulRaqamiListAPIView.as_view(),            name='qabul-raqamlari'),
]
