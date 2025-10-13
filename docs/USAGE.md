# Usage Guide

## Getting Started

### First Time Setup

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure API key**
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
```

3. **Verify installation**
```bash
python -c "import yt_dlp; import openai; print('✅ Ready!')"
```

## Using the Gradio UI

### Starting the UI

```bash
python app_gradio.py
```

The interface will open at `http://localhost:7860`

### Basic Workflow

1. **Enter URLs**
   - Paste YouTube URLs in the text box
   - One URL per line
   - Supports various YouTube URL formats

2. **Start Transcription**
   - Click "🚀 Transcribe Videos"
   - Watch the progress bar
   - Wait for completion

3. **View Results**
   - Click "🔄 Refresh File List"
   - Select a file from dropdown
   - View content in the text area
   - Download files as needed

### Supported URL Formats

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/embed/VIDEO_ID
https://www.youtube.com/watch?v=VIDEO_ID&t=10s
```

## Using the CLI

### Basic Commands

**Single video:**
```bash
python main.py https://youtu.be/dQw4w9WgXcQ
```

**Multiple videos:**
```bash
python main.py https://youtu.be/VIDEO1 https://youtu.be/VIDEO2
```

**From file:**
```bash
python main.py --file urls.txt
```

### Creating URL Files

Create a text file with one URL per line:

```txt
# urls.txt
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/abc123def45
https://youtu.be/xyz789uvw12
```

Then run:
```bash
python main.py --file urls.txt
```

### CLI Options

```bash
python main.py --help
```

Output:
```
usage: main.py [-h] [--file FILE] [urls ...]

YouTube Transcriber Pro - Transcribe YouTube videos using OpenAI Whisper

positional arguments:
  urls                  YouTube video URLs to transcribe

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  File containing YouTube URLs (one per line)
```

## Understanding Output Files

### JSON Format

Located in `transcripts/` directory:

```json
{
  "video_id": "dQw4w9WgXcQ",
  "url": "https://youtu.be/dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "language": null,
  "transcript": "We're no strangers to love...",
  "timestamp": "2025-10-12T14:30:00",
  "index": 1,
  "word_count": 780
}
```

**Fields:**
- `video_id`: YouTube video identifier
- `url`: Original video URL
- `title`: Video title from YouTube
- `language`: Detected language (null in text mode)
- `transcript`: Full transcription text
- `timestamp`: When transcription was created
- `index`: Sequential file number
- `word_count`: Total words in transcript

### TXT Format

Human-readable format:

```
Title: Rick Astley - Never Gonna Give You Up
URL: https://youtu.be/dQw4w9WgXcQ
Video ID: dQw4w9WgXcQ
Language: N/A
Timestamp: 2025-10-12T14:30:00
Word Count: 780

================================================================================

We're no strangers to love
You know the rules and so do I...
```

## Advanced Usage

### Programmatic Usage

```python
from src.transcriber import YouTubeTranscriber

# Initialize
transcriber = YouTubeTranscriber()

# Process single video
result = transcriber.process_video(
    url="https://youtu.be/VIDEO_ID",
    index=1
)

if result['success']:
    print(f"✅ {result['title']}")
    print(f"📄 JSON: {result['json_path']}")
    print(f"📄 TXT: {result['txt_path']}")
else:
    print(f"❌ Error: {result['error']}")

# Process multiple videos
urls = [
    "https://youtu.be/VIDEO1",
    "https://youtu.be/VIDEO2"
]

results = transcriber.process_multiple_videos(urls)

for result in results:
    if result['success']:
        print(f"✅ {result['title']}")
```

### Custom Progress Callbacks

```python
def my_progress_callback(message: str):
    print(f"[{datetime.now()}] {message}")

result = transcriber.process_video(
    url="https://youtu.be/VIDEO_ID",
    index=1,
    progress_callback=my_progress_callback
)
```

### Batch Processing Script

```python
# batch_process.py
import sys
from pathlib import Path
from src.transcriber import YouTubeTranscriber

