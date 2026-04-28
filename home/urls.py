from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
    # Main pages
    path('home/', views.home, name='home'),
    path('welcome/', views.welcome, name='welcome'),

    # Lesson Plan CRUD
    path('mylessonplans/', views.mylessonplans, name='mylessonplans'),
    path('createnewlesson/', views.createnewlesson, name='createnewlesson'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:pk>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:pk>/duplicate/', views.duplicate_lesson, name='duplicate_lesson'),
    path('lesson/<int:pk>/delete/', views.delete_lesson, name='delete_lesson'),
    path('lesson/<int:pk>/archive/', views.archive_lesson, name='archive_lesson'),
    path('lesson/autosave/', views.autosave_lesson, name='autosave_lesson'),
    path('lesson/<int:pk>/autosave/', views.autosave_lesson, name='autosave_lesson_pk'),

    # Resources and Materials
    path('myresources/', views.myresources, name='myresources'),
    path('create-material/', views.create_material, name='create_material'),
    path('material/<int:pk>/edit/', views.edit_material, name='edit_material'),
    path('material/<int:pk>/delete/', views.delete_material, name='delete_material'),
    path('create-resource/', views.create_resource, name='create_resource'),
    path('resource/<int:pk>/edit/', views.edit_resource, name='edit_resource'),
    path('resource/<int:pk>/delete/', views.delete_resource, name='delete_resource'),

    # Calendar and Curriculum
    path('mycurriculums/', views.mycurriculums, name='mycurriculums'),
    path('upload-curriculum/', views.upload_curriculum, name='upload_curriculum'),
    path('curriculum/<int:pk>/delete/', views.delete_curriculum, name='delete_curriculum'),
    path('mycalendar/', views.mycalendar_view, name='mycalendar'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home:welcome'), name='logout'),

    # Password Reset
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('home:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('home:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),

    # AI Features
    path('ai_chat/', views.ai_chat, name='ai_chat'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
]
