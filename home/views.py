from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse # Added for redirecting with reverse
from django import forms
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
import cohere
import json

from .forms import (MyForm, LessonPlanForm, MaterialForm, ResourceForm, 
                   CustomUserCreationForm, LessonSearchForm, UserProfileForm)
from .models import (MyFormModel, LessonPlan, Material, Resource, Curriculum, 
                    Subject, Grade, Standard, LessonSchedule)
from .ai.ai_review import review_lesson, generate_ai_response
from .ai.ai_utils import analyze_text


def home(request):
    """Enhanced home page with dashboard data"""
    if not request.user.is_authenticated:
        return redirect(reverse('home:welcome')) # Redirect to welcome page if not logged in

    recent_lessons = LessonPlan.objects.filter(user=request.user)[:5]
    total_lessons = LessonPlan.objects.filter(user=request.user).count()
    total_materials = Material.objects.filter(user=request.user).count()
    total_resources = Resource.objects.filter(user=request.user).count()
    
    context = {
        'recent_lessons': recent_lessons,
        'total_lessons': total_lessons,
        'total_materials': total_materials,
        'total_resources': total_resources,
    }
    
    return render(request, "pages/home.html", context)


def welcome(request):
    return render(request, "pages/welcome.html")


@login_required
def mylessonplans(request):
    """Enhanced lesson plans listing with search and filtering"""
    form = LessonSearchForm(request.GET)
    lessons = LessonPlan.objects.filter(user=request.user)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        subject = form.cleaned_data.get('subject')
        grade = form.cleaned_data.get('grade')
        duration = form.cleaned_data.get('duration')
        
        if query:
            lessons = lessons.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(learning_objectives__icontains=query)
            )
        if subject:
            lessons = lessons.filter(subject=subject)
        if grade:
            lessons = lessons.filter(grade=grade)
        if duration:
            lessons = lessons.filter(duration=duration)
    
    # Pagination
    paginator = Paginator(lessons.order_by('-updated_at'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "pages/mylessonplans.html", {
        'page_obj': page_obj,
        'search_form': form,  # Changed from 'form' to 'search_form'
        'lesson_plans': page_obj.object_list,  # Changed from 'lessons': page_obj
        'is_paginated': page_obj.has_other_pages() # Added for pagination template logic
    })


@login_required
def lesson_detail(request, pk):
    """Detailed lesson plan view with AI feedback"""
    lesson = get_object_or_404(LessonPlan, pk=pk, user=request.user)
    ai_feedback = analyze_text(lesson.description)
    return render(request, "pages/lesson_plan_detail.html", {
        'lesson_plan': lesson,  # Changed context variable name
        'ai_feedback': ai_feedback
    })


@login_required
def createnewlesson(request):
    """Enhanced lesson creation with comprehensive form"""
    if request.method == "POST":
        # Handle AJAX AI chat requests
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            user_input = request.POST.get("ai_input", "")
            ai_response = generate_ai_response(user_input)
            return JsonResponse({"ai_response": ai_response})
        
        # Handle lesson creation
        form = LessonPlanForm(request.POST, user=request.user)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.user = request.user
            lesson.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f"Lesson '{lesson.title}' created successfully!")
            return redirect('home:lesson_detail', pk=lesson.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LessonPlanForm(user=request.user)

    return render(request, "pages/createnewlesson.html", {"form": form})


@login_required
def edit_lesson(request, pk):
    """Edit existing lesson plan"""
    lesson = get_object_or_404(LessonPlan, pk=pk, user=request.user)
    
    if request.method == "POST":
        form = LessonPlanForm(request.POST, instance=lesson, user=request.user)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, f"Lesson '{lesson.title}' updated successfully!")
            return redirect('home:lesson_detail', pk=lesson.pk) # Added namespace
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LessonPlanForm(instance=lesson, user=request.user)

    return render(request, "pages/lesson_plan_form.html", {"form": form, "lesson": lesson})


