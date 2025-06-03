from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.utils.gcs_url_gen import generate_upload_url
from src.backend.utils.publish import publish_message
from src.backend.models.general import UploadNotification
import os


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
        file_path = f"https://storage.googleapis.com/{BUCKET_NAME}/{payload.filename}"
        message = {
            "filename": payload.filename,
            "file_path": file_path,
        }
        result = publish_message(message)
        return result
    else:
        return { "message": "failed to get status on upload" }


# @app.get("/test-publish")
# async def test_publish():
#     result = publish_message()
#     return result
