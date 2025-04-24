from django.core.management.base import BaseCommand
from django.utils import timezone
import logging

from scheduler.services import process_scheduled_messages

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process scheduled messages that are due to be sent'

    def handle(self, *args, **options):
        self.stdout.write(f"Starting scheduled message processing at {timezone.now()}")
        
        count = process_scheduled_messages()
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {count} scheduled messages")
        )
