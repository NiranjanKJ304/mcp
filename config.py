import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv(PROJECT_ROOT / ".env")


GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv(
    "GITHUB_PERSONAL_ACCESS_TOKEN"
)


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

MODEL = os.getenv(
    "MODEL",
    "llama-3.3-70b-versatile"
)


if not GITHUB_PERSONAL_ACCESS_TOKEN:
    raise ValueError(
        "GITHUB_PERSONAL_ACCESS_TOKEN is missing from .env"
    )  

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing from .env"
    )  

