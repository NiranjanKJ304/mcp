"""
Configuration helpers for the backend package.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load .env
load_dotenv(PROJECT_ROOT / ".env")

@dataclass(frozen=True)
class Settings:
    # -----------------------------
    # Database Configuration
    # -----------------------------
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "company")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "")

    # -----------------------------
    # MCP Server
    # -----------------------------
    server_path: Path = PROJECT_ROOT / "server.py"

    # -----------------------------
    # Groq
    # -----------------------------
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    model: str = os.getenv(
        "MODEL",
        "llama-3.3-70b-versatile"
    )


settings = Settings()


def get_settings() -> Settings:
    return settings