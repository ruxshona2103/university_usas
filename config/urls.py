from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static
from common.translate_view import translate_view

urlpatterns = [
    path('admin/translate/', admin.site.admin_view(translate_view), name='admin_translate'),
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(),                          name='schema'),
    path('swagger/',    SpectacularSwaggerView.as_view(url_name='schema'),     name='swagger-ui'),
    path('redoc/',      SpectacularRedocView.as_view(url_name='schema'),       name='redoc'),

    path('api/', include('domains.pages.urls')),
    path('api/', include('domains.academic.urls')),
    path('api/', include('domains.news.urls')),
    path('api/', include('domains.students.urls')),
    path('api/', include('domains.tenders.urls')),
    path('api/', include('domains.contact.urls')),
    path('api/', include('domains.international.urls')),
    path('api/', include('domains.activities.urls')),
    path('api/', include('domains.axborot.urls')),
    path('api/', include('domains.infra.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
