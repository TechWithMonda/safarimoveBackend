from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import timedelta

class DisappearingMessage(models.Model):
    sender = models.CharField(max_length=100)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.sent_at + timedelta(hours=24)
