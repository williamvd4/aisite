from django.urls import path

from . import views

app_name = 'your_app'  # replace with your app name

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]


from django.shortcuts import render
from django.views.generic import TemplateView

def IndexView(request):
    return render(request, 'index.html')

def AboutView(request):
    return render(request, 'about.html')

def ContactView(request):
    return render(request, 'contact.html')

def LoginView(request):
    return render(request, 'login.html')

def LogoutView(request):
    return render(request, 'logout.html')
