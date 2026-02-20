import uuid
from django.db import models
from django.utils import timezone

class SecretInterview(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    candidate_name = models.CharField(max_length=100)
    candidate_email = models.EmailField()
    interviewer_name = models.CharField(max_length=100)
    system_prompt = models.TextField(max_length=2000)
    interview_datetime = models.DateTimeField()
    expires_at = models.DateTimeField(null=True, blank=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return f"{self.candidate_name} - {self.token}"