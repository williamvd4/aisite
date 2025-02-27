"""
Content extractors for curriculum documents and standards.
These extractors specialize in identifying specific types of information 
within documents.
"""
import re
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple

import nltk
from nltk.tokenize import sent_tokenize
import spacy
try:
    import en_core_web_sm
    nlp = en_core_web_sm.load()
except ImportError:
    nlp = spacy.load("en_core_web_sm")
except:
    # Fallback if spaCy model isn't available
    nlp = None

logger = logging.getLogger(__name__)

class BaseExtractor(ABC):
    """Base class for content extractors"""
    
    @abstractmethod
    def extract(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Extract structured information from text"""
        pass

class StandardsExtractor(BaseExtractor):
    """Extractor for academic standards from documents"""
    
    def __init__(self):
        # Common patterns for standards identifiers
        self.standard_patterns = [
            # Common Core style (e.g., CCSS.ELA-LITERACY.RL.9-10.1)
            r'([A-Z]+\.[\w\.-]+\.\w+\.\d+(?:-\d+)?\.(?:\d+[a-z]?))',
            # State standard style (e.g., MA.ELA.9.4)
            r'([A-Z]{2}\.(?:ELA|Math|Science|SocialStudies)\.(?:\d+)\.(?:\d+)(?:\.\w+)?)',
            # Simple standards (e.g., Standard 3.4.2)
            r'Standard\s+(\d+\.\d+(?:\.\d+)?)',
            # Another format with standard prefix (e.g., Std 3.A.1)
            r'(?:Std|Standard)\s+(\d+\.[A-Z](?:\.\d+)?)'
        ]
    
    def extract(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Extract standards information from text"""
        results = {
            'identified_standards': [],
            'subject_area': self._extract_subject_area(text, metadata),
            'grade_levels': self._extract_grade_levels(text, metadata)
        }
        
        # Extract standards by pattern matching
        for pattern in self.standard_patterns:
            for match in re.finditer(pattern, text):
                standard_id = match.group(1)
                
                # Get the standard description (the sentence containing the standard)
                sentences = sent_tokenize(text[match.start():match.start()+500])
                if sentences:
                    description = sentences[0].strip()
                    
                    # Add to results
                    results['identified_standards'].append({
                        'identifier': standard_id,
                        'description': description,
                        'position': match.start()
                    })
        
        # Sort by position in document
        results['identified_standards'].sort(key=lambda x: x['position'])
        
        # Try to categorize standards by topics
        results['topics'] = self._categorize_by_topics(results['identified_standards'])
        
        return results
    
    def _extract_subject_area(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """Attempt to extract the subject area from the document"""
        subjects = ['mathematics', 'math', 'english language arts', 'ela', 'science', 
                    'social studies', 'history', 'art', 'music', 'physical education',
                    'health', 'computer science', 'world languages', 'foreign language']
        
        # Check metadata first if available
        if metadata:
            # Check title and other metadata fields
            for field in ['title', 'subject', 'category']:
                if field in metadata:
                    value = metadata[field]
                    for subject in subjects:
                        if subject in value.lower():
                            return subject
        
        # Fall back to text analysis
        text_lower = text.lower()
        for subject in subjects:
            if subject in text_lower:
                # Count occurrences to find the most likely subject
                count = text_lower.count(subject)
                if count > 2:  # Arbitrary threshold
                    return subject
        
        return "unknown"
    
    def _extract_grade_levels(self, text: str, metadata: Dict[str, Any] = None) -> List[str]:
        """Extract grade levels mentioned in the document"""
        grade_patterns = [
            # Numeric grades (e.g., Grade 5, Grade 6-8)
            r'Grade\s+(\d+(?:-\d+)?)',
            # K-12 style (e.g., K-5, K-8)
            r'K-(\d+)',
            # Grade ranges with dash (e.g., Grades 9-12)
            r'Grades\s+(\d+-\d+)'
        ]
        
        grades = []
        for pattern in grade_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                grades.append(match.group(1))
        
        # Remove duplicates
        return list(set(grades))
    
    def _categorize_by_topics(self, standards: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Attempt to categorize standards by topics based on content analysis"""
        topics = {}
        
        # Skip if no spaCy model available
        if not nlp:
            return topics
        
        for standard in standards:
            description = standard['description']
            
            # Use spaCy to analyze the text
            doc = nlp(description)
            
            # Extract key phrases (noun chunks)
            key_phrases = [chunk.text.lower() for chunk in doc.noun_chunks]
            
            # Assign to a topic based on key phrases
            assigned = False
            for phrase in key_phrases:
                # Look for topic indicators
                for topic_word in ['read', 'writ', 'speak', 'listen', 'number', 'algebra', 'geometry', 
                                   'data', 'statistic', 'science', 'history', 'geography']:
                    if topic_word in phrase:
                        if topic_word not in topics:
                            topics[topic_word] = []
                        topics[topic_word].append(standard)
                        assigned = True
                        break
                
                if assigned:
                    break
            
            # If not assigned to a specific topic, put in "other"
            if not assigned:
                if "other" not in topics:
                    topics["other"] = []
                topics["other"].append(standard)
        
        return topics

class CurriculumExtractor(BaseExtractor):
    """Extractor for curriculum materials from documents"""
    
    def extract(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Extract curriculum information from text"""
        results = {
            'learning_objectives': self._extract_learning_objectives(text),
            'activities': self._extract_activities(text),
            'assessments': self._extract_assessments(text),
            'resources': self._extract_resources(text),
            'timeframe': self._extract_timeframe(text),
            'grade_levels': self._extract_grade_levels(text, metadata),
            'subject': self._extract_subject(text, metadata)
        }
        
        return results
    
    def _extract_learning_objectives(self, text: str) -> List[str]:
        """Extract learning objectives from the document"""
        objectives = []
        
        # Common patterns for learning objectives
        patterns = [
            r'(?:Students will|Learners will|Students should)(?:\s+be able to)?\s+(.*?)(?:\.|$)',
            r'Learning Objectives?(?:.*?)(?:\n|:)\s*(.*?)(?:\n\n|\n[A-Z])',
            r'Objective(?:s)?(?:.*?)(?:\n|:)\s*(.*?)(?:\n\n|\n[A-Z])',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Clean up the extracted text
                obj = match.group(1).strip()
                if obj and len(obj) > 10:  # Minimum length to filter noise
                    # Split by bullet points or numbers if present
                    if re.search(r'(?:\n\s*[-•*]|\n\s*\d+\.)', obj):
                        for line in re.split(r'(?:\n\s*[-•*]|\n\s*\d+\.)', obj):
                            if line.strip() and len(line.strip()) > 10:
                                objectives.append(line.strip())
                    else:
                        objectives.append(obj)
        
        return objectives
    
    def _extract_activities(self, text: str) -> List[Dict[str, str]]:
        """Extract learning activities from the document"""
        activities = []
        
        # Look for sections that describe activities
        activity_sections = self._find_sections(text, ['Activities', 'Learning Activities', 'Tasks', 'Procedures'])
        
        for section in activity_sections:
            # Parse individual activities within the section
            # This is a simplified approach - would need refinement for real documents
            activity_matches = re.finditer(r'(?:(?:\d+\.)|(?:•)|(?:-)|(?:[A-Z][a-z]+:))\s*(.*?)(?:\n\n|\n(?:(?:\d+\.)|(?:•)|(?:-)|(?:[A-Z][a-z]+:))|\Z)', 
                                         section, re.DOTALL)
            
            for match in activity_matches:
                activity_text = match.group(1).strip()
                if activity_text and len(activity_text) > 20:  # Minimum length to filter noise
                    activities.append({
                        'description': activity_text,
                        'type': self._classify_activity_type(activity_text)
                    })
        
        return activities
    
    def _classify_activity_type(self, activity_text: str) -> str:
        """Classify the type of learning activity"""
        activity_types = {
            'discussion': ['discuss', 'conversation', 'debate', 'share', 'talk about'],
            'group_work': ['group', 'team', 'collaborate', 'work together'],
            'individual_work': ['individual', 'independently', 'own work', 'personal'],
            'research': ['research', 'investigate', 'explore', 'find out', 'search'],
            'hands_on': ['experiment', 'build', 'create', 'construct', 'draw', 'design'],
            'reading': ['read', 'reading', 'text', 'book', 'article'],
            'writing': ['write', 'essay', 'journal', 'note', 'composition'],
            'assessment': ['quiz', 'test', 'exam', 'assessment', 'evaluate']
        }
        
        text_lower = activity_text.lower()
        
        for activity_type, keywords in activity_types.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return activity_type
        
        return 'other'
    
    def _extract_assessments(self, text: str) -> List[Dict[str, str]]:
        """Extract assessment information from the document"""
        assessments = []
        
        # Look for sections that describe assessments
        assessment_sections = self._find_sections(text, ['Assessment', 'Evaluation', 'Grading', 
                                                       'Performance Tasks', 'Tests', 'Quizzes'])
        
        for section in assessment_sections:
            # Parse individual assessments within the section
            assessment_matches = re.finditer(r'(?:(?:\d+\.)|(?:•)|(?:-)|(?:[A-Z][a-z]+:))\s*(.*?)(?:\n\n|\n(?:(?:\d+\.)|(?:•)|(?:-)|(?:[A-Z][a-z]+:))|\Z)', 
                                           section, re.DOTALL)
            
            for match in assessment_matches:
                assessment_text = match.group(1).strip()
                if assessment_text and len(assessment_text) > 20:  # Minimum length to filter noise
                    assessments.append({
                        'description': assessment_text,
                        'type': self._classify_assessment_type(assessment_text)
                    })
        
        return assessments
    
    def _classify_assessment_type(self, assessment_text: str) -> str:
        """Classify the type of assessment"""
        assessment_types = {
            'formative': ['formative', 'ongoing', 'during', 'check for understanding'],
            'summative': ['summative', 'final', 'end of unit', 'end of chapter'],
            'project': ['project', 'portfolio', 'presentation'],
            'quiz': ['quiz', 'short test'],
            'test': ['test', 'exam', 'examination'],
            'rubric': ['rubric', 'criteria', 'scoring guide'],
            'self_assessment': ['self-assessment', 'self assessment', 'reflect on their own']
        }
        
        text_lower = assessment_text.lower()
        
        for assessment_type, keywords in assessment_types.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return assessment_type
        
        return 'other'
    
    def _extract_resources(self, text: str) -> List[str]:
        """Extract required resources or materials from the document"""
        resources = []
        
        # Look for sections that describe resources
        resource_sections = self._find_sections(text, ['Resources', 'Materials', 'Supplies', 'Equipment'])
        
        for section in resource_sections:
            # Parse individual resources within the section
            resource_matches = re.finditer(r'(?:(?:\d+\.)|(?:•)|(?:-))\s*(.*?)(?:\n(?:(?:\d+\.)|(?:•)|(?:-))|\Z)', 
                                         section)
            
            for match in resource_matches:
                resource_text = match.group(1).strip()
                if resource_text:
                    resources.append(resource_text)
        
        return resources
    
    def _extract_timeframe(self, text: str) -> Dict[str, Any]:
        """Extract timeframe information from the document"""
        timeframe = {}
        
        # Look for patterns that indicate timeframe
        patterns = [
            r'(\d+)\s+(?:day|days)',
            r'(\d+)\s+(?:week|weeks)',
            r'(\d+)\s+(?:class periods|periods|classes)',
            r'(\d+)\s+(?:minutes|hours)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                unit = re.search(r'(\w+)$', pattern).group(1)
                timeframe[unit] = value
                break
        
        return timeframe
    
    def _extract_grade_levels(self, text: str, metadata: Dict[str, Any] = None) -> List[str]:
        """Extract grade levels from the document"""
        grade_levels = []
        
        # Check title and metadata first if available
        if metadata and 'title' in metadata:
            title = metadata['title']
            grade_match = re.search(r'Grade\s+(\d+(?:-\d+)?)', title, re.IGNORECASE)
            if grade_match:
                grade_levels.append(grade_match.group(1))
        
        # Search in the text
        patterns = [
            r'Grade\s+(\d+(?:-\d+)?)',
            r'Grades\s+(\d+(?:-\d+)?)',
            r'(\d+)(?:th|st|nd|rd) Grade',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                grade_levels.append(match.group(1))
        
        # Remove duplicates
        return list(set(grade_levels))
    
    def _extract_subject(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """Extract subject information from the document"""
        subjects = ['Mathematics', 'Math', 'English Language Arts', 'ELA', 'Science', 
                  'Social Studies', 'History', 'Art', 'Music', 'Physical Education',
                  'Health', 'Computer Science', 'World Languages', 'Foreign Language']
        
        # Check title and metadata first if available
        if metadata and 'title' in metadata:
            title = metadata['title']
            for subject in subjects:
                if subject.lower() in title.lower():
                    return subject
        
        # Count occurrences in the text
        text_lower = text.lower()
        max_count = 0
        detected_subject = 'unknown'
        
        for subject in subjects:
            count = text_lower.count(subject.lower())
            if count > max_count:
                max_count = count
                detected_subject = subject
        
        return detected_subject if max_count > 2 else 'unknown'
    
    def _find_sections(self, text: str, section_names: List[str]) -> List[str]:
        """Find sections in the document by their headings"""
        sections = []
        
        for name in section_names:
            # Look for the section heading followed by content
            pattern = fr'(?:^|\n)\s*{name}[:\s]*\n+(.*?)(?:\n\s*[A-Z][A-Za-z\s]+[:\s]*\n+|\Z)'
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                section_text = match.group(1).strip()
                if section_text:
                    sections.append(section_text)
        
        return sections