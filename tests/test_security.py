"""Tests for src.security SecurityManager"""

import time

import pytest

from src.security import SecurityManager


@pytest.fixture
def manager():
    return SecurityManager()


class TestRateLimiter:
    def test_allows_under_limit(self, manager):
        allowed, _ = manager.search_limiter.is_allowed("user1")
        assert allowed is True

    def test_blocks_over_limit(self):
        from src.security import RateLimiter

        limiter = RateLimiter(max_requests=2, window_seconds=60)
        limiter.is_allowed("u")
        limiter.is_allowed("u")
        allowed, wait = limiter.is_allowed("u")
        assert allowed is False
        assert wait is not None


class TestBlacklist:
    def test_add_and_check_blacklist(self, manager):
        manager.add_to_blacklist("bad_user")
        assert manager.is_blacklisted("bad_user") is True

    def test_blacklist_expires(self, manager):
        manager.blacklist_ttl = 1  # 1 second TTL
        manager.add_to_blacklist("temp_user")
        assert manager.is_blacklisted("temp_user") is True
        time.sleep(1.1)
        assert manager.is_blacklisted("temp_user") is False

    def test_remove_from_blacklist(self, manager):
        manager.add_to_blacklist("remove_me")
        assert manager.remove_from_blacklist("remove_me") is True
        assert manager.is_blacklisted("remove_me") is False

    def test_remove_nonexistent_returns_false(self, manager):
        assert manager.remove_from_blacklist("ghost") is False

    def test_cleanup_blacklist(self, manager):
        manager.blacklist_ttl = 1
        manager.add_to_blacklist("a")
        manager.add_to_blacklist("b")
        time.sleep(1.1)
        removed = manager.cleanup_blacklist()
        assert removed == 2
        assert len(manager.blacklist) == 0

    def test_failed_attempts_reset_on_remove(self, manager):
        manager.record_failed_attempt("user_x")
        manager.record_failed_attempt("user_x")
        manager.add_to_blacklist("user_x")
        manager.remove_from_blacklist("user_x")
        assert manager.failed_attempts.get("user_x", 0) == 0

    def test_record_failed_attempt_triggers_blacklist(self, manager):
        for _ in range(manager.max_failed_attempts):
            manager.record_failed_attempt("abuser")
        assert manager.is_blacklisted("abuser") is True
