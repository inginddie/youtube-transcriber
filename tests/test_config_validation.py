"""Tests for config.validate_config()"""

import pytest

import config


def test_valid_defaults_pass():
    """Default config values should pass validation."""
    config.validate_config()


def test_invalid_chunk_size(monkeypatch):
    """CHUNK_SIZE out of range raises ValueError."""
    monkeypatch.setattr(config, "CHUNK_SIZE", 50)
    with pytest.raises(ValueError, match="CHUNK_SIZE"):
        config.validate_config()


def test_chunk_overlap_exceeds_chunk_size(monkeypatch):
    """CHUNK_OVERLAP >= CHUNK_SIZE raises ValueError."""
    monkeypatch.setattr(config, "CHUNK_SIZE", 1000)
    monkeypatch.setattr(config, "CHUNK_OVERLAP", 1000)
    with pytest.raises(ValueError, match="CHUNK_OVERLAP"):
        config.validate_config()


def test_invalid_temperature(monkeypatch):
    """TEMPERATURE > 2.0 raises ValueError."""
    monkeypatch.setattr(config, "TEMPERATURE", 2.5)
    with pytest.raises(ValueError, match="TEMPERATURE"):
        config.validate_config()


def test_invalid_top_k(monkeypatch):
    """TOP_K_RESULTS = 0 raises ValueError."""
    monkeypatch.setattr(config, "TOP_K_RESULTS", 0)
    with pytest.raises(ValueError, match="TOP_K_RESULTS"):
        config.validate_config()


def test_invalid_max_retries(monkeypatch):
    """MAX_RETRIES = 0 raises ValueError."""
    monkeypatch.setattr(config, "MAX_RETRIES", 0)
    with pytest.raises(ValueError, match="MAX_RETRIES"):
        config.validate_config()


def test_invalid_retry_delay(monkeypatch):
    """Negative RETRY_DELAY raises ValueError."""
    monkeypatch.setattr(config, "RETRY_DELAY", -1)
    with pytest.raises(ValueError, match="RETRY_DELAY"):
        config.validate_config()