def process_playlist(urls_file: str):
    transcriber = YouTubeTranscriber()
    
    with open(urls_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Processing {len(urls)} videos...")
    
    results = transcriber.process_multiple_videos(urls)
    
    successful = sum(1 for r in results if r['success'])
    print(f"\n✅ Completed: {successful}/{len(urls)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_process.py urls.txt")
        sys.exit(1)
    
    process_playlist(sys.argv[1])
```

## Phase 2: RAG and Chat

### Indexing Transcripts

```python
from src.rag_engine import RAGEngine

# Initialize
rag = RAGEngine()

# Index all transcripts
rag.index_transcripts()
```

### Semantic Search

```python
# Search for content
results = rag.search("machine learning", k=5)

for result in results:
    print(f"Score: {result['score']:.4f}")
    print(f"Video: {result['metadata']['title']}")
    print(f"Content: {result['content'][:200]}...")
    print()
```

### Conversational Chat

```python
# Setup conversation
rag.load_vector_store()
rag.setup_conversation_chain()

# Ask questions
response = rag.chat("What are the main topics discussed?")
print(response['answer'])

print("\nSources:")
for source in response['sources']:
    print(f"- {source['title']}")
    print(f"  {source['url']}")

# Continue conversation
response = rag.chat("Can you elaborate on the first topic?")
print(response['answer'])

# Reset conversation
rag.reset_conversation()
```

## Tips and Best Practices

### 1. URL Validation

Always validate URLs before processing:

```python
from src.utils import validate_url

url = "https://youtu.be/VIDEO_ID"
if validate_url(url):
    # Process video
    pass
else:
    print("Invalid URL")
```

### 2. Error Handling

Wrap processing in try-except:

```python
try:
    result = transcriber.process_video(url)
    if result['success']:
        print("Success!")
    else:
        print(f"Failed: {result['error']}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 3. Cost Management

Monitor your usage:

```python
# Estimate cost before processing
def estimate_cost(duration_minutes: int) -> float:
    return duration_minutes * 0.006

# For a 30-minute video
cost = estimate_cost(30)
print(f"Estimated cost: ${cost:.2f}")
```

### 4. File Organization

Keep transcripts organized:

```bash
transcripts/
├── 2025-10-12/
│   ├── 01_video_title.json
│   └── 01_video_title.txt
└── 2025-10-13/
    ├── 01_another_video.json
    └── 01_another_video.txt
```

### 5. Cleanup

Regularly clean up temp files:

```python
from src.utils import cleanup_temp_files
from config import TEMP_AUDIO_DIR

cleanup_temp_files(TEMP_AUDIO_DIR)
```

## Troubleshooting

### Common Issues

**Issue: "FFmpeg not found"**
```bash
# Install FFmpeg
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

**Issue: "API key not found"**
```bash
# Check .env file exists
cat .env

# Verify key is set
python -c "from config import OPENAI_API_KEY; print(OPENAI_API_KEY[:10])"
```

**Issue: "File too large"**
- Whisper API has 25MB limit
- Solution: Video will be automatically split (future feature)

**Issue: "Rate limit exceeded"**
- Wait a few minutes
- Reduce concurrent requests
- Upgrade OpenAI tier

### Debug Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Performance Tips

### 1. Parallel Processing

For multiple videos:

```python
from concurrent.futures import ThreadPoolExecutor

def process_parallel(urls, max_workers=3):
    transcriber = YouTubeTranscriber()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(transcriber.process_video, url, i)
            for i, url in enumerate(urls, 1)
        ]
        
        results = [f.result() for f in futures]
    
    return results
```

### 2. Caching

Avoid re-transcribing:

```python
from pathlib import Path
import json

def is_already_transcribed(video_id: str) -> bool:
    for json_file in Path('transcripts').glob('*.json'):
        with open(json_file) as f:
            data = json.load(f)
            if data['video_id'] == video_id:
                return True
    return False
```

### 3. Batch Operations

Process in batches:

```python
def process_in_batches(urls, batch_size=5):
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}")
        transcriber.process_multiple_videos(batch)
        time.sleep(60)  # Rate limiting
```

## Integration Examples

### With Notion

```python
# Export to Notion-friendly format
def export_to_notion(json_path: str):
    with open(json_path) as f:
        data = json.load(f)
    
    notion_format = f"""
# {data['title']}

**URL**: {data['url']}
**Date**: {data['timestamp']}
**Words**: {data['word_count']}

## Transcript

{data['transcript']}
"""
    
    return notion_format
```

### With Obsidian

```python
# Create Obsidian note
def create_obsidian_note(json_path: str, vault_path: str):
    with open(json_path) as f:
        data = json.load(f)
    
    note_path = Path(vault_path) / f"{data['title']}.md"
    
    with open(note_path, 'w') as f:
        f.write(f"# {data['title']}\n\n")
        f.write(f"- URL: {data['url']}\n")
        f.write(f"- Date: {data['timestamp']}\n")
        f.write(f"- Tags: #youtube #transcript\n\n")
        f.write(f"## Content\n\n{data['transcript']}")
```

---

## Next Steps

- Explore [API Documentation](API.md)
- Learn about [Deployment](DEPLOYMENT.md)
- Understand [Architecture](ARCHITECTURE.md)
- Check [Examples](../examples/)
