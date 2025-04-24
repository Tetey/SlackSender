"""
Celery tasks for the scheduler app
"""
import logging
from celery import shared_task
from .services import process_scheduled_messages

logger = logging.getLogger(__name__)

@shared_task
def process_due_messages():
    """
    Task to process all due scheduled messages
    This task is scheduled to run periodically via Celery Beat
    """
    logger.info("Starting scheduled task to process due messages")
    processed_count = process_scheduled_messages()
    logger.info(f"Processed {processed_count} scheduled messages")
    return processed_count
