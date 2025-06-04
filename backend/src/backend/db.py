from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URL")
DB_NAME = os.getenv("MONGODB_DATABASE")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
pdf_collection = db["pdfs"]