from django.urls import path, reverse_lazy, include # Add include here
from . import views
from django.contrib.auth import views as auth_views # Import auth_views

app_name = 'home'  # Added this line

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('welcome/', views.welcome, name='welcome'),
    
    # Lesson Plan CRUD
    path('mylessonplans/', views.mylessonplans, name='mylessonplans'),
    path('createnewlesson/', views.createnewlesson, name='createnewlesson'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:pk>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:pk>/duplicate/', views.duplicate_lesson, name='duplicate_lesson'),
    path('lesson/<int:pk>/delete/', views.delete_lesson, name='delete_lesson'),
    
    # Resources and Materials
    path('myresources/', views.myresources, name='myresources'),
    path('create-material/', views.create_material, name='create_material'),
    path('create-resource/', views.create_resource, name='create_resource'),
    
    # Calendar and Curriculum
    path('mycurriculums/', views.mycurriculums, name='mycurriculums'),
    path('upload-curriculum/', views.upload_curriculum, name='upload_curriculum'),
    
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    # Add Django's built-in auth URLs for password reset
    path('password_reset/', include('django.contrib.auth.urls')),  # This includes several URLs like password_reset_done, password_reset_confirm, password_reset_complete

    # AI Features
    path('ai_chat/', views.ai_chat, name='ai_chat'),
    
    # Legacy URLs (for backward compatibility)
    path('createnewlesson-legacy/', views.createnewlesson_legacy, name='createnewlesson_legacy'),

    path('profile/', views.profile_view, name='profile'),
    path('mycalendar/', views.mycalendar_view, name='mycalendar'), # This is the correct one

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html', subject_template_name='registration/password_reset_subject.txt', success_url=reverse_lazy('home:password_reset_done')), name='password_reset'),
]
