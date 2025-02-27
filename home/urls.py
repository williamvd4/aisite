from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('documents/', views.documents_list, name='documents_list'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<uuid:document_id>/', views.document_detail, name='document_detail'),
    path('documents/<uuid:document_id>/process/', views.process_document, name='process_document'),
    path('standards/', views.standards_list, name='standards_list'),
    path('api/documents/<uuid:document_id>/content/', views.api_document_content, name='api_document_content'),
    path('api/documents/<uuid:document_id>/content/<str:content_type>/', views.api_document_content, name='api_document_content_type'),
]