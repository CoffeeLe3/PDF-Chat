import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1
import json
import tempfile
from utils import extract_text_from_pdf
from google.cloud import storage

load_dotenv()

SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")


def download_pdf_via_gcs(bucket_name, blob_name, destination_path):
    storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(destination_path)


def callback(message):
    try:
        print(f"Received {message.data}.")
        data = json.loads(message.data.decode("utf-8"))

        bucket_name = GCS_BUCKET_NAME
        blob_name = data.get("filename")

        if not blob_name:
            raise ValueError("Message missing 'filename' field.")

        # download to tmp
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".pdf", dir="/tmp"
        ) as tmp_file:
            download_pdf_via_gcs(bucket_name, blob_name, tmp_file.name)
            local_path = tmp_file.name

        extracted_text = extract_text_from_pdf(local_path)
        print("Extracted text:")
        print(extracted_text)

        os.remove(local_path)

        message.ack()

    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()


def start_subscriber():
    subscriber = pubsub_v1.SubscriberClient.from_service_account_file(
        SERVICE_ACCOUNT_JSON
    )
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
