# yourapp/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Name of the app
# Create your views here.

def home(request):
    """Homepage view"""
    context = {'message': 'Welcome to our website!'}
    return render(request, 'pages/index.html', context)

def page_not_found(request, exception):
    """404 error handler view"""
    return render(request, 'errors/404.html', status=404)

handler404 = 'yourapp.views.page_not_found'
