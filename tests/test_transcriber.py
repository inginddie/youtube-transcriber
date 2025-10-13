"""
Unit tests for transcriber module
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile

from src.transcriber import YouTubeTranscriber


class TestYouTubeTranscriber:
    """Tests for YouTubeTranscriber class"""
    
    @pytest.fixture
    def transcriber(self):
        """Create transcriber instance for testing"""
        with patch('src.transcriber.OpenAI'):
            return YouTubeTranscriber()
    
    def test_initialization(self, transcriber):
        """Test transcriber initializes correctly"""
        assert transcriber.temp_dir is not None
        assert transcriber.output_dir is not None
    
    @patch('src.transcriber.yt_dlp.YoutubeDL')
    def test_download_audio_success(self, mock_ydl, transcriber):
        """Test successful audio download"""
        # Mock yt-dlp
        mock_instance = MagicMock()
        mock_instance.extract_info.return_value = {
            'title': 'Test Video',
            'id': 'test123'
        }
        mock_ydl.return_value.__enter__.return_value = mock_instance
        
        url = "https://youtu.be/test123"
        
        with tempfile.TemporaryDirectory() as tmpdir:
            transcriber.temp_dir = Path(tmpdir)
            
            # Create mock audio file
            audio_path = transcriber.temp_dir / "test123.mp3"
            audio_path.touch()
            
            result, title = transcriber.download_audio(url)
            
            assert title == "Test Video"
    
    def test_download_audio_invalid_url(self, transcriber):
        """Test download with invalid URL"""
        url = "https://www.google.com"
        
        with pytest.raises(ValueError, match="Invalid YouTube URL"):
            transcriber.download_audio(url)
    
    @patch('src.transcriber.OpenAI')
    def test_transcribe_audio_file_not_found(self, mock_openai, transcriber):
        """Test transcription with non-existent file"""
        audio_path = Path("/nonexistent/file.mp3")
        
        with pytest.raises(FileNotFoundError):
            transcriber.transcribe_audio(audio_path)
    
    @patch('src.transcriber.OpenAI')
    def test_transcribe_audio_file_too_large(self, mock_openai, transcriber):
        """Test transcription with file exceeding size limit"""
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
            # Create a file larger than 25MB
            tmp.write(b'0' * (26 * 1024 * 1024))
            tmp_path = Path(tmp.name)
        
        try:
            with pytest.raises(ValueError, match="Audio file too large"):
                transcriber.transcribe_audio(tmp_path)
        finally:
            tmp_path.unlink()
    
    def test_process_video_invalid_url(self, transcriber):
        """Test processing with invalid URL"""
        result = transcriber.process_video("https://www.google.com", 1)
        
        assert result['success'] is False
        assert 'error' in result
    
    @patch.object(YouTubeTranscriber, 'download_audio')
    @patch.object(YouTubeTranscriber, 'transcribe_audio')
    @patch('src.transcriber.save_transcript')
    def test_process_video_success(
        self, 
        mock_save, 
        mock_transcribe, 
        mock_download, 
        transcriber
    ):
        """Test successful video processing"""
        # Setup mocks
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = Path(tmpdir) / "test.mp3"
            audio_path.touch()
            
            mock_download.return_value = (audio_path, "Test Video")
            mock_transcribe.return_value = "This is a test transcript"
            mock_save.return_value = (Path("test.json"), Path("test.txt"))
            
            result = transcriber.process_video("https://youtu.be/test123", 1)
            
            assert result['success'] is True
            assert result['title'] == "Test Video"
            assert 'word_count' in result
    
    def test_process_multiple_videos(self, transcriber):
        """Test processing multiple videos"""
        urls = [
            "https://youtu.be/test1",
            "https://youtu.be/test2"
        ]
        
        with patch.object(transcriber, 'process_video') as mock_process:
            mock_process.return_value = {'success': True, 'title': 'Test'}
            
            results = transcriber.process_multiple_videos(urls)
            
            assert len(results) == 2
            assert mock_process.call_count == 2
