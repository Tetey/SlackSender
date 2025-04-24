#!/usr/bin/env python
"""
Scheduler runner script for processing scheduled messages.
This script runs as a separate process and periodically checks for scheduled messages that are due to be sent.
"""
import os
import time
import datetime
import logging
import django

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('scheduler_runner')

def main():
    """
    Main function that runs the scheduler.
    """
    logger.info("Starting scheduler runner...")
    
    # Set up Django environment
    logger.info("Setting up Django environment...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    # Import Django models after setting up the environment
    from scheduler.models import ScheduledMessage
    from scheduler.services import send_slack_message
    from django.utils import timezone
    
    # Wait for the web server to start up
    logger.info("Waiting 60 seconds for web server to start...")
    time.sleep(60)
    
    # Run the scheduler every minute
    while True:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Running scheduled tasks at {current_time}")
        
        try:
            # Process scheduled messages directly without using the management command
            now = timezone.now()
            logger.info(f"Checking for messages due before {now}")
            
            # Get all pending messages that are due
            due_messages = ScheduledMessage.objects.filter(
                status='pending',
                scheduled_time__lte=now
            )
            
            logger.info(f"Found {due_messages.count()} messages to process")
            
            for message in due_messages:
                logger.info(f"Processing message {message.id} to channel {message.channel}")
                
                try:
                    success = send_slack_message(message.message, message.channel)
                    
                    if success:
                        message.status = 'sent'
                        message.save()
                        logger.info(f"Successfully sent message {message.id}")
                    else:
                        message.status = 'failed'
                        message.save()
                        logger.error(f"Failed to send message {message.id}")
                except Exception as e:
                    message.status = 'failed'
                    message.save()
                    logger.error(f"Error processing message {message.id}: {str(e)}")
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        # Wait for the next minute
        logger.info("Waiting 60 seconds for next run...")
        time.sleep(60)

if __name__ == "__main__":
    main()
