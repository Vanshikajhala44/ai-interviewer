from django.urls import path
from . import views
# from .views import home

urlpatterns = [
    path('', views.schedule_interview, name='schedule_interview'),
    path('secret/<uuid:token>/', views.start_interview_from_link, name='start_interview_from_link'),
    #  path("", home, name="home"),
    
]