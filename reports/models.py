from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TrafficReport(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    location = models.CharField(max_length=100)
    message = models.CharField(max_length=40)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.location} - {self.message} ({self.severity})"