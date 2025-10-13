# ⚡ Quick Start Guide

Get up and running with YouTube Transcriber Pro in 5 minutes!

## 🎯 Prerequisites

Before you start, make sure you have:

- ✅ Python 3.8 or higher
- ✅ FFmpeg installed
- ✅ OpenAI API key

### Install FFmpeg

**Windows:**
```bash
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

### Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it (you'll need it in step 3)

---

## 🚀 Installation (3 Steps)

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd youtube-transcriber
```

### Step 2: Run Setup Script

**Linux/Mac:**
```bash
bash scripts/setup.sh
```

**Windows:**
```bash
scripts\setup.bat
```

This will:
- Create virtual environment
- Install dependencies
- Create necessary directories
- Generate .env file

### Step 3: Add Your API Key

Edit the `.env` file:

```bash
# Linux/Mac
nano .env

# Windows
notepad .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

Save and close.

---

## 🎬 First Transcription

### Option A: Using the Web UI (Recommended)

1. **Start the UI:**
```bash
python app_gradio.py
```

2. **Open your browser:**
```
http://localhost:7860
```

3. **Transcribe a video:**
   - Paste a YouTube URL in the text box
   - Click "🚀 Transcribe Videos"
   - Wait for completion
   - View and download your transcript!

### Option B: Using the CLI

```bash
python main.py https://youtu.be/dQw4w9WgXcQ
```

That's it! Your transcript will be saved in the `transcripts/` folder.

---

## 📁 Where Are My Files?

After transcription, you'll find:

```
transcripts/
├── 01_video_title.json    # Structured data
└── 01_video_title.txt     # Human-readable
```

**JSON format** - For programmatic use:
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "transcript": "Full text...",
  "word_count": 1234
}
```

**TXT format** - For reading:
```
Title: Video Title
URL: https://youtu.be/dQw4w9WgXcQ
...

Full transcription text here...
```

---

## 💡 Common Use Cases

### Transcribe Multiple Videos

Create a file `urls.txt`:
```
https://youtu.be/VIDEO_1
https://youtu.be/VIDEO_2
https://youtu.be/VIDEO_3
```

Then run:
```bash
python main.py --file urls.txt
```

### Use in Your Python Code

```python
from src.transcriber import YouTubeTranscriber

transcriber = YouTubeTranscriber()
result = transcriber.process_video("https://youtu.be/VIDEO_ID", 1)

if result['success']:
    print(f"✅ {result['title']}")
    print(f"📄 {result['json_path']}")
```

### Search Your Transcripts (Phase 2)

```python
from src.rag_engine import RAGEngine

# Index your transcripts
rag = RAGEngine()
rag.index_transcripts()

# Search
results = rag.search("machine learning", k=5)
for result in results:
    print(result['content'])
```

### Chat with Your Videos (Phase 2)

```python
# Setup
rag.load_vector_store()
rag.setup_conversation_chain()

# Ask questions
response = rag.chat("What are the main topics?")
print(response['answer'])
```

---

## 🧪 Verify Installation

Run the test suite:

```bash
pytest
```

You should see:
```
======================== test session starts ========================
...
======================== X passed in X.XXs =========================
```

---

## 💰 Cost Estimate

Whisper API costs **$0.006 per minute** of audio:

| Video Length | Cost      |
|--------------|-----------|
| 10 minutes   | $0.06     |
| 30 minutes   | $0.18     |
| 1 hour       | $0.36     |

---

## 🆘 Troubleshooting

### "FFmpeg not found"

**Solution:** Install FFmpeg (see prerequisites above)

### "OPENAI_API_KEY not found"

**Solution:** Make sure you created `.env` file with your API key

### "Module not found"

**Solution:** Activate virtual environment:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### "Port 7860 already in use"

**Solution:** Change port in `config.py`:
```python
GRADIO_PORT = 7861  # Use different port
```

---

## 📚 Next Steps

Now that you're up and running:

1. **Read the full documentation:**
   - [Usage Guide](docs/USAGE.md)
   - [API Reference](docs/API.md)
   - [Deployment Guide](docs/DEPLOYMENT.md)

2. **Check out examples:**
   - [Basic Examples](examples/basic_usage.py)
   - [Advanced Examples](examples/advanced_usage.py)

3. **Deploy to production:**
   - [Hugging Face Spaces](docs/DEPLOYMENT.md#hugging-face-spaces-recommended---free)
   - [Docker](docs/DEPLOYMENT.md#docker-deployment)
   - [AWS](docs/DEPLOYMENT.md#aws-deployment)

4. **Contribute:**
   - [Contributing Guide](CONTRIBUTING.md)

---

## 🎉 You're All Set!

You now have a fully functional YouTube transcription system!

**Happy transcribing! 🚀**

---

## 📞 Need Help?

- 📖 [Full Documentation](docs/)
- 💬 [GitHub Issues](https://github.com/YOUR_REPO/issues)
- 🤝 [Contributing](CONTRIBUTING.md)

---

**Made with ❤️ by @inginddie**
