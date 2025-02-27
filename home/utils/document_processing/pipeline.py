"""
Document processing pipeline for handling curriculum and standards documents.
"""
import os
import logging
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from django.conf import settings
from django.utils import timezone

from ...models import Document, ExtractedContent, ProcessingJob, StandardsMetadata, Standard
from .processors import get_processor, BaseDocumentProcessor
from .extractors import StandardsExtractor, CurriculumExtractor

logger = logging.getLogger(__name__)

class DocumentProcessingPipeline:
    """Main pipeline for processing curriculum and standards documents"""
    
    def __init__(self):
        self.standards_extractor = StandardsExtractor()
        self.curriculum_extractor = CurriculumExtractor()
    
    def process_document(self, document_id: str) -> Dict[str, Any]:
        """Process a document and store the results"""
        try:
            # Get the document
            document = Document.objects.get(id=document_id)
            
            # Create or get processing job
            job, created = ProcessingJob.objects.get_or_create(
                document=document,
                defaults={'status': 'pending'}
            )
            
            # Update job status
            job.status = 'processing'
            job.started_at = timezone.now()
            job.save()
            
            # Get file path
            file_path = document.file.path
            
            # Get appropriate processor based on file type
            processor = get_processor(document.file_type)
            
            # Process the document
            processing_result = processor.process(file_path)
            
            # Extract specific content based on document type
            extracted_data = self._extract_specific_content(
                document.document_type,
                processing_result['text'],
                processing_result['metadata']
            )
            
            # Store extracted content
            self._store_extracted_content(document, extracted_data)
            
            # Update document and job status
            document.processed = True
            document.save()
            
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()
            
            return {
                'document_id': str(document.id),
                'status': 'success',
                'extracted_data_types': list(extracted_data.keys())
            }
            
        except Document.DoesNotExist:
            logger.error(f"Document with ID {document_id} does not exist")
            return {'status': 'error', 'message': f"Document with ID {document_id} does not exist"}
        
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {str(e)}")
            
            # Update job status
            try:
                job.status = 'failed'
                job.error_message = str(e)
                job.save()
            except:
                pass
            
            return {'status': 'error', 'message': str(e)}
    
    def _extract_specific_content(
        self, 
        document_type: str, 
        text: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract content based on document type"""
        
        results = {}
        
        # Extract basic metadata
        results['metadata'] = metadata
        
        # Extract content specific to document type
        if document_type == 'standards':
            standards_data = self.standards_extractor.extract(text, metadata)
            results['standards'] = standards_data
            
        elif document_type == 'curriculum':
            curriculum_data = self.curriculum_extractor.extract(text, metadata)
            results['curriculum'] = curriculum_data
            
        elif document_type == 'lesson_plan':
            # For lesson plans, extract both curriculum and standards
            curriculum_data = self.curriculum_extractor.extract(text, metadata)
            standards_data = self.standards_extractor.extract(text, metadata)
            
            results['curriculum'] = curriculum_data
            results['standards'] = standards_data
            
        else:  # 'other'
            # For other documents, try both extractors
            curriculum_data = self.curriculum_extractor.extract(text, metadata)
            standards_data = self.standards_extractor.extract(text, metadata)
            
            # Determine which extractor was more effective
            if standards_data['identified_standards'] and len(standards_data['identified_standards']) > 3:
                results['standards'] = standards_data
                
            if curriculum_data['learning_objectives'] and len(curriculum_data['learning_objectives']) > 0:
                results['curriculum'] = curriculum_data
        
        return results
    
    def _store_extracted_content(self, document: Document, extracted_data: Dict[str, Any]) -> None:
        """Store extracted content in the database"""
        
        # Store general extracted content
        for content_type, content in extracted_data.items():
            ExtractedContent.objects.create(
                document=document,
                content_type=content_type,
                content=content
            )
        
        # Store standards if they were extracted
        if 'standards' in extracted_data:
            standards_data = extracted_data['standards']
            
            # Create standards metadata entry
            metadata = StandardsMetadata.objects.create(
                document=document,
                state=self._determine_state(document, standards_data),
                subject=standards_data['subject_area'],
                grade_level=', '.join(standards_data['grade_levels']) if standards_data['grade_levels'] else 'Unknown',
                year_published=datetime.now().year  # Default to current year if not specified
            )
            
            # Create individual standard entries
            for standard_item in standards_data['identified_standards']:
                Standard.objects.create(
                    metadata=metadata,
                    identifier=standard_item['identifier'],
                    description=standard_item['description']
                )
    
    def _determine_state(self, document: Document, standards_data: Dict[str, Any]) -> str:
        """Determine which state the standards are from"""
        
        # First try to infer from the standards identifiers
        for standard in standards_data.get('identified_standards', []):
            identifier = standard['identifier']
            
            # Check for state code at beginning of identifier (e.g., FL.ELA.3.4)
            state_match = re.match(r'^([A-Z]{2})\.', identifier)
            if state_match:
                state_code = state_match.group(1)
                state_map = {
                    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
                    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
                    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
                    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
                    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
                    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
                    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
                    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
                    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
                    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
                    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
                    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
                    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
                }
                
                if state_code in state_map:
                    return state_map[state_code]
        
        # If state can't be determined from identifiers, try the document title
        state_names = [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
            'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
            'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
            'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
            'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 
            'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 
            'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
            'West Virginia', 'Wisconsin', 'Wyoming'
        ]
        
        title = document.title.lower()
        for state in state_names:
            if state.lower() in title:
                return state
        
        # Default for Common Core
        if 'common core' in title.lower() or 'ccss' in title.lower():
            return 'Common Core'
        
        # Default value if state can't be determined
        return 'Unknown'


import re  # Add this import at the top