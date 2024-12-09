from django.urls import path
from home import views
from .views import frontend_view

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
