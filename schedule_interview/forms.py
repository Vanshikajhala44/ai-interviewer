from django import forms

TOPIC_CHOICES = [
    ('Arrays', 'Arrays'),
    ('Strings', 'Strings'),
    ('Linked Lists', 'Linked Lists'),
    ('Dynamic Programming', 'Dynamic Programming'),
    ('Trees', 'Trees'),
    ('Sorting', 'Sorting'),
    ('Recursion', 'Recursion'),
]

DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

LANGUAGE_CHOICES = [
    ('python', 'Python'),
    ('javascript', 'JavaScript'),
    ('java', 'Java'),
    ('cpp', 'C++'),
]

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
    expires_at = forms.DateTimeField(
        label="Link Expiration (optional)",
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    coding_question = forms.CharField(
        label="Coding Question",
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "Generate from side panel and paste here..."
        }),
        max_length=3000
    )
    coding_topic = forms.ChoiceField(
        choices=TOPIC_CHOICES,
        required=False,  # ← hidden field
        initial='Arrays'
    )
    coding_difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,  # ← hidden field
        initial='medium'
    )
    coding_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=False,  # ← hidden field
        initial='python'
    )