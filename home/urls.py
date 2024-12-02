from django.urls import path
from home import views
from .views import frontend_view


urlpatterns = [
    path('ai_chat/', views.ai_chat, name='ai_chat'),
    path('', views.welcome, name='welcome'),
    path('mylessonplans', views.mylessonplans, name='mylessonplans'),
    path('home', views.home, name='home'),
    path('createnewlesson', views.createnewlesson, name='createnewlesson'),
    path('mycalendar', views.mycalendar, name='mycalendar'),
    path('mycurriculums', views.mycurriculums, name='mycurriculums'),
    path('myresources', views.myresources, name='myresources'),
    path('signup', views.signup, name='signup'),
    path('ai_chat/', views.ai_chat, name='ai_chat'),
    path('upload_curriculum/', views.upload_curriculum, name='upload_curriculum'),
    path('login/', views.user_login, name='login'),
    path('', frontend_view, name='frontend'),
]