"""Tests for path traversal prevention via src.utils.is_safe_path."""

from pathlib import Path

from src.utils import is_safe_path


class TestIsSafePath:
    def test_valid_path_inside_allowed_dir(self, tmp_path):
        allowed = tmp_path / "transcripts"
        allowed.mkdir()
        target = allowed / "file.json"
        target.write_text("{}")
        assert is_safe_path(str(target), allowed) is True

    def test_path_traversal_blocked(self, tmp_path):
        allowed = tmp_path / "transcripts"
        allowed.mkdir()
        malicious = str(allowed / ".." / ".." / "etc" / "passwd")
        assert is_safe_path(malicious, allowed) is False

    def test_absolute_path_outside_dir_blocked(self, tmp_path):
        allowed = tmp_path / "transcripts"
        allowed.mkdir()
        outside = tmp_path / "secret.txt"
        outside.write_text("secret")
        assert is_safe_path(str(outside), allowed) is False

    def test_symlink_escape_blocked(self, tmp_path):
        allowed = tmp_path / "transcripts"
        allowed.mkdir()
        outside = tmp_path / "secret.txt"
        outside.write_text("secret")
        link = allowed / "link.txt"
        try:
            link.symlink_to(outside)
        except OSError:
            # Symlinks may not be supported (Windows without privileges)
            return
        assert is_safe_path(str(link), allowed) is False

    def test_empty_path(self, tmp_path):
        assert is_safe_path("", tmp_path) is False

    def test_nonexistent_but_within_dir(self, tmp_path):
        allowed = tmp_path / "transcripts"
        allowed.mkdir()
        # Nonexistent file within dir should be safe (for write operations)
        target = allowed / "new_file.json"
        assert is_safe_path(str(target), allowed) is True
