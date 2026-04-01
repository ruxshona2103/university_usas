from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # API sxema
    path('api/schema/', SpectacularAPIView.as_view(),                          name='schema'),
    path('swagger/',    SpectacularSwaggerView.as_view(url_name='schema'),     name='swagger-ui'),
    path('redoc/',      SpectacularRedocView.as_view(url_name='schema'),       name='redoc'),

    # Domenlar
    path('api/', include('domains.pages.api.urls')),
    path('api/', include('domains.academic.api.urls')),
    path('api/', include('domains.news.api.urls')),
    path('api/', include('domains.students.api.urls')),
    path('api/', include('domains.tenders.api.urls')),
    path('api/', include('domains.contact.api.urls')),
    path('api/', include('domains.international.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
