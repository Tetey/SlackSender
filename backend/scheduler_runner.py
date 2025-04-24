#!/usr/bin/env python
"""
Scheduler runner script for processing scheduled messages.
This script runs as a separate process and periodically checks for scheduled messages that are due to be sent.
"""
import time
import datetime
import subprocess
import logging

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
    
    # Wait for the web server to start up
    logger.info("Waiting 60 seconds for web server to start...")
    time.sleep(60)
    
    # Run the scheduler every minute
    while True:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Running scheduled tasks at {current_time}")
        
        try:
            # Run the management command to process scheduled messages
            result = subprocess.run(
                ['python', 'manage.py', 'process_scheduled_messages'],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Command output: {result.stdout}")
            if result.stderr:
                logger.warning(f"Command stderr: {result.stderr}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running command: {e}")
            logger.error(f"Command stderr: {e.stderr}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        # Wait for the next minute
        logger.info("Waiting 60 seconds for next run...")
        time.sleep(60)

if __name__ == "__main__":
    main()
