"""
Management command to process scheduled messages
"""
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from scheduler.models import ScheduledMessage
from scheduler.services import send_slack_message

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process scheduled messages that are due to be sent'

    def handle(self, *args, **options):
        now = timezone.now()
        self.stdout.write(f"Processing scheduled messages at {now}")
        
        # Get all pending messages that are due
        due_messages = ScheduledMessage.objects.filter(
            status='pending',
            scheduled_time__lte=now
        )
        
        self.stdout.write(f"Found {due_messages.count()} messages to process")
        
        for message in due_messages:
            self.stdout.write(f"Processing message {message.id} to channel {message.channel}")
            
            try:
                success = send_slack_message(message.message, message.channel)
                
                if success:
                    message.status = 'sent'
                    message.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully sent message {message.id}"))
                else:
                    message.status = 'failed'
                    message.save()
                    self.stdout.write(self.style.ERROR(f"Failed to send message {message.id}"))
            except Exception as e:
                message.status = 'failed'
                message.save()
                logger.error(f"Error processing message {message.id}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Error processing message {message.id}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS("Finished processing scheduled messages"))
