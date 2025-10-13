# API Documentation

## Core Modules

### `src.transcriber.YouTubeTranscriber`

Main class for transcribing YouTube videos.

#### Methods

##### `__init__()`
Initialize the transcriber with OpenAI client.

```python
transcriber = YouTubeTranscriber()
```

##### `download_audio(url: str, progress_callback: Optional[Callable] = None)`
Download audio from YouTube video.

**Parameters:**
- `url` (str): YouTube video URL
- `progress_callback` (Optional[Callable]): Callback function for progress updates

**Returns:**
- `Tuple[Path, str]`: Audio file path and video title

**Raises:**
- `ValueError`: If URL is invalid
- `Exception`: If download fails

**Example:**
```python
audio_path, title = transcriber.download_audio("https://youtu.be/VIDEO_ID")
```

##### `transcribe_audio(audio_path: Path, progress_callback: Optional[Callable] = None)`
Transcribe audio file using OpenAI Whisper.

**Parameters:**
- `audio_path` (Path): Path to audio file
- `progress_callback` (Optional[Callable]): Callback function for progress updates

**Returns:**
- `str`: Transcription text

**Raises:**
- `FileNotFoundError`: If audio file doesn't exist
- `ValueError`: If file exceeds 25MB limit
- `Exception`: If transcription fails

**Example:**
```python
transcript = transcriber.transcribe_audio(Path("audio.mp3"))
```

##### `process_video(url: str, index: int = 1, progress_callback: Optional[Callable] = None)`
Process a single video: download, transcribe, and save.

**Parameters:**
- `url` (str): YouTube video URL
- `index` (int): File index number
- `progress_callback` (Optional[Callable]): Callback function for progress updates

**Returns:**
- `Dict[str, Any]`: Processing results

**Example:**
```python
result = transcriber.process_video("https://youtu.be/VIDEO_ID", index=1)
if result['success']:
    print(f"Transcribed: {result['title']}")
```

##### `process_multiple_videos(urls: List[str], progress_callback: Optional[Callable] = None)`
Process multiple videos sequentially.

**Parameters:**
- `urls` (List[str]): List of YouTube video URLs
- `progress_callback` (Optional[Callable]): Callback function for progress updates

**Returns:**
- `List[Dict[str, Any]]`: List of processing results

**Example:**
```python
urls = ["https://youtu.be/VIDEO1", "https://youtu.be/VIDEO2"]
results = transcriber.process_multiple_videos(urls)
```

---

### `src.rag_engine.RAGEngine`

RAG engine for semantic search and chat (Phase 2).

#### Methods

##### `__init__()`
Initialize RAG engine with embeddings and LLM.

```python
rag = RAGEngine()
```

##### `load_transcripts()`
Load all transcript JSON files.

**Returns:**
- `List[Dict[str, Any]]`: List of transcript data

##### `index_transcripts(progress_callback: Optional[Callable] = None)`
Create vector embeddings and index all transcripts.

**Parameters:**
- `progress_callback` (Optional[Callable]): Callback function for progress updates

**Raises:**
- `ValueError`: If no transcripts found

**Example:**
```python
rag.index_transcripts()
```

##### `load_vector_store()`
Load existing vector store.

**Raises:**
- `ValueError`: If vector store not found

##### `setup_conversation_chain()`
Setup conversational retrieval chain.

**Raises:**
- `ValueError`: If vector store not initialized

##### `chat(question: str)`
Ask a question and get an answer with sources.

**Parameters:**
- `question` (str): User question

**Returns:**
- `Dict[str, Any]`: Answer and source documents

**Example:**
```python
result = rag.chat("What is the main topic discussed?")
print(result['answer'])
for source in result['sources']:
    print(f"Source: {source['title']}")
```

##### `search(query: str, k: int = TOP_K_RESULTS)`
Semantic search over transcripts.

**Parameters:**
- `query` (str): Search query
- `k` (int): Number of results to return

**Returns:**
- `List[Dict[str, Any]]`: Relevant chunks with metadata

**Example:**
```python
results = rag.search("machine learning", k=5)
for result in results:
    print(f"Score: {result['score']}")
    print(f"Content: {result['content']}")
```

##### `reset_conversation()`
Reset conversation memory.

---

### `src.utils`

Utility functions.

#### Functions

##### `extract_video_id(url: str)`
Extract video ID from YouTube URL.

**Parameters:**
- `url` (str): YouTube URL

**Returns:**
- `Optional[str]`: Video ID or None if invalid

**Example:**
```python
video_id = extract_video_id("https://youtu.be/dQw4w9WgXcQ")
# Returns: "dQw4w9WgXcQ"
```

##### `sanitize_filename(filename: str, max_length: int = 100)`
Sanitize filename by removing invalid characters.

**Parameters:**
- `filename` (str): Original filename
- `max_length` (int): Maximum length

**Returns:**
- `str`: Sanitized filename

##### `save_transcript(data: Dict[str, Any], output_dir: Path, index: int)`
Save transcript in JSON and TXT formats.

**Parameters:**
- `data` (Dict[str, Any]): Transcript data
- `output_dir` (Path): Output directory
- `index` (int): File index

**Returns:**
- `Tuple[Path, Path]`: JSON and TXT file paths

##### `validate_url(url: str)`
Validate if URL is a valid YouTube URL.

**Parameters:**
- `url` (str): URL to validate

**Returns:**
- `bool`: True if valid, False otherwise

##### `parse_urls_input(urls_text: str)`
Parse URLs from text input (one per line).

**Parameters:**
- `urls_text` (str): Text containing URLs

**Returns:**
- `List[str]`: List of valid URLs

##### `count_words(text: str)`
Count words in text.

**Parameters:**
- `text` (str): Input text

**Returns:**
- `int`: Word count

##### `format_timestamp()`
Get current timestamp in ISO format.

**Returns:**
- `str`: ISO formatted timestamp

##### `cleanup_temp_files(temp_dir: Path, keep_recent: int = 0)`
Clean up temporary audio files.

**Parameters:**
- `temp_dir` (Path): Temporary directory
- `keep_recent` (int): Number of recent files to keep

---

## Configuration

### Environment Variables

```bash
OPENAI_API_KEY=sk-proj-your-key-here
WHISPER_MODEL=whisper-1
EMBEDDING_MODEL=text-embedding-ada-002
CHAT_MODEL=gpt-4-turbo-preview
```

### Config Constants

```python
# Directory paths
TRANSCRIPTS_DIR: Path
TEMP_AUDIO_DIR: Path
VECTOR_DB_DIR: Path

# Audio settings
AUDIO_FORMAT: str = "mp3"
AUDIO_QUALITY: str = "192"

# RAG settings
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
TOP_K_RESULTS: int = 3
TEMPERATURE: float = 0.7

# Gradio settings
GRADIO_PORT: int = 7860
GRADIO_SHARE: bool = False

# Rate limiting
MAX_RETRIES: int = 3
RETRY_DELAY: int = 2
```

---

## Error Handling

All functions raise appropriate exceptions:

- `ValueError`: Invalid input parameters
- `FileNotFoundError`: Required files not found
- `Exception`: General processing errors

Always wrap API calls in try-except blocks:

```python
try:
    result = transcriber.process_video(url)
    if result['success']:
        print("Success!")
    else:
        print(f"Error: {result['error']}")
except Exception as e:
    print(f"Unexpected error: {e}")
```
