"""
Unit tests for configuration module
"""

import os
import tempfile
from pathlib import Path

import pytest

from config import create_directories


class TestConfiguration:
    """Tests for configuration functions"""

    def test_create_directories(self):
        """Test directory creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Temporarily change config paths
            import config

            original_transcripts = config.TRANSCRIPTS_DIR
            original_temp = config.TEMP_AUDIO_DIR
            original_vector = config.VECTOR_DB_DIR

            try:
                config.TRANSCRIPTS_DIR = Path(tmpdir) / "transcripts"
                config.TEMP_AUDIO_DIR = Path(tmpdir) / "temp_audio"
                config.VECTOR_DB_DIR = Path(tmpdir) / "vector_db"

                create_directories()

                assert config.TRANSCRIPTS_DIR.exists()
                assert config.TEMP_AUDIO_DIR.exists()
                assert config.VECTOR_DB_DIR.exists()
                assert (config.TEMP_AUDIO_DIR / ".gitkeep").exists()
                assert (config.VECTOR_DB_DIR / ".gitkeep").exists()

            finally:
                config.TRANSCRIPTS_DIR = original_transcripts
                config.TEMP_AUDIO_DIR = original_temp
                config.VECTOR_DB_DIR = original_vector
