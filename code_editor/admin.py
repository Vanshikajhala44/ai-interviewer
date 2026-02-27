
from django.contrib import admin
from .models import CodingQuestion, CodeSubmission

@admin.register(CodingQuestion)
class CodingQuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'difficulty', 'language', 'created_at']

@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['question', 'language', 'status', 'submitted_at']