# schedule_interview/forms.py
from django import forms

class InterviewForm(forms.Form):
    candidate_name = forms.CharField(label="Candidate Name", max_length=100)
    candidate_email = forms.EmailField(label="Candidate Email")
    interviewer_name = forms.CharField(label="Interviewer Name", max_length=100)
    system_prompt = forms.CharField(
        label="AI System Prompt",
        widget=forms.Textarea(attrs={"rows": 4}),
        max_length=2000
    )
    interview_datetime = forms.DateTimeField(
        label="Interview Date & Time",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    # Optional expiration
    expires_at = forms.DateTimeField(
        label="Link Expiration (optional)",
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )