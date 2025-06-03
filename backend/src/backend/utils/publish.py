import os
import json
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC = os.getenv("TOPIC_NAME")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def publish_message(data):
    """
    subcribes to a topic and 
    publishes message
    """
    publisher = pubsub_v1.PublisherClient.from_service_account_file(SERVICE_ACCOUNT_JSON)
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC)

    json_data = json.dumps(data).encode("utf-8")

    future = publisher.publish(topic_path, json_data)

    print(f"Published message ID: {future.result()}")
    return f"Published message ID: {future.result()}"
