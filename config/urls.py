
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importar settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('', include('apps.gestion_flota.urls')),
    path('', include('apps.recordatorios.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
