# Architecture Documentation

## System Overview

YouTube Transcriber Pro is built with a modular architecture that separates concerns and allows for easy extension.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                  │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │   Gradio UI      │         │   CLI Interface  │     │
│  │  (app_gradio.py) │         │    (main.py)     │     │
│  └────────┬─────────┘         └────────┬─────────┘     │
└───────────┼──────────────────────────────┼──────────────┘
            │                              │
            └──────────────┬───────────────┘
                           │
┌──────────────────────────┼──────────────────────────────┐
│                   Business Logic Layer                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │         YouTubeTranscriber (transcriber.py)        │ │
│  │  - download_audio()                                │ │
│  │  - transcribe_audio()                              │ │
│  │  - process_video()                                 │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │           RAGEngine (rag_engine.py)                │ │
│  │  - index_transcripts()                             │ │
│  │  - chat()                                          │ │
│  │  - search()                                        │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────────────┬───────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────┐
│                   Integration Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ OpenAI   │  │  yt-dlp  │  │ ChromaDB │  │LangChain│ │
│  │ Whisper  │  │          │  │          │  │         │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└───────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────┐
│                      Storage Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │transcripts│  │temp_audio│  │vector_db │              │
│  │  (JSON)   │  │  (MP3)   │  │ (Chroma) │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└───────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### Gradio UI (`app_gradio.py`)
- **Purpose**: Web-based interface for end users
- **Features**:
  - URL input with validation
  - Real-time progress tracking
  - File viewer and download
  - Chat interface (Phase 2)
- **Technology**: Gradio 4.x
- **Port**: 7860 (configurable)

#### CLI Interface (`main.py`)
- **Purpose**: Command-line tool for automation
- **Features**:
  - Single/multiple URL processing
  - File-based input
  - Progress callbacks
  - Batch processing
- **Use Cases**: Scripts, cron jobs, CI/CD

### 2. Business Logic Layer

#### YouTubeTranscriber (`src/transcriber.py`)
Core transcription engine.

**Responsibilities:**
- Audio download from YouTube
- Audio transcription via Whisper API
- File management and cleanup
- Error handling and retries

**Key Methods:**
```python
download_audio(url) -> (Path, str)
transcribe_audio(audio_path) -> str
process_video(url, index) -> Dict
process_multiple_videos(urls) -> List[Dict]
```

**Design Patterns:**
- **Strategy Pattern**: Pluggable audio downloaders
- **Template Method**: Video processing workflow
- **Observer Pattern**: Progress callbacks

#### RAGEngine (`src/rag_engine.py`)
Retrieval-Augmented Generation engine.

**Responsibilities:**
- Text chunking and embedding
- Vector storage management
- Semantic search
- Conversational chat

**Key Methods:**
```python
index_transcripts() -> None
chat(question) -> Dict
search(query, k) -> List[Dict]
```

**Design Patterns:**
- **Facade Pattern**: Simplifies LangChain complexity
- **Singleton Pattern**: Single vector store instance
- **Chain of Responsibility**: LangChain pipeline

### 3. Integration Layer

#### OpenAI Whisper API
- **Model**: whisper-1
- **Input**: Audio files (MP3, max 25MB)
- **Output**: Text transcription
- **Cost**: $0.006/minute
- **Rate Limit**: 50 requests/min (tier 1)

#### yt-dlp
- **Purpose**: YouTube audio extraction
- **Format**: MP3, 192kbps
- **Features**: Auto-retry, format selection
- **Dependency**: FFmpeg

#### ChromaDB
- **Purpose**: Vector database
- **Storage**: Local filesystem
- **Features**: Similarity search, metadata filtering
- **Scalability**: ~1M documents

#### LangChain
- **Purpose**: RAG orchestration
- **Components**:
  - Text splitters
  - Embeddings
  - Vector stores
  - Conversational chains

### 4. Storage Layer

#### Transcripts Directory
```
transcripts/
├── 01_video_title.json    # Structured data
├── 01_video_title.txt     # Human-readable
├── 02_another_video.json
└── 02_another_video.txt
```

**JSON Schema:**
```json
{
  "video_id": "string",
  "url": "string",
  "title": "string",
  "language": "string|null",
  "transcript": "string",
  "timestamp": "ISO8601",
  "index": "integer",
  "word_count": "integer"
}
```

#### Temporary Audio
- **Purpose**: Intermediate audio files
- **Lifecycle**: Created → Used → Deleted
- **Cleanup**: Automatic after transcription

#### Vector Database
- **Format**: ChromaDB persistence
- **Contents**: Embeddings + metadata
- **Indexing**: On-demand or scheduled

## Data Flow

### Phase 1: Transcription Flow

