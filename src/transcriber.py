"""
Core transcription engine for YouTube Transcriber Pro
"""
import os
import time
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, Callable
import yt_dlp
from openai import OpenAI

from src.logger import setup_logger

# Setup logger
logger = setup_logger("transcriber")

from config import (
    OPENAI_API_KEY,
    WHISPER_MODEL,
    TEMP_AUDIO_DIR,
    TRANSCRIPTS_DIR,
    AUDIO_FORMAT,
    AUDIO_QUALITY,
    MAX_RETRIES,
    RETRY_DELAY
)
from src.utils import (
    extract_video_id,
    sanitize_filename,
    save_transcript,
    cleanup_temp_files,
    format_timestamp,
    count_words
)


class YouTubeTranscriber:
    """Main transcriber class"""
    
    # Cache para la ubicación de FFmpeg
    _ffmpeg_location_cache = None
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.temp_dir = TEMP_AUDIO_DIR
        self.output_dir = TRANSCRIPTS_DIR
        
        # Encontrar FFmpeg una sola vez al inicializar
        if YouTubeTranscriber._ffmpeg_location_cache is None:
            YouTubeTranscriber._ffmpeg_location_cache = self._find_ffmpeg()
            if not YouTubeTranscriber._ffmpeg_location_cache:
                raise Exception(
                    "FFmpeg no encontrado. Por favor instala FFmpeg:\n"
                    "  - Windows: winget install ffmpeg\n"
                    "  - Luego reinicia PowerShell\n"
                    "  - O descarga de: https://ffmpeg.org/download.html"
                )
    
    def _find_ffmpeg(self) -> Optional[str]:
        """
        Find FFmpeg installation on the system
        
        Returns:
            Path to FFmpeg directory or None if not found
        """
        # Method 1: Check if ffmpeg is in PATH
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            return str(Path(ffmpeg_path).parent)
        
        # Method 2: Check specific known locations (faster than recursive search)
        import os
        specific_paths = [
            # WinGet common location
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Packages' / 'Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe' / 'ffmpeg-8.0-full_build' / 'bin',
            # Chocolatey
            Path('C:/ProgramData/chocolatey/bin'),
            # Manual installation
            Path('C:/ffmpeg/bin'),
            Path('C:/Program Files/ffmpeg/bin'),
        ]
        
        for path in specific_paths:
            if path.exists() and (path / 'ffmpeg.exe').exists():
                return str(path)
        
        # Method 3: Quick recursive search only in WinGet packages (limited depth)
        winget_packages = Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Packages'
        if winget_packages.exists():
            for item in winget_packages.iterdir():
                if 'ffmpeg' in item.name.lower():
                    # Search only 2 levels deep
                    for root, dirs, files in os.walk(item):
                        if 'ffmpeg.exe' in files:
                            return root
                        # Limit depth
                        if root.count(os.sep) - str(item).count(os.sep) > 2:
                            del dirs[:]
        
        return None
    
    def download_audio(self, url: str, progress_callback: Optional[Callable] = None) -> Optional[Path]:
        """
        Download audio from YouTube video
        
        Args:
            url: YouTube video URL
            progress_callback: Optional callback for progress updates
            
        Returns:
            Path to downloaded audio file or None if failed
        """
        logger.info(f"📥 Starting download for URL: {url}")
        
        video_id = extract_video_id(url)
        if not video_id:
            logger.error(f"Invalid YouTube URL: {url}")
            raise ValueError(f"Invalid YouTube URL: {url}")
        
        logger.info(f"🎬 Video ID extracted: {video_id}")
        output_path = self.temp_dir / f"{video_id}.{AUDIO_FORMAT}"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': AUDIO_FORMAT,
                'preferredquality': AUDIO_QUALITY,
            }],
            'outtmpl': str(self.temp_dir / f"{video_id}.%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': YouTubeTranscriber._ffmpeg_location_cache,
            # Configuraciones anti-bot más agresivas
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
            },
            # Usar cliente Android (más difícil de bloquear)
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web'],
                    'skip': ['hls', 'dash'],
                }
            },
        }
        
        # Si falla con Chrome, intentar sin cookies
        try:
            # Primer intento con cookies de Chrome
            pass
        except:
            # Si falla, remover cookies y usar solo headers
            if 'cookiesfrombrowser' in ydl_opts:
                del ydl_opts['cookiesfrombrowser']
        
        if progress_callback:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    progress_callback(f"Downloading: {d.get('_percent_str', 'N/A')}")
                elif d['status'] == 'finished':
                    progress_callback("Download complete, converting...")
            
            ydl_opts['progress_hooks'] = [progress_hook]
        
        # Intentar múltiples estrategias de descarga
        # Orden optimizado: primero sin cookies (para servidores), luego con cookies (para local)
        strategies = [
            # Estrategia 1: Sin cookies, solo headers avanzados (mejor para servidores)
            {'remove_cookies': True},
            # Estrategia 2: Modo básico sin opciones avanzadas
            {'remove_cookies': True, 'basic_mode': True},
            # Estrategia 3: Con cookies de Chrome (solo funciona si Chrome está instalado)
            {'cookiesfrombrowser': ('chrome',)},
            # Estrategia 4: Con cookies de Firefox (solo funciona si Firefox está instalado)
            {'cookiesfrombrowser': ('firefox',)},
        ]
        
        last_error = None
        
        for i, strategy in enumerate(strategies, 1):
            try:
                logger.info(f"🔧 Strategy {i}/{len(strategies)}: Configuring yt-dlp with FFmpeg: {YouTubeTranscriber._ffmpeg_location_cache}")
                
                # Aplicar estrategia actual
                current_opts = ydl_opts.copy()
                
                # Remover cookiesfrombrowser si la estrategia lo requiere
                if strategy.get('remove_cookies'):
                    current_opts.pop('cookiesfrombrowser', None)
                
                # Modo básico: remover opciones avanzadas
                if strategy.get('basic_mode'):
                    current_opts.pop('user_agent', None)
                    current_opts.pop('http_headers', None)
                    current_opts.pop('extractor_args', None)
                
                # Agregar cookies si la estrategia lo especifica
                if 'cookiesfrombrowser' in strategy:
                    current_opts['cookiesfrombrowser'] = strategy['cookiesfrombrowser']
                
                with yt_dlp.YoutubeDL(current_opts) as ydl:
                    logger.info("⬇️  Downloading video metadata...")
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)
                    
                    logger.info(f"✅ Download complete: {title}")
                    logger.info(f"⏱️  Duration: {duration // 60}m {duration % 60}s")
                    
                    file_size_mb = output_path.stat().st_size / (1024 * 1024)
                    logger.info(f"📦 Audio file size: {file_size_mb:.2f}MB")
                    
                    if progress_callback:
                        progress_callback(f"Downloaded: {title}")
                    
                    return output_path, title
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"⚠️  Strategy {i} failed: {last_error}")
                
                # Si el error es de cookies no encontradas, skip silenciosamente
                if "could not find" in last_error.lower() and "cookies" in last_error.lower():
                    logger.info(f"⏭️  Skipping cookie-based strategy (browser not available)")
                    if i < len(strategies):
                        continue
                
                if i < len(strategies):
                    logger.info(f"🔄 Trying next strategy...")
                    continue  # Intentar siguiente estrategia
                else:
                    # Todas las estrategias fallaron
                    logger.error(f"❌ All {len(strategies)} strategies failed")
                    
                    # Mensaje más útil si es detección de bot
                    if "bot" in last_error.lower() or "sign in" in last_error.lower():
                        raise Exception(
                            f"YouTube is blocking this video (bot detection). "
                            f"This video may require authentication or may be age-restricted. "
                            f"Try a different video or contact support. Error: {last_error}"
                        )
                    else:
                        raise Exception(f"Failed to download audio after {len(strategies)} attempts. Last error: {last_error}")
    
    def _split_audio(self, audio_path: Path, max_size_mb: float = 24) -> list[Path]:
        """
        Split audio file into chunks if it's too large
        
        Args:
            audio_path: Path to audio file
            max_size_mb: Maximum size per chunk in MB
            
        Returns:
            List of audio chunk paths
        """
        import subprocess
        
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        logger.info(f"📊 Audio file size: {file_size_mb:.2f}MB")
        
        if file_size_mb <= max_size_mb:
            logger.info("✅ File size OK, no splitting needed")
            return [audio_path]
        
        # Calculate number of chunks needed
        num_chunks = int(file_size_mb / max_size_mb) + 1
        logger.info(f"✂️  Splitting audio into {num_chunks} chunks...")
        
        # Get audio duration using ffprobe
        # Detectar si estamos en Windows o Linux
        ffprobe_name = "ffprobe.exe" if os.name == 'nt' else "ffprobe"
        
        # Si ffmpeg_location es un directorio, agregar el nombre del ejecutable
        if YouTubeTranscriber._ffmpeg_location_cache and Path(YouTubeTranscriber._ffmpeg_location_cache).is_dir():
            ffprobe_path = Path(YouTubeTranscriber._ffmpeg_location_cache) / ffprobe_name
        else:
            # Si no es un directorio, usar solo el nombre (está en PATH)
            ffprobe_path = ffprobe_name
        
        result = subprocess.run(
            [str(ffprobe_path), "-v", "error", "-show_entries", 
             "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", 
             str(audio_path)],
            capture_output=True,
            text=True
        )
        
        duration = float(result.stdout.strip())
        chunk_duration = duration / num_chunks
        
        # Split audio into chunks
        chunks = []
        
        # Detectar si estamos en Windows o Linux para ffmpeg
        ffmpeg_name = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
        
        # Si ffmpeg_location es un directorio, agregar el nombre del ejecutable
        if YouTubeTranscriber._ffmpeg_location_cache and Path(YouTubeTranscriber._ffmpeg_location_cache).is_dir():
            ffmpeg_path = Path(YouTubeTranscriber._ffmpeg_location_cache) / ffmpeg_name
        else:
            # Si no es un directorio, usar solo el nombre (está en PATH)
            ffmpeg_path = ffmpeg_name
        
        for i in range(num_chunks):
            start_time = i * chunk_duration
            chunk_path = audio_path.parent / f"{audio_path.stem}_chunk{i}{audio_path.suffix}"
            
            logger.info(f"✂️  Creating chunk {i+1}/{num_chunks} (start: {start_time:.1f}s, duration: {chunk_duration:.1f}s)")
            
            subprocess.run(
                [str(ffmpeg_path), "-i", str(audio_path), 
                 "-ss", str(start_time), "-t", str(chunk_duration),
                 "-c", "copy", str(chunk_path), "-y"],
                capture_output=True
            )
            
            chunk_size_mb = chunk_path.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Chunk {i+1} created: {chunk_size_mb:.2f}MB")
            
            chunks.append(chunk_path)
        
        logger.info(f"✅ All {num_chunks} chunks created successfully")
        return chunks
    
    def transcribe_audio(self, audio_path: Path, progress_callback: Optional[Callable] = None) -> str:
        """
        Transcribe audio file using OpenAI Whisper
        
        Args:
            audio_path: Path to audio file
            progress_callback: Optional callback for progress updates
            
        Returns:
            Transcription text
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Check file size (Whisper API limit is 25MB)
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > 25:
            logger.warning(f"⚠️  File exceeds 25MB limit, splitting required")
            if progress_callback:
                progress_callback(f"Audio file is {file_size_mb:.2f}MB, splitting into chunks...")
            
            # Split audio into chunks
            chunks = self._split_audio(audio_path)
            
            logger.info(f"📦 Processing {len(chunks)} chunks...")
            if progress_callback:
                progress_callback(f"Split into {len(chunks)} chunks, transcribing...")
            
            # Transcribe each chunk
            transcripts = []
            for i, chunk_path in enumerate(chunks, 1):
                logger.info(f"🎯 Processing chunk {i}/{len(chunks)}")
                if progress_callback:
                    progress_callback(f"Transcribing chunk {i}/{len(chunks)}...")
                
                chunk_transcript = self._transcribe_single_file(chunk_path, progress_callback)
                transcripts.append(chunk_transcript)
                
                # Clean up chunk
                logger.info(f"🗑️  Cleaning up chunk {i}")
                chunk_path.unlink()
                
                # Rate limiting: Wait between chunks to avoid 429 errors
                if i < len(chunks):
                    wait_time = 5  # seconds
                    logger.info(f"⏳ Waiting {wait_time}s before next chunk (rate limiting)...")
                    if progress_callback:
                        progress_callback(f"Waiting {wait_time}s to avoid rate limits...")
                    time.sleep(wait_time)
            
            # Combine transcripts
            full_transcript = " ".join(transcripts)
            total_words = len(full_transcript.split())
            
            logger.info(f"✅ All chunks combined: {total_words} total words")
            if progress_callback:
                progress_callback("All chunks transcribed and combined!")
            
            return full_transcript
        else:
            return self._transcribe_single_file(audio_path, progress_callback)
    
    def _transcribe_single_file(self, audio_path: Path, progress_callback: Optional[Callable] = None) -> str:
        """
        Transcribe a single audio file (must be under 25MB)
        
        Args:
            audio_path: Path to audio file
            progress_callback: Optional callback for progress updates
            
        Returns:
            Transcription text
        """
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        logger.info(f"🎤 Transcribing file: {audio_path.name} ({file_size_mb:.2f}MB)")
        
        if progress_callback:
            progress_callback("Transcribing with Whisper API...")
        
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"🔄 Attempt {attempt + 1}/{MAX_RETRIES} - Calling Whisper API...")
                start_time = time.time()
                
                with open(audio_path, 'rb') as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model=WHISPER_MODEL,
                        file=audio_file,
                        response_format="text"
                    )
                
                elapsed_time = time.time() - start_time
                word_count = len(transcript.split())
                
                logger.info(f"✅ Transcription complete in {elapsed_time:.1f}s")
                logger.info(f"📝 Words transcribed: {word_count}")
                
                if progress_callback:
                    progress_callback("Transcription complete!")
                
                return transcript
            
            except Exception as e:
                error_str = str(e)
                logger.warning(f"⚠️  Attempt {attempt + 1} failed: {error_str}")
                
                # Check if it's a rate limit error (429)
                is_rate_limit = "429" in error_str or "rate limit" in error_str.lower()
                
                if attempt < MAX_RETRIES - 1:
                    # Use exponential backoff for rate limits
                    if is_rate_limit:
                        wait_time = RETRY_DELAY * (2 ** attempt) * 2  # Double wait for rate limits
                        logger.warning(f"🚦 Rate limit detected! Waiting {wait_time}s...")
                        if progress_callback:
                            progress_callback(f"Rate limit - waiting {wait_time}s...")
                    else:
                        wait_time = RETRY_DELAY
                        logger.info(f"⏳ Waiting {wait_time}s before retry...")
                        if progress_callback:
                            progress_callback(f"Retry {attempt + 1}/{MAX_RETRIES}...")
                    
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ Transcription failed after {MAX_RETRIES} attempts")
                    raise Exception(f"Transcription failed after {MAX_RETRIES} attempts: {str(e)}")
    
    def _check_if_already_transcribed(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Check if a video has already been transcribed
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary with existing transcript info or None if not found
        """
        import json
        
        # Search for existing transcripts with this video_id
        for json_file in self.output_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if data.get('video_id') == video_id:
                    # Found existing transcript
                    txt_file = json_file.with_suffix('.txt')
                    
                    return {
                        'video_id': video_id,
                        'title': data.get('title', 'Unknown'),
                        'json_path': str(json_file),
                        'txt_path': str(txt_file) if txt_file.exists() else None,
                        'word_count': data.get('word_count', 0),
                        'timestamp': data.get('timestamp', 'Unknown')
                    }
            except Exception as e:
                logger.debug(f"Error reading {json_file}: {e}")
                continue
        
        return None
    
    def process_video(
        self, 
        url: str, 
        index: int = 1, 
        progress_callback: Optional[Callable] = None,
        skip_if_exists: bool = True
    ) -> Dict[str, Any]:
        """
        Process a single video: download, transcribe, and save
        
        Args:
            url: YouTube video URL
            index: File index number
            progress_callback: Optional callback for progress updates
            skip_if_exists: Skip if video already transcribed (default: True)
            
        Returns:
            Dictionary with processing results
        """
        logger.info("=" * 80)
        logger.info(f"🎬 PROCESSING VIDEO #{index}")
        logger.info("=" * 80)
        
        try:
            # Extract video ID
            video_id = extract_video_id(url)
            if not video_id:
                logger.error("Invalid YouTube URL")
                raise ValueError("Invalid YouTube URL")
            
            logger.info(f"🆔 Video ID: {video_id}")
            logger.info(f"🔗 URL: {url}")
            
            # Check if already transcribed
            if skip_if_exists:
                logger.info("🔍 Checking for existing transcript...")
                existing = self._check_if_already_transcribed(video_id)
                
                if existing:
                    logger.info("=" * 80)
                    logger.info(f"⏭️  VIDEO ALREADY TRANSCRIBED - SKIPPING")
                    logger.info(f"📄 Title: {existing['title']}")
                    logger.info(f"📅 Transcribed: {existing['timestamp']}")
                    logger.info(f"📁 JSON: {existing['json_path']}")
                    if existing['txt_path']:
                        logger.info(f"📁 TXT: {existing['txt_path']}")
                    logger.info("=" * 80)
                    
                    if progress_callback:
                        progress_callback(f"⏭️  Skipped: {existing['title']} (already transcribed)")
                    
                    return {
                        "success": True,
                        "skipped": True,
                        "video_id": video_id,
                        "title": existing['title'],
                        "json_path": existing['json_path'],
                        "txt_path": existing['txt_path'],
                        "word_count": existing['word_count'],
                        "message": "Video already transcribed"
                    }
                else:
                    logger.info("✅ No existing transcript found, proceeding...")
            
            if progress_callback:
                progress_callback(f"Processing video {index}: {video_id}")
            
            # Download audio
            audio_path, title = self.download_audio(url, progress_callback)
            
            # Transcribe
            transcript_text = self.transcribe_audio(audio_path, progress_callback)
            
            # Prepare data
            data = {
                "video_id": video_id,
                "url": url,
                "title": title,
                "language": None,  # Whisper auto-detects but doesn't return it in text mode
                "transcript": transcript_text,
                "timestamp": format_timestamp(),
                "index": index,
                "word_count": count_words(transcript_text)
            }
            
            # Save files
            logger.info("💾 Saving transcript files...")
            if progress_callback:
                progress_callback("Saving transcript files...")
            
            json_path, txt_path = save_transcript(data, self.output_dir, index)
            
            logger.info(f"✅ JSON saved: {json_path.name}")
            logger.info(f"✅ TXT saved: {txt_path.name}")
            
            # Cleanup temp audio
            if audio_path.exists():
                logger.info("🗑️  Cleaning up temporary audio file...")
                audio_path.unlink()
            
            logger.info("=" * 80)
            logger.info(f"✅ VIDEO #{index} COMPLETED SUCCESSFULLY")
            logger.info(f"📊 Total words: {data['word_count']}")
            logger.info("=" * 80)
            
            if progress_callback:
                progress_callback(f"✅ Completed: {title}")
            
            return {
                "success": True,
                "video_id": video_id,
                "title": title,
                "json_path": str(json_path),
                "txt_path": str(txt_path),
                "word_count": data["word_count"]
            }
        
        except Exception as e:
            logger.error("=" * 80)
            logger.error(f"❌ VIDEO #{index} FAILED")
            logger.error(f"Error: {str(e)}")
            logger.error("=" * 80)
            
            if progress_callback:
                progress_callback(f"❌ Error: {str(e)}")
            
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    def process_multiple_videos(
        self, 
        urls: list[str], 
        progress_callback: Optional[Callable] = None,
        skip_if_exists: bool = True
    ) -> list[Dict[str, Any]]:
        """
        Process multiple videos sequentially
        
        Args:
            urls: List of YouTube video URLs
            progress_callback: Optional callback for progress updates
            skip_if_exists: Skip videos that are already transcribed
            
        Returns:
            List of processing results
        """
        results = []
        
        # Check for duplicates in the input list
        seen_video_ids = set()
        unique_urls = []
        duplicate_urls = []
        
        for url in urls:
            video_id = extract_video_id(url)
            if video_id:
                if video_id in seen_video_ids:
                    duplicate_urls.append(url)
                    logger.warning(f"⚠️  Duplicate URL in list: {url} (Video ID: {video_id})")
                else:
                    seen_video_ids.add(video_id)
                    unique_urls.append(url)
            else:
                logger.warning(f"⚠️  Invalid URL skipped: {url}")
        
        if duplicate_urls:
            logger.info(f"🔍 Found {len(duplicate_urls)} duplicate URLs in input list (removed)")
        
        logger.info(f"📊 Processing {len(unique_urls)} unique videos")
        
        for i, url in enumerate(unique_urls, 1):
            if progress_callback:
                progress_callback(f"\n{'='*60}\nProcessing {i}/{len(unique_urls)}\n{'='*60}")
            
            result = self.process_video(url, i, progress_callback, skip_if_exists)
            results.append(result)
            
            # Small delay between videos (rate limiting)
            if i < len(unique_urls):
                time.sleep(2)
        
        # Final cleanup
        cleanup_temp_files(self.temp_dir)
        
        # Print summary
        logger.info("=" * 80)
        logger.info("📊 PROCESSING SUMMARY")
        logger.info("=" * 80)
        
        transcribed = [r for r in results if r.get('success') and not r.get('skipped')]
        skipped = [r for r in results if r.get('success') and r.get('skipped')]
        failed = [r for r in results if not r.get('success')]
        
        logger.info(f"✅ Newly transcribed: {len(transcribed)}")
        logger.info(f"⏭️  Skipped (already exist): {len(skipped)}")
        logger.info(f"❌ Failed: {len(failed)}")
        logger.info(f"📝 Total processed: {len(results)}")
        
        if duplicate_urls:
            logger.info(f"🔍 Duplicates removed from input: {len(duplicate_urls)}")
        
        logger.info("=" * 80)
        
        return results
