"""
Configuration management for Vectorless RAG.
Handles environment variables, defaults, and app settings.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class AppConfig:
    """Central configuration manager for the application."""

    # App metadata
    APP_TITLE = "Vectorless RAG"
    APP_ICON = "🔍"
    APP_LAYOUT = "wide"
    APP_SIDEBAR_STATE = "expanded"

    # Groq API settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    AVAILABLE_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]

    # Chunking defaults
    DEFAULT_CHUNK_SIZE = 300
    DEFAULT_OVERLAP = 50
    CHUNK_SIZE_MIN = 100
    CHUNK_SIZE_MAX = 600
    CHUNK_SIZE_STEP = 50
    OVERLAP_MIN = 0
    OVERLAP_MAX = 100
    OVERLAP_STEP = 10

    # Retrieval defaults
    DEFAULT_TOP_K = 4
    TOP_K_MIN = 1
    TOP_K_MAX = 10

    # BM25 defaults
    DEFAULT_K1 = 1.5
    DEFAULT_B = 0.75
    K1_MIN = 0.5
    K1_MAX = 3.0
    K1_STEP = 0.1
    B_MIN = 0.0
    B_MAX = 1.0
    B_STEP = 0.05

    # LLM generation settings
    MAX_TOKENS = 800
    TEMPERATURE = 0.2

    @classmethod
    def is_api_key_configured(cls) -> bool:
        """Check if Groq API key is available."""
        return bool(cls.GROQ_API_KEY)

    @classmethod
    def get_api_key_masked(cls) -> str:
        """Return masked API key for display (show first/last 4 chars)."""
        if not cls.GROQ_API_KEY:
            return ""
        key = cls.GROQ_API_KEY
        if len(key) <= 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"
