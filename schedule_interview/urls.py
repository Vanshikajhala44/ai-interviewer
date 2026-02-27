
from django.urls import path
from . import views

app_name = 'schedule_interview'

urlpatterns = [
    path('', views.schedule_interview, name='schedule_interview'),
    path('success/<uuid:token>/', views.schedule_success, name='schedule_success'),
    path('start/<uuid:token>/', views.start_interview_from_link, name='start_interview'),
     path('verify/<uuid:token>/', views.verify_passcode, name='verify_passcode'),
     path('login/', views.interviewer_login, name='interviewer_login'),
    path('logout/', views.interviewer_logout, name='interviewer_logout'),
]