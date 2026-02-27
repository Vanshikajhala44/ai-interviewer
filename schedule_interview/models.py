import uuid
from django.db import models
from django.utils import timezone
import random,string

class SecretInterview(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    candidate_name = models.CharField(max_length=100)
    candidate_email = models.EmailField()
    interviewer_name = models.CharField(max_length=100)
    system_prompt = models.TextField(max_length=2000)
    interview_datetime = models.DateTimeField()
    expires_at = models.DateTimeField(null=True, blank=True)
    used = models.BooleanField(default=False)
    passcode = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField( default=timezone.now)
    coding_question = models.TextField(blank=True, default='')
    coding_topic = models.CharField(max_length=100, blank=True, default='Arrays')
    coding_difficulty = models.CharField(max_length=20, blank=True, default='medium')
    coding_language = models.CharField(max_length=50, blank=True, default='python')
    def save(self, *args, **kwargs):
        # ✅ Auto-generate 6-digit passcode on first save
        if not self.passcode:
            self.passcode = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

  
    def __str__(self):
        return f"{self.candidate_name} - {self.token}"
