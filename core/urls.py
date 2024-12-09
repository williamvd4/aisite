"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
    path("", include('theme_material_kit.urls'))
]
