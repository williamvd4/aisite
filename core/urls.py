from django.contrib import admin
from django.urls import path, include
from django.conf import settings # New import
from django.conf.urls.static import static # New import

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
    path("", include('theme_material_kit.urls'))
]

# Add this block to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
