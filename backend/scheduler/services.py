"""
Service for handling scheduled message sending
"""
import logging
from django.utils import timezone
from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .models import ScheduledMessage

logger = logging.getLogger(__name__)

def get_slack_client():
    """
    Get a Slack client instance with the configured token
    """
    return WebClient(token=settings.SLACK_BOT_TOKEN)

def send_slack_message(message, channel):
    """
    Send a message to a Slack channel
    """
    client = get_slack_client()
    try:
        result = client.chat_postMessage(channel=channel, text=message)
        logger.info(f"Message sent to {channel}: {result}")
        return True
    except SlackApiError as e:
        logger.error(f"Error sending message to Slack: {e}")
        return False

def process_scheduled_messages():
    """
    Process all due scheduled messages
    This would typically be run by a scheduler like Celery
    """
    now = timezone.now()
    logger.info(f"Processing scheduled messages at {now}")
    
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
    
    logger.info("Finished processing scheduled messages")
    return due_messages.count()
