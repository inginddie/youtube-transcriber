"""
Configuration module for YouTube Transcriber Pro
"""
import os
from pathlib import Path
from dotenv import load_dotenv

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

def create_directories():
    """Create necessary directories if they don't exist"""
    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    TEMP_AUDIO_DIR.mkdir(exist_ok=True)
    VECTOR_DB_DIR.mkdir(exist_ok=True)
    
    # Create .gitkeep files
    (TEMP_AUDIO_DIR / ".gitkeep").touch()
    (VECTOR_DB_DIR / ".gitkeep").touch()
