from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    """Subject model for standardized subjects"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Grade(models.Model):
    """Grade level model"""
    level = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(help_text="Order for sorting grades")
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.level


class Standard(models.Model):
    """Educational standards (Common Core, etc.)"""
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='standards')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='standards')
    
    def __str__(self):
        return f"{self.code}: {self.description[:50]}..."


class LessonPlan(models.Model):
    """Comprehensive lesson plan model"""
    
    DURATION_CHOICES = [
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '1 hour'),
        (90, '1.5 hours'),
        (120, '2 hours'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Brief description of the lesson")
    
    # Educational Details
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lesson_plans')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='lesson_plans')
    lesson_date = models.DateField(null=True, blank=True, verbose_name="Date of Lesson")  # New field
    duration = models.IntegerField(choices=DURATION_CHOICES, default=45, help_text="Duration in minutes")
    
    # Lesson Components
    learning_objectives = models.TextField(help_text="What students will learn/be able to do")
    essential_question = models.TextField(blank=True, help_text="Key question driving the lesson")
    materials_needed = models.TextField(help_text="List of required materials and resources")
    
    # Lesson Structure
    opening_activity = models.TextField(help_text="How the lesson begins")
    main_instruction = models.TextField(help_text="Core teaching/learning activities")
    guided_practice = models.TextField(blank=True, help_text="Structured practice with teacher support")
    independent_practice = models.TextField(blank=True, help_text="Individual student work")
    closing_activity = models.TextField(help_text="How the lesson concludes")
    
    # Assessment & Differentiation
    formative_assessment = models.TextField(help_text="How you'll check for understanding during lesson")
    summative_assessment = models.TextField(blank=True, help_text="How learning will be evaluated")
    differentiation_strategies = models.TextField(help_text="Accommodations for different learners")
    
    # Additional Fields
    homework_assignment = models.TextField(blank=True, help_text="Any assigned homework")
    extension_activities = models.TextField(blank=True, help_text="Activities for early finishers")
    reflection_notes = models.TextField(blank=True, help_text="Post-lesson reflection and notes")
    
    # Metadata
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False, help_text="Share with other teachers")
    is_template = models.BooleanField(default=False, help_text="Available as template")
    
    # Standards alignment
    standards = models.ManyToManyField(Standard, blank=True, related_name='lesson_plans')
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Lesson Plan"
        verbose_name_plural = "Lesson Plans"
    
    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.grade.level})"


class Material(models.Model):
    """Teaching materials and resources"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(help_text="Material content or instructions")
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    url = models.URLField(blank=True, help_text="External resource URL")
    
    # Categorization
    material_type = models.CharField(max_length=50, choices=[
        ('handout', 'Handout'),
        ('worksheet', 'Worksheet'),
        ('presentation', 'Presentation'),
        ('video', 'Video'),
        ('interactive', 'Interactive Activity'),
        ('assessment', 'Assessment'),
        ('other', 'Other'),
    ], default='other')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials', null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='materials', null=True, blank=True)
    
    # Relationships
    lesson_plans = models.ManyToManyField(LessonPlan, blank=True, related_name='materials')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="materials")
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Resource(models.Model):
    """External resources and references"""
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    
    # Categorization
    resource_type = models.CharField(max_length=50, choices=[
        ('website', 'Website'),
        ('video', 'Video'),
        ('article', 'Article'),
        ('book', 'Book'),
        ('tool', 'Online Tool'),
        ('game', 'Educational Game'),
        ('other', 'Other'),
    ], default='website')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='resources', null=True, blank=True)
    
    # Relationships
    lesson_plans = models.ManyToManyField(LessonPlan, blank=True, related_name='resources')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resources")
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Curriculum(models.Model):
    """Curriculum documents and standards"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    file = models.FileField(upload_to="curriculums/", null=True)
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='curriculums', null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='curriculums', null=True, blank=True)
    
    # Relationships
    lesson_plans = models.ManyToManyField(LessonPlan, blank=True, related_name='curriculums')
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class AIUsageLog(models.Model):
    """Structured log of AI interactions for analytics and debugging."""

    REQUEST_TYPE_CHOICES = [
        ('lesson_assist', 'Lesson Assistance'),
        ('lesson_review', 'Lesson Review'),
        ('general_chat', 'General Chat'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='ai_usage_logs')
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES,
                                     default='general_chat')
    prompt_length = models.IntegerField(default=0, help_text="Character count of the prompt")
    used_curriculum_context = models.BooleanField(default=False)
    response_length = models.IntegerField(default=0, help_text="Character count of the response")
    latency_ms = models.IntegerField(default=0, help_text="Time taken in milliseconds")
    success = models.BooleanField(default=True)
    failure_reason = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "AI Usage Log"
        verbose_name_plural = "AI Usage Logs"

    def __str__(self):
        status = "OK" if self.success else "FAIL"
        return f"[{status}] {self.get_request_type_display()} – {self.created_at:%Y-%m-%d %H:%M}"


class LessonSchedule(models.Model):
    """Schedule lessons for specific dates/times"""
    lesson_plan = models.ForeignKey(LessonPlan, on_delete=models.CASCADE, related_name='schedules')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_schedules')
    
    scheduled_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    
    # Class/Period information
    class_period = models.CharField(max_length=100, blank=True, help_text="Period 1, Math Class, etc.")
    classroom = models.CharField(max_length=100, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=[
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='planned')
    
    notes = models.TextField(blank=True, help_text="Notes about this specific lesson instance")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date', 'start_time']
        unique_together = ['user', 'scheduled_date', 'start_time', 'class_period']
    
    def __str__(self):
        return f"{self.lesson_plan.title} - {self.scheduled_date}"



