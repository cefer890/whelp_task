from celery import Celery
import requests
from models import Task
import json
import logging
import os

# Get the API key from environment variables
api_key = os.environ.get('API_KEY')

# RabbitMQ broker URL
broker_url = 'amqp://guest:guest@localhost'

# Create a Celery application
celery_app = Celery('tasks', broker=broker_url)

# Create a logger
logger = logging.getLogger(__name__)

# Celery task for processing the IP address
@celery_app.task
def process_task(ip_address):
    try:
        # Fetch data from the IP data service
        response = requests.get(f"https://ipdata.co/{ip_address}?api-key={api_key}")

        if response.status_code == 200:
            # Convert JSON data to a string
            data_json = json.dumps(response.json())

            # Save the data to the database
            new_task = Task.create(ip_address=ip_address, data=data_json)
            logger.info("Task completed successfully: %s", ip_address)
            return {"status": "success", "message": "Task completed successfully"}
        else:
            logger.error("Failed to fetch data from IP service: %s", ip_address)
            return {"status": "error", "message": "Failed to fetch data from IP service"}
    except Exception as e:
        logger.exception("An error occurred while processing task: %s", e)
        return {"status": "error", "message": str(e)}
