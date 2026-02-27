from django.urls import path
from . import views

app_name = 'interview'

urlpatterns = [
    path('', views.home, name='home'),
    path('tts/', views.tts_audio, name='tts_audio'),
    path('start/', views.start_interview, name='start_interview'),
    path('continue/', views.interview_view, name='interview_view'),
    path('end/', views.end_interview, name='end_interview'),  # ← ADD THIS!
]