import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

# Fetch MONGO_URI from env var or fallback to hardcoded string
MONGO_URI = os.getenv(
    "MONGO_URI"
)
