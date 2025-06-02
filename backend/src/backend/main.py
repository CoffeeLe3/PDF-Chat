from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.utils.gcs_url_gen import generate_upload_url

origins = [
        "http://localhost:3000",
]

app = FastAPI(
    title="PDF-Chat",
    version="0.1.0",
    description="chat with your pdf's to learn efficiently"
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


@app.get("/generate-upload-url")
async def get_upload_url(filename: str):
    return generate_upload_url(filename)
