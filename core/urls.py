import:  from my_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('home.urls')),
    path("", include('theme_material_kit.urls'))
]
