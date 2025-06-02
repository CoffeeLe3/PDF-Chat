from dotenv import load_dotenv
from google.cloud import storage
import os

load_dotenv()

SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

def cors_configuration(bucket_name: str):
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    bucket = client.get_bucket(bucket_name)
    bucket.cors = [
        {
            "origin": ["http://localhost:3000"],
            "responseHeader": ["Content-Type", "x-goog-resumable"],
            "method": ["PUT", "POST", "OPTIONS"],
            "maxAgeSeconds": 3600,
        }
    ]
    bucket.patch()
    print(f"CORS policies set for bucket {bucket.name}: {bucket.cors}")

cors_configuration(BUCKET_NAME) # type: ignore