@login_required
def duplicate_lesson(request, pk):
    """Duplicate an existing lesson plan"""
    original_lesson = get_object_or_404(LessonPlan, pk=pk, user=request.user)
    
    # Create a copy
    duplicated_lesson = LessonPlan.objects.get(pk=pk)
    duplicated_lesson.pk = None  # This will create a new instance
    duplicated_lesson.title = f"Copy of {original_lesson.title}"
    duplicated_lesson.save()
    
    # Copy many-to-many relationships
    duplicated_lesson.standards.set(original_lesson.standards.all())
    duplicated_lesson.materials.set(original_lesson.materials.all())
    duplicated_lesson.resources.set(original_lesson.resources.all())
    
    messages.success(request, f"Lesson duplicated successfully!")
    return redirect('edit_lesson', pk=duplicated_lesson.pk)


@login_required
def delete_lesson(request, pk):
    """Delete lesson plan"""
    lesson = get_object_or_404(LessonPlan, pk=pk, user=request.user)
    
    if request.method == "POST":
        lesson_title = lesson.title
        lesson.delete()
        messages.success(request, f"Lesson '{lesson_title}' deleted successfully!")
        return redirect('home:mylessonplans') # Added namespace
    
    return render(request, "pages/lesson_plan_confirm_delete.html", {"lesson_plan": lesson}) # Changed template and context variable


@login_required
def mycalendar_view(request):
    lesson_plans = LessonPlan.objects.filter(user=request.user, lesson_date__isnull=False)
    events = []
    for lesson in lesson_plans:
        events.append({
            'title': lesson.title,
            'start': lesson.lesson_date.strftime("%Y-%m-%d"),
            'url': reverse('home:lesson_detail', args=[lesson.pk]),
            'allDay': True
        })
    return render(request, 'pages/mycalendar.html', {'events': json.dumps(events)})


@login_required
def mycurriculums(request):
    """Enhanced curriculum management"""
    curriculums = Curriculum.objects.filter(user=request.user)
    return render(request, "pages/mycurriculums.html", {"curriculums": curriculums})


@login_required
def myresources(request):
    """Resource management page"""
    resources = Resource.objects.filter(user=request.user)
    materials = Material.objects.filter(user=request.user)
    
    return render(request, "pages/myresources.html", {
        'resources': resources,
        'materials': materials
    })


@login_required
def create_material(request):
    """Create new teaching material"""
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            material.save()
            messages.success(request, f"Material '{material.title}' created successfully!")
            return redirect('myresources')
    else:
        form = MaterialForm()
    
    return render(request, "pages/create_material.html", {"form": form})


@login_required
def create_resource(request):
    """Create new external resource"""
    if request.method == "POST":
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.user = request.user
            resource.save()
            messages.success(request, f"Resource '{resource.title}' created successfully!")
            return redirect('myresources')
    else:
        form = ResourceForm()
    
    return render(request, "pages/create_resource.html", {"form": form})


def signup(request):
    """Enhanced user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'pages/signup.html', {'form': form})


def user_login(request):
    """Enhanced login with better error handling"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "pages/welcome.html")
    else:
        return render(request, "pages/welcome.html")


@login_required
def ai_chat(request):
    """AI chat functionality"""
    ai_response = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.POST.get("ai_input", "")
        
        if user_input:
            try:
                ai_response = generate_ai_response(user_input)
            except Exception as e:
                ai_response = "Sorry, I'm having trouble right now. Please try again later."
                print(f"AI Chat Error: {e}")

    return render(request, "ai/ai_chat.html", {
        "ai_response": ai_response, 
        "user_input": user_input
    })


@require_POST
@login_required
def upload_curriculum(request):
    """Upload curriculum file"""
    if request.FILES.get("file"):
        file = request.FILES["file"]
        # You'll need to add subject and grade fields to the form
        curriculum = Curriculum(
            title=file.name, 
            user=request.user, 
            file=file,
            # subject=subject,  # Add these after updating the form
            # grade=grade,
        )
        curriculum.save()
        return JsonResponse({
            "message": "File uploaded successfully",
            "file_name": file.name,
            "file_url": curriculum.file.url,
        })
    return JsonResponse({"error": "No file uploaded"}, status=400)


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'pages/profile.html', {'form': form})


# Legacy view - keeping for backward compatibility
def createnewlesson_legacy(request):
    """Legacy lesson creation - deprecated"""
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            messages.success(request, "Lesson created successfully!")
            return redirect('mylessonplans')
    else:
        form = MyForm()

    return render(request, "pages/createnewlesson_legacy.html", {"form": form})
