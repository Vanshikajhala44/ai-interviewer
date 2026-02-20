from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_interview, name='schedule_interview'),
    path('secret/<uuid:token>/', views.start_interview_from_link, name='start_interview_from_link'),
]