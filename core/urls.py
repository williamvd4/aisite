from django.contrib import admin
from django.urls import path, include
from django.conf import settings # New import
from django.conf.urls.static import static # New import
from home import views as home_views # Add this line

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_views.welcome, name='welcome'), # Change this line
    path("home/", include('home.urls')), # Add this line to include home.urls under /home/
    path("", include('theme_material_kit.urls')),
]

# Add this block to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
