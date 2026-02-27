from django.db import models

# Create your models here.
from django.db import models

class CodingQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ]

    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    language = models.CharField(max_length=50)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    example_input = models.TextField(blank=True)
    example_output = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    starter_code = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.difficulty}"


class CodeSubmission(models.Model):
    question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE, related_name='submissions')
    language = models.CharField(max_length=50)
    code = models.TextField()
    output = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    status = models.CharField(max_length=100, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question.topic} - {self.submitted_at}"