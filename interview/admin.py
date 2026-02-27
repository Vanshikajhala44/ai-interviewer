from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import InterviewScore

@admin.register(InterviewScore)
class InterviewScoreAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'candidate_email', 'raw_score', 'percentage', 'evaluated_at']