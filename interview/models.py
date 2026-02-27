# interview/models.py

from django.db import models

class InterviewScore(models.Model):
    interview_token = models.CharField(max_length=200, unique=True)
    candidate_name  = models.CharField(max_length=100)
    candidate_email = models.EmailField()
    raw_score       = models.IntegerField(default=0)
    percentage      = models.FloatField(default=0.0)
    total_questions = models.IntegerField(default=10)
    evaluated_at    = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        max_score = 100  # 10 per question * 10 questions
        self.percentage = round((self.raw_score / max_score) * 100, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidate_name} - {self.percentage}%"