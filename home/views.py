# home/views.py

import os
import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone

from .models import Document, ExtractedContent, StandardsMetadata, Standard, ProcessingJob
from .utils.document_processing.pipeline import DocumentProcessingPipeline

logger = logging.getLogger(__name__)

# Name of the app
# Create your views here.

def home(request):
    """Homepage view"""
    context = {
        'message': 'Welcome to our document processing system!',
        'recent_documents': Document.objects.all().order_by('-created_at')[:5]
    }
    return render(request, 'pages/index.html', context)

def document_upload(request):
    """Document upload view"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        document_type = request.POST.get('document_type')
        uploaded_file = request.FILES.get('file')
        
        if not all([title, document_type, uploaded_file]):
            messages.error(request, 'Please fill all required fields')
            return redirect('document_upload')
        
        # Determine file type
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        file_type_map = {
            '.pdf': 'pdf',
            '.docx': 'docx',
            '.doc': 'docx',
            '.txt': 'txt',
            '.html': 'html',
            '.htm': 'html'
        }
        file_type = file_type_map.get(file_extension, 'other')
        
        # Create document
        document = Document.objects.create(
            title=title,
            description=description,
            file=uploaded_file,
            file_type=file_type,
            document_type=document_type
        )
        
        # Create processing job for this document
        ProcessingJob.objects.create(
            document=document,
            status='pending'
        )
        
        messages.success(request, 'Document uploaded successfully. Processing will begin shortly.')
        return redirect('document_detail', document_id=document.id)
    
    return render(request, 'pages/document_upload.html')

def document_detail(request, document_id):
    """Document detail view"""
    document = get_object_or_404(Document, id=document_id)
    
    # Get processing job
    try:
        job = document.processing_jobs.latest('created_at')
    except ProcessingJob.DoesNotExist:
        job = None
    
    # Get extracted content
    extracted_contents = document.extracted_contents.all()
    
    # Get standards if applicable
    standards_metadata = document.standards_metadata.all().first()
    standards = []
    if standards_metadata:
        standards = standards_metadata.standards.all()
    
    context = {
        'document': document,
        'job': job,
        'extracted_contents': extracted_contents,
        'standards_metadata': standards_metadata,
        'standards': standards
    }
    
    return render(request, 'pages/document_detail.html', context)

def documents_list(request):
    """List all documents"""
    documents = Document.objects.all().order_by('-created_at')
    
    context = {
        'documents': documents
    }
    
    return render(request, 'pages/documents_list.html', context)

@csrf_exempt
@require_POST
def process_document(request, document_id):
    """Process a document"""
    document = get_object_or_404(Document, id=document_id)
    
    # Initialize pipeline
    pipeline = DocumentProcessingPipeline()
    
    # Process document in background
    try:
        result = pipeline.process_document(str(document.id))
        
        if result['status'] == 'success':
            messages.success(request, 'Document processed successfully.')
        else:
            messages.error(request, f"Error processing document: {result.get('message', 'Unknown error')}")
        
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        messages.error(request, f"Error processing document: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def standards_list(request):
    """List all standards"""
    standards = Standard.objects.all().select_related('metadata').order_by('metadata__state', 'identifier')
    
    # Group by state and subject
    grouped_standards = {}
    for standard in standards:
        state = standard.metadata.state
        subject = standard.metadata.subject
        
        if state not in grouped_standards:
            grouped_standards[state] = {}
        
        if subject not in grouped_standards[state]:
            grouped_standards[state][subject] = []
        
        grouped_standards[state][subject].append(standard)
    
    context = {
        'grouped_standards': grouped_standards
    }
    
    return render(request, 'pages/standards_list.html', context)

def api_document_content(request, document_id, content_type=None):
    """API endpoint to get document content in JSON format"""
    document = get_object_or_404(Document, id=document_id)
    
    if content_type:
        # Get specific content type
        try:
            content = document.extracted_contents.get(content_type=content_type)
            return JsonResponse(content.content)
        except ExtractedContent.DoesNotExist:
            return JsonResponse({'error': f'Content type {content_type} not found'}, status=404)
    else:
        # Get all content types
        contents = {}
        for content in document.extracted_contents.all():
            contents[content.content_type] = content.content
        
        return JsonResponse(contents)

def page_not_found(request, exception):
    """404 error handler view"""
    return render(request, 'errors/404.html', status=404)

handler404 = 'home.views.page_not_found'