from django.contrib import admin
from .models import Document, ExtractedContent, StandardsMetadata, Standard, ProcessingJob

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'file_type', 'processed', 'created_at')
    list_filter = ('document_type', 'file_type', 'processed')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(ExtractedContent)
class ExtractedContentAdmin(admin.ModelAdmin):
    list_display = ('document', 'content_type', 'created_at')
    list_filter = ('content_type',)
    search_fields = ('document__title', 'content_type')
    date_hierarchy = 'created_at'

@admin.register(StandardsMetadata)
class StandardsMetadataAdmin(admin.ModelAdmin):
    list_display = ('state', 'subject', 'grade_level', 'year_published')
    list_filter = ('state', 'subject', 'year_published')
    search_fields = ('state', 'subject', 'grade_level')
    date_hierarchy = 'created_at'

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'description_truncated', 'metadata')
    list_filter = ('metadata__state', 'metadata__subject')
    search_fields = ('identifier', 'description')
    
    def description_truncated(self, obj):
        if len(obj.description) > 100:
            return obj.description[:100] + '...'
        return obj.description
    description_truncated.short_description = 'Description'

@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ('document', 'status', 'started_at', 'completed_at', 'created_at')
    list_filter = ('status',)
    search_fields = ('document__title', 'error_message')
    date_hierarchy = 'created_at'