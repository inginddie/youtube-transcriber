"""Tests for logging integration in utils and rag_engine"""

from pathlib import Path
from unittest.mock import patch


class TestUtilsLogging:
    def test_cleanup_temp_files_logs_warning_on_error(self, tmp_path):
        """utils.cleanup_temp_files uses logger.warning, not print, on OSError."""
        # Create a file that we'll make fail to delete
        test_file = tmp_path / "test.mp3"
        test_file.write_text("data")

        with patch("src.utils.logger") as mock_logger, patch.object(
            Path, "unlink", side_effect=OSError("permission denied")
        ):
            from src.utils import cleanup_temp_files

            cleanup_temp_files(tmp_path)

            mock_logger.warning.assert_called_once()
            assert "permission denied" in mock_logger.warning.call_args[0][0]


class TestRagEngineLogging:
    def test_load_transcripts_logs_on_bad_json(self, tmp_path):
        """rag_engine.load_transcripts uses logger.exception, not print, on bad JSON."""
        pytest = __import__("pytest")
        try:
            import langchain  # noqa: F401
        except ImportError:
            pytest.skip("langchain not installed")

        import src.rag_engine as rag_mod

        # Create a bad JSON file
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{invalid json")

        with patch.object(rag_mod, "TRANSCRIPTS_DIR", tmp_path), patch.object(
            rag_mod, "logger"
        ) as mock_logger, patch.object(rag_mod, "OpenAIEmbeddings"), patch.object(
            rag_mod, "ChatOpenAI"
        ), patch.object(
            rag_mod, "ConversationBufferMemory"
        ):
            rag = rag_mod.RAGEngine()
            result = rag.load_transcripts()

        assert result == []
        mock_logger.exception.assert_called_once()
        assert "bad.json" in mock_logger.exception.call_args[0][0]
