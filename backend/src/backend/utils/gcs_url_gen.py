from google.cloud import storage
from datetime import timedelta
import os


SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")


def generate_upload_url(filename: str):
    """
    generates a pre-signed url to upload files to google cloud
    returns the pre-signed url (valid for 15 minutes)
    """
    
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="PUT",
        content_type="application/pdf",
    )

    return {"upload_url": url}
