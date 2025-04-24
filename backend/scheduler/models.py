from django.db import models
from django.utils import timezone

# Create your models here.

class ScheduledMessage(models.Model):
    """Model for scheduled Slack messages"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    
    message = models.TextField(help_text="The message content to be sent")
    channel = models.CharField(max_length=100, help_text="The Slack channel to send the message to")
    scheduled_time = models.DateTimeField(help_text="When the message should be sent")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Message to {self.channel} at {self.scheduled_time}"
    
    @property
    def is_due(self):
        """Check if the message is due to be sent"""
        return self.status == 'pending' and self.scheduled_time <= timezone.now()
