from django.urls import path
from . import views

app_name = 'code_editor'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate-question/', views.generate_question, name='generate_question'),
    path('coding-round/<int:question_id>/', views.coding_round, name='coding_round'),
    path('run/', views.run_code, name='run_code'),
    path('submit/', views.submit_code, name='submit_code'),
    path('success/<int:submission_id>/', views.success, name='success'),  # add this
    path('start-from-session/', views.start_coding_from_session, name='start_coding_from_session'),
]