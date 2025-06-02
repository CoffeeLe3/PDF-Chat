from pydantic import BaseModel

class UploadNotification(BaseModel):
    filename: str