```
1. User Input
   └─> URL validation
       └─> Video ID extraction

2. Audio Download
   └─> yt-dlp extraction
       └─> MP3 conversion (FFmpeg)
           └─> Save to temp_audio/

3. Transcription
   └─> Read audio file
       └─> Send to Whisper API
           └─> Receive text response

4. Storage
   └─> Create JSON (structured)
       └─> Create TXT (readable)
           └─> Save to transcripts/

5. Cleanup
   └─> Delete temp audio
       └─> Update UI/CLI
```

### Phase 2: RAG Flow

```
1. Indexing
   └─> Load all JSON transcripts
       └─> Split into chunks (1000 chars)
           └─> Generate embeddings
               └─> Store in ChromaDB

2. Query
   └─> User question
       └─> Convert to embedding
           └─> Similarity search (top-k)
               └─> Retrieve relevant chunks

3. Generation
   └─> Build prompt with context
       └─> Send to GPT-4
           └─> Receive answer
               └─> Format with citations
```

## Configuration Management

### Environment Variables
```
OPENAI_API_KEY      # Required
WHISPER_MODEL       # Optional (default: whisper-1)
EMBEDDING_MODEL     # Optional (default: text-embedding-ada-002)
CHAT_MODEL          # Optional (default: gpt-4-turbo-preview)
```

### Config File (`config.py`)
- Centralized configuration
- Type-safe constants
- Directory management
- Model parameters

## Error Handling Strategy

### Levels of Error Handling

1. **Input Validation**
   - URL format checking
   - File existence verification
   - Parameter validation

2. **API Errors**
   - Rate limiting (exponential backoff)
   - Network failures (retry with delay)
   - Authentication errors (fail fast)

3. **Processing Errors**
   - File size limits
   - Format incompatibilities
   - Disk space issues

4. **User Feedback**
   - Clear error messages
   - Progress indicators
   - Partial success reporting

### Retry Logic

```python
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

for attempt in range(MAX_RETRIES):
    try:
        result = api_call()
        break
    except Exception as e:
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY * (attempt + 1))
        else:
            raise
```

## Security Considerations

### API Key Management
- Never commit to version control
- Use environment variables
- Rotate keys regularly
- Monitor usage

### Input Sanitization
- Validate all URLs
- Sanitize filenames
- Limit file sizes
- Check file types

### Rate Limiting
- Implement request throttling
- Queue management
- User quotas (future)

### Data Privacy
- No PII in logs
- Secure temp file cleanup
- Optional data encryption

## Performance Optimization

### Bottlenecks

1. **Audio Download**: Network-bound
2. **Transcription**: API rate-limited
3. **Embedding**: Compute-intensive
4. **Vector Search**: Memory-bound

### Optimization Strategies

1. **Caching**
   - Cache transcriptions by video ID
   - Reuse embeddings

2. **Parallel Processing**
   - Multiple videos concurrently
   - Thread pool for I/O operations

3. **Batch Operations**
   - Batch embedding generation
   - Bulk vector insertion

4. **Resource Management**
   - Cleanup temp files immediately
   - Limit concurrent API calls
   - Stream large files

## Scalability

### Current Limitations
- Single-threaded processing
- Local storage only
- No distributed processing

### Future Enhancements
- **Horizontal Scaling**: Multiple workers
- **Cloud Storage**: S3/GCS integration
- **Queue System**: Redis/RabbitMQ
- **Caching Layer**: Redis for results
- **Load Balancing**: Multiple instances

## Testing Strategy

### Unit Tests
- Individual function testing
- Mock external dependencies
- Edge case coverage

### Integration Tests
- End-to-end workflows
- API integration
- File I/O operations

### Performance Tests
- Load testing
- Stress testing
- Memory profiling

## Monitoring and Logging

### Metrics to Track
- Transcription success rate
- Average processing time
- API costs
- Error rates
- Storage usage

### Logging Levels
```python
DEBUG: Detailed diagnostic info
INFO: General informational messages
WARNING: Warning messages
ERROR: Error messages
CRITICAL: Critical failures
```

## Deployment Architecture

### Development
```
Local Machine
├── Python venv
├── Local storage
└── Direct API calls
```

### Production (Hugging Face Spaces)
```
HF Infrastructure
├── Container runtime
├── Persistent storage
├── Environment secrets
└── Auto-scaling
```

### Production (Self-hosted)
```
Server/VM
├── Nginx (reverse proxy)
├── systemd (process manager)
├── Docker (optional)
└── Monitoring (logs, metrics)
```

## Future Architecture Considerations

### Microservices
- Separate transcription service
- Dedicated RAG service
- API gateway

### Event-Driven
- Message queue for jobs
- Webhook notifications
- Async processing

### Multi-tenancy
- User authentication
- Quota management
- Isolated storage

---

## Conclusion

This architecture provides:
- ✅ Modularity and maintainability
- ✅ Clear separation of concerns
- ✅ Easy testing and debugging
- ✅ Scalability path
- ✅ Security best practices
