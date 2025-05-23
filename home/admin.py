# Import the necessary modules
from django.contrib import admin
from .models import (MyFormModel, Lesson, Curriculum, Resource, Material, 
                    LessonPlan, Subject, Grade, Standard, LessonSchedule)


# Admin for new comprehensive models
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('level', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'subject', 'grade')
    list_filter = ('subject', 'grade')
    search_fields = ('code', 'description')


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade', 'user', 'duration', 'created_at', 'is_public')
    list_filter = ('subject', 'grade', 'duration', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'learning_objectives')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('standards',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'subject', 'grade', 'duration', 'user')
        }),
        ('Lesson Content', {
            'fields': ('learning_objectives', 'essential_question', 'materials_needed')
        }),
        ('Lesson Structure', {
            'fields': ('opening_activity', 'main_instruction', 'guided_practice', 
                      'independent_practice', 'closing_activity')
        }),
        ('Assessment & Differentiation', {
            'fields': ('formative_assessment', 'summative_assessment', 'differentiation_strategies')
        }),
        ('Additional Information', {
            'fields': ('homework_assignment', 'extension_activities', 'reflection_notes')
        }),
        ('Standards & Sharing', {
            'fields': ('standards', 'is_public', 'is_template')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'subject', 'grade', 'user', 'is_public')
    list_filter = ('material_type', 'subject', 'grade', 'is_public')
    search_fields = ('title', 'description')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'subject', 'grade', 'user', 'is_public')
    list_filter = ('resource_type', 'subject', 'grade', 'is_public')
    search_fields = ('title', 'description', 'url')


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade', 'user', 'created_at')
    list_filter = ('subject', 'grade', 'created_at')
    search_fields = ('title', 'description')


@admin.register(LessonSchedule)
class LessonScheduleAdmin(admin.ModelAdmin):
    list_display = ('lesson_plan', 'scheduled_date', 'start_time', 'status', 'user')
    list_filter = ('status', 'scheduled_date', 'lesson_plan__subject')
    search_fields = ('lesson_plan__title', 'class_period', 'classroom')
    date_hierarchy = 'scheduled_date'


# Legacy models
admin.site.register(MyFormModel)
admin.site.register(Lesson)

