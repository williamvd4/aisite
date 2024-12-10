from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Changed name from 'index' to 'home'
    path('welcome/', views.welcome, name='welcome'),
    path('mylessonplans/', views.mylessonplans, name='mylessonplans'),
    path('createnewlesson/', views.createnewlesson, name='createnewlesson'),
    path('mycalendar/', views.mycalendar, name='mycalendar'), 
    path('mycurriculums/', views.mycurriculums, name='mycurriculums'),
    path('myresources/', views.myresources, name='myresources'),
    path('signup/', views.signup, name='signup'),
    path('ai_chat/', views.ai_chat, name='ai_chat'),
    path('login/', views.user_login, name='login'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
]
