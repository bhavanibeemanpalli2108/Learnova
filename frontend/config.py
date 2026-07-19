import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    # "http://127.0.0.1:8000/api/v1"
    "https://learnova-backend-s5n2.onrender.com/api/v1"
)

HEALTH_URL = f"{BACKEND_URL}/health"
UPLOAD_URL = f"{BACKEND_URL}/upload"
CHAT_URL = f"{BACKEND_URL}/chat"