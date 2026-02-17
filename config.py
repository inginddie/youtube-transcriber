"""
Configuration module for YouTube Transcriber Pro
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

_config_logger = logging.getLogger("config")

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Note: API key validation is done at runtime, not import time
# This allows Docker builds to succeed without the key

# Model Configuration
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4-turbo-preview")

# Directory Configuration
BASE_DIR = Path(__file__).parent
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
TEMP_AUDIO_DIR = BASE_DIR / "temp_audio"
VECTOR_DB_DIR = BASE_DIR / "vector_db"

# Transcription Configuration
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = "192"

# RAG Configuration (Phase 2)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3
TEMPERATURE = 0.7

# Gradio Configuration
GRADIO_PORT = 7860
GRADIO_SHARE = False

# Rate Limiting
MAX_RETRIES = 5  # Increased for rate limit handling
RETRY_DELAY = 3  # seconds (will use exponential backoff for rate limits)


def validate_config():
    """Validate configuration values for types and ranges."""
    if not isinstance(CHUNK_SIZE, int) or not (100 <= CHUNK_SIZE <= 10000):
        raise ValueError(
            f"CHUNK_SIZE must be an int between 100 and 10000, got {CHUNK_SIZE!r}"
        )
    if not isinstance(CHUNK_OVERLAP, int) or CHUNK_OVERLAP < 0 or CHUNK_OVERLAP >= CHUNK_SIZE:
        raise ValueError(
            f"CHUNK_OVERLAP must be an int >= 0 and < CHUNK_SIZE ({CHUNK_SIZE}), got {CHUNK_OVERLAP!r}"
        )
    if not isinstance(TOP_K_RESULTS, int) or not (1 <= TOP_K_RESULTS <= 20):
        raise ValueError(f"TOP_K_RESULTS must be an int between 1 and 20, got {TOP_K_RESULTS!r}")
    if not isinstance(TEMPERATURE, (int, float)) or not (0.0 <= TEMPERATURE <= 2.0):
        raise ValueError(f"TEMPERATURE must be a float between 0.0 and 2.0, got {TEMPERATURE!r}")
    if not isinstance(MAX_RETRIES, int) or not (1 <= MAX_RETRIES <= 20):
        raise ValueError(f"MAX_RETRIES must be an int between 1 and 20, got {MAX_RETRIES!r}")
    if not isinstance(RETRY_DELAY, (int, float)) or not (0 <= RETRY_DELAY <= 60):
        raise ValueError(f"RETRY_DELAY must be a number between 0 and 60, got {RETRY_DELAY!r}")
    _config_logger.debug("Configuration validated successfully")


def create_directories():
    """Create necessary directories if they don't exist"""
    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    TEMP_AUDIO_DIR.mkdir(exist_ok=True)
    VECTOR_DB_DIR.mkdir(exist_ok=True)

    # Create .gitkeep files
    (TEMP_AUDIO_DIR / ".gitkeep").touch()
    (VECTOR_DB_DIR / ".gitkeep").touch()
