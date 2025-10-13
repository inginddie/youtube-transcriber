"""
Unit tests for utility functions
"""
import pytest
from pathlib import Path
import tempfile
import json

from src.utils import (
    extract_video_id,
    sanitize_filename,
    save_transcript,
    validate_url,
    parse_urls_input,
    count_words,
    format_timestamp
)


class TestExtractVideoId:
    """Tests for extract_video_id function"""
    
    def test_standard_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_embed_url(self):
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_url_with_params(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s"
        assert extract_video_id(url) == "dQw4w9WgXcQ"
    
    def test_invalid_url(self):
        url = "https://www.google.com"
        assert extract_video_id(url) is None


class TestSanitizeFilename:
    """Tests for sanitize_filename function"""
    
    def test_remove_invalid_chars(self):
        filename = 'test<>:"/\\|?*file'
        result = sanitize_filename(filename)
        assert '<' not in result
        assert '>' not in result
        assert ':' not in result
    
    def test_replace_spaces(self):
        filename = "test file name"
        result = sanitize_filename(filename)
        assert result == "test_file_name"
    
    def test_max_length(self):
        filename = "a" * 200
        result = sanitize_filename(filename, max_length=50)
        assert len(result) == 50


class TestValidateUrl:
    """Tests for validate_url function"""
    
    def test_valid_youtube_url(self):
        assert validate_url("https://youtu.be/dQw4w9WgXcQ") is True
        assert validate_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") is True
    
    def test_invalid_url(self):
        assert validate_url("https://www.google.com") is False
        assert validate_url("not a url") is False


class TestParseUrlsInput:
    """Tests for parse_urls_input function"""
    
    def test_single_url(self):
        text = "https://youtu.be/dQw4w9WgXcQ"
        urls = parse_urls_input(text)
        assert len(urls) == 1
        assert urls[0] == text
    
    def test_multiple_urls(self):
        text = """https://youtu.be/dQw4w9WgXcQ
https://youtu.be/abc123def45
https://youtu.be/xyz789uvw12"""
        urls = parse_urls_input(text)
        assert len(urls) == 3
    
    def test_mixed_valid_invalid(self):
        text = """https://youtu.be/dQw4w9WgXcQ
https://www.google.com
https://youtu.be/abc123def45"""
        urls = parse_urls_input(text)
        assert len(urls) == 2
    
    def test_empty_lines(self):
        text = """https://youtu.be/dQw4w9WgXcQ

https://youtu.be/abc123def45

"""
        urls = parse_urls_input(text)
        assert len(urls) == 2


class TestCountWords:
    """Tests for count_words function"""
    
    def test_simple_text(self):
        text = "Hello world this is a test"
        assert count_words(text) == 6
    
    def test_empty_text(self):
        assert count_words("") == 0
    
    def test_multiple_spaces(self):
        text = "Hello    world"
        assert count_words(text) >= 2


class TestFormatTimestamp:
    """Tests for format_timestamp function"""
    
    def test_returns_string(self):
        result = format_timestamp()
        assert isinstance(result, str)
    
    def test_iso_format(self):
        result = format_timestamp()
        assert 'T' in result  # ISO format contains T separator


class TestSaveTranscript:
    """Tests for save_transcript function"""
    
    def test_save_creates_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            
            data = {
                "video_id": "test123",
                "url": "https://youtu.be/test123",
                "title": "Test Video",
                "language": "en",
                "transcript": "This is a test transcript",
                "timestamp": "2025-10-12T10:00:00",
                "index": 1,
                "word_count": 5
            }
            
            json_path, txt_path = save_transcript(data, output_dir, 1)
            
            assert json_path.exists()
            assert txt_path.exists()
    
    def test_json_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            
            data = {
                "video_id": "test123",
                "title": "Test Video",
                "transcript": "Test content",
                "word_count": 2
            }
            
            json_path, _ = save_transcript(data, output_dir, 1)
            
            with open(json_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            assert loaded_data['video_id'] == "test123"
            assert loaded_data['title'] == "Test Video"
    
    def test_txt_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            
            data = {
                "video_id": "test123",
                "title": "Test Video",
                "url": "https://youtu.be/test123",
                "transcript": "Test transcript content",
                "word_count": 3
            }
            
            _, txt_path = save_transcript(data, output_dir, 1)
            
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "Test Video" in content
            assert "Test transcript content" in content
