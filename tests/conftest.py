"""
Pytest configuration and fixtures
"""
import pytest
import os
from pathlib import Path


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing"""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-for-testing")


@pytest.fixture
def sample_transcript_data():
    """Sample transcript data for testing"""
    return {
        "video_id": "test123",
        "url": "https://youtu.be/test123",
        "title": "Test Video Title",
        "language": "en",
        "transcript": "This is a sample transcript for testing purposes.",
        "timestamp": "2025-10-12T10:00:00",
        "index": 1,
        "word_count": 8
    }


@pytest.fixture
def sample_urls():
    """Sample YouTube URLs for testing"""
    return [
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=abc123def45",
        "https://youtu.be/xyz789uvw12"
    ]
