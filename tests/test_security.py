"""Tests for src.security SecurityManager"""

import time

import pytest

from src.security import SecurityManager


@pytest.fixture
def manager():
    return SecurityManager()


# ============================================================================
# AuthManager (consolidated session management)
# ============================================================================


class TestAuthManager:
    @pytest.fixture
    def auth_manager(self, manager):
        """AuthManager with require_auth=True for testing session logic."""
        manager.auth.require_auth = True
        return manager.auth

    def test_create_and_verify_session(self, auth_manager):
        sid = auth_manager.create_session("user1")
        assert auth_manager.verify_session(sid) is True

    def test_verify_expired_session(self, auth_manager):
        auth_manager.session_timeout = 1
        sid = auth_manager.create_session("user1")
        time.sleep(1.1)
        assert auth_manager.verify_session(sid) is False

    def test_get_session_returns_metadata(self, auth_manager):
        sid = auth_manager.create_session("user1")
        session = auth_manager.get_session(sid)
        assert session is not None
        assert session["user_id"] == "user1"
        assert session["authenticated"] is True
        assert "last_activity" in session

    def test_get_session_returns_none_for_invalid(self, auth_manager):
        assert auth_manager.get_session("bogus") is None

    def test_destroy_session(self, auth_manager):
        sid = auth_manager.create_session("user1")
        assert auth_manager.destroy_session(sid) is True
        assert auth_manager.verify_session(sid) is False

    def test_destroy_nonexistent_returns_false(self, auth_manager):
        assert auth_manager.destroy_session("nope") is False

    def test_cleanup_expired_sessions(self, auth_manager):
        auth_manager.session_timeout = 1
        auth_manager.create_session("a")
        auth_manager.create_session("b")
        time.sleep(1.1)
        removed = auth_manager.cleanup_expired_sessions()
        assert removed == 2
        assert len(auth_manager.sessions) == 0


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
