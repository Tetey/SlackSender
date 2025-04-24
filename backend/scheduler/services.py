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
    return WebClient(token=settings.SLACK_API_TOKEN)

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
    due_messages = ScheduledMessage.objects.filter(
        status='pending',
        scheduled_time__lte=timezone.now()
    )
    
    for message in due_messages:
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
            logger.exception(f"Error sending message {message.id}: {str(e)}")
    
    return len(due_messages)
