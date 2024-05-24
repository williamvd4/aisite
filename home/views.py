from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.

def homepage(request):
    """Homepage view"""
    # Page from the theme 
    context = {'message': 'Welcome to our website!'}
    return render(request, 'pages/index.html', context)

def page_not_found(request, exception):
    """404 error handler view"""
    return render(request, 'errors/404.html', status=404)


handler404 = 'yourapp.views.page_not_found'
