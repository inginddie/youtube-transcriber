"""
Utility functions for YouTube Transcriber Pro
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from src.logger import setup_logger

logger = setup_logger("utils")


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL

    Args:
        url: YouTube URL

    Returns:
        Video ID or None if invalid
    """
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)",
        r"youtube\.com\/embed\/([^&\n?#]+)",
        r"youtube\.com\/v\/([^&\n?#]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """
    Sanitize filename by removing invalid characters

    Args:
        filename: Original filename
        max_length: Maximum length for filename

    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "", filename)
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Limit length
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename


def save_transcript(data: Dict[str, Any], output_dir: Path, index: int) -> tuple[Path, Path]:
    """
    Save transcript in JSON and TXT formats

    Args:
        data: Transcript data dictionary
        output_dir: Output directory path
        index: File index number

    Returns:
        Tuple of (json_path, txt_path)
    """
    # Create safe filename
    title = sanitize_filename(data.get("title", "untitled"))
    base_filename = f"{index:02d}_{title}"

    # Save JSON
    json_path = output_dir / f"{base_filename}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save TXT
    txt_path = output_dir / f"{base_filename}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {data.get('title', 'N/A')}\n")
        f.write(f"URL: {data.get('url', 'N/A')}\n")
        f.write(f"Video ID: {data.get('video_id', 'N/A')}\n")
        f.write(f"Language: {data.get('language', 'N/A')}\n")
        f.write(f"Timestamp: {data.get('timestamp', 'N/A')}\n")
        f.write(f"Word Count: {data.get('word_count', 0)}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        f.write(data.get("transcript", ""))

    return json_path, txt_path


def cleanup_temp_files(temp_dir: Path, keep_recent: int = 0):
    """
    Clean up temporary audio files

    Args:
        temp_dir: Temporary directory path
        keep_recent: Number of recent files to keep
    """
    if not temp_dir.exists():
        return

    files = sorted(temp_dir.glob("*"), key=os.path.getmtime, reverse=True)

    # Skip .gitkeep
    files = [f for f in files if f.name != ".gitkeep"]

    # Delete old files
    for file in files[keep_recent:]:
        try:
            file.unlink()
        except OSError as e:
            logger.warning(f"Could not delete {file}: {e}")


def format_timestamp() -> str:
    """
    Get current timestamp in ISO format

    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()


def count_words(text: str) -> int:
    """
    Count words in text

    Args:
        text: Input text

    Returns:
        Word count
    """
    return len(text.split())


def validate_url(url: str) -> bool:
    """
    Validate if URL is a valid YouTube URL

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    return extract_video_id(url) is not None


def parse_urls_input(urls_text: str) -> list[str]:
    """
    Parse URLs from text input (one per line)

    Args:
        urls_text: Text containing URLs

    Returns:
        List of valid URLs
    """
    lines = urls_text.strip().split("\n")
    urls = []

    for line in lines:
        line = line.strip()
        if line and validate_url(line):
            urls.append(line)

    return urls
