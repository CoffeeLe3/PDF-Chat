from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.utils.gcs_url_gen import generate_upload_url
from src.backend.utils.publish import publish_message
from src.backend.models.general import UploadNotification
from src.backend.db import pdf_collection
import os
import uuid


BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

origins = [
    "http://localhost:3000",
]

app = FastAPI(
    title="PDF-Chat",
    version="0.1.0",
    description="chat with your pdf's to learn efficiently",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    """
    Root endpoint for API.
    Returns a welcome message.
    """
    return {"message": "Welcome to PDF-Chatr! Start chatting with ypur PDF files"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns the status of the API and Docker service.
    """
    return {
        "status": "ok",
        "message": "API is healthy",
    }


@app.get("/pdf/generate-upload-url")
async def get_upload_url(filename: str):
    return generate_upload_url(filename)


@app.post("/pdf/notify-uploaded")
async def notify_successful_upload(payload: UploadNotification):
    if payload:
        status = "uploaded"
        file_path = f"https://storage.googleapis.com/{BUCKET_NAME}/{payload.filename}"
        pdf_id = str(uuid.uuid4())

        message = {
            "pdf_id": pdf_id,
            "filename": payload.filename,
            "file_path": file_path,
            "status": status,
        }

        insert_result = pdf_collection.insert_one(message.copy())

        if insert_result.inserted_id:
            result = publish_message(message)
            return {
                "message": "Upload notification processed successfully",
                "pdf_id": pdf_id,
                "pubsub": result,
            }
        else:
            return {"error": "Failed to save document in MongoDB"}
    else:
        return {"message": "failed to get status on upload"}


# @app.get("/test-publish")
# async def test_publish():
#     result = publish_message()
#     return result
