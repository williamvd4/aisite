from django.db import models
from django.utils.timezone import now
import uuid

class Document(models.Model):
    """Model for storing uploaded curriculum documents and standards"""
    DOCUMENT_TYPES = (
        ('curriculum', 'Curriculum Document'),
        ('standards', 'State Standards'),
        ('lesson_plan', 'Lesson Plan'),
        ('other', 'Other')
    )

    FILE_TYPES = (
        ('pdf', 'PDF Document'),
        ('docx', 'Word Document'),
        ('txt', 'Text Document'),
        ('html', 'HTML Document'),
        ('other', 'Other')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class ExtractedContent(models.Model):
    """Model for storing structured content extracted from documents"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='extracted_contents')
    content_type = models.CharField(max_length=100)
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.content_type} from {self.document.title}"

class StandardsMetadata(models.Model):
    """Model for storing metadata about academic standards"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='standards_metadata')
    year_published = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.state} {self.subject} Standards ({self.grade_level})"

class Standard(models.Model):
    """Model for individual academic standards"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metadata = models.ForeignKey(StandardsMetadata, on_delete=models.CASCADE, related_name='standards')
    identifier = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.identifier}: {self.description[:50]}..."

class ProcessingJob(models.Model):
    """Model for tracking document processing jobs"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='processing_jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Processing job for {self.document.title} ({self.status})"