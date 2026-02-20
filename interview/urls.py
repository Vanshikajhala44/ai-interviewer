


# interview/urls.py
from django.urls import path
from .views import home, start_interview, interview_view, transcribe,tts_audio
app_name = "interview"  # <-- add this line
urlpatterns = [
    path("", home, name="home"),
   
    path("start/", start_interview, name="start_interview"),
    path("interview/", interview_view, name="interview_view"),
    path("transcribe/", transcribe, name="transcribe"),
    path('tts_audio/', tts_audio, name='tts_audio'),
]

