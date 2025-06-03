import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1

load_dotenv()

SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")


def callback(message):
    print(f"Received {message}.")
    message.ack()

def start_subscriber():
    subscriber = pubsub_v1.SubscriberClient.from_service_account_file(SERVICE_ACCOUNT_JSON)
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    print(f"Listening for messages on {subscription_path}...")

    future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        future.result()
    except KeyboardInterrupt:
        print("Stopped manually.")
        future.cancel()

if __name__ == "__main__":
    start_subscriber() 