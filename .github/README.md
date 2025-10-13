# 🎥 YouTube Transcriber Pro

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Open-source tool for transcribing YouTube videos using OpenAI Whisper, with semantic search, conversational chat, and complete management capabilities.

## ✨ Features

- 🎯 **Accurate Transcription**: Powered by OpenAI Whisper API
- 🌍 **Multi-language Support**: Automatic language detection
- 📊 **Dual Output**: JSON (RAG-ready) + TXT (human-readable)
- 🖥️ **User-Friendly UI**: Built with Gradio
- 🔍 **Semantic Search**: RAG-powered search over transcripts
- 💬 **Conversational Chat**: Ask questions about your videos
- ⚙️ **Complete Management**: Web UI and CLI tools for managing transcripts
- 🗄️ **Vector DB Management**: Monitor and clean your vector database
- 🚀 **Easy Deployment**: Ready for Hugging Face Spaces

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FFmpeg ([Download here](https://ffmpeg.org/download.html))
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd youtube-transcriber
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-proj-your-key-here
```

## 📚 Documentation

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete documentation index
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[docs/](docs/)** - Detailed documentation
  - [Usage Guide](docs/USAGE.md)
  - [RAG Guide](docs/RAG_GUIDE.md)
  - [Management Guide](docs/MANAGEMENT.md)
  - [API Reference](docs/API.md)
  - [Workflow](docs/WORKFLOW.md)
  - [And more...](docs/README.md)

## 📖 Usage

### Option 1: Gradio UI (Recommended)

```bash
python app_gradio.py
```

Then open your browser to `http://localhost:7860`

**Available Tabs:**
- 📝 **Transcribe**: Process YouTube videos
- 🔍 **Search**: Semantic search across transcripts
- 💬 **Chat**: Ask questions about your videos
- ⚙️ **Management**: Manage transcripts and vector database

### Option 2: Command Line

**Single URL:**
```bash
python main.py https://youtu.be/VIDEO_ID
```

**Multiple URLs:**
```bash
python main.py https://youtu.be/VIDEO1 https://youtu.be/VIDEO2
```

**From file:**
```bash
python main.py --file urls.txt
```

### Option 3: Management CLI

```bash
# List all transcriptions
python manage.py --list

# View statistics
python manage.py --stats

# Delete specific transcription
python manage.py --delete VIDEO_ID

# Check vector database status
python manage.py --check-db

# Clean temporary files
python manage.py --clean-temp

# Clear vector database
python manage.py --clear-db

# Delete everything (with confirmation)
python manage.py --clear-all
```

See [docs/MANAGEMENT.md](docs/MANAGEMENT.md) for detailed management guide.

## 📁 Project Structure

```
youtube-transcriber/
├── src/                    # Source code
│   ├── transcriber.py     # Core transcription logic
│   ├── rag_engine.py      # RAG & chat (Phase 2)
│   └── utils.py           # Utility functions
├── tests/                 # Unit tests
│   ├── test_transcriber.py
│   ├── test_utils.py
│   └── conftest.py
├── docs/                  # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── ARCHITECTURE.md
├── transcripts/           # Output files
├── temp_audio/            # Temporary audio files
├── main.py               # CLI interface
├── app_gradio.py         # Gradio UI
├── config.py             # Configuration
└── requirements.txt      # Dependencies
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_utils.py
```

## 💰 Cost Estimation

Whisper API pricing: **$0.006 per minute**

| Video Duration | Approximate Cost |
|----------------|------------------|
| 10 minutes     | $0.06 USD        |
| 30 minutes     | $0.18 USD        |
| 1 hour         | $0.36 USD        |
| 2 hours        | $0.72 USD        |

## 📊 Output Format

### JSON Output
```json
{
  "video_id": "dQw4w9WgXcQ",
  "url": "https://youtu.be/dQw4w9WgXcQ",
  "title": "Video Title",
  "language": null,
  "transcript": "Full transcription...",
  "timestamp": "2025-10-12T14:30:00",
  "index": 1,
  "word_count": 2547
}
```

### TXT Output
```
Title: Video Title
URL: https://youtu.be/dQw4w9WgXcQ
Video ID: dQw4w9WgXcQ
Language: N/A
Timestamp: 2025-10-12T14:30:00
Word Count: 2547

================================================================================

Full transcription text here...
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model Configuration
WHISPER_MODEL = "whisper-1"
EMBEDDING_MODEL = "text-embedding-ada-002"  # Phase 2
CHAT_MODEL = "gpt-4-turbo-preview"          # Phase 2

# Processing Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3
```

## 🌐 Deployment

### Hugging Face Spaces (Free)

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select Gradio SDK
3. Push your code
4. Add `OPENAI_API_KEY` in Space settings → Repository Secrets

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 🗺️ Roadmap

### Phase 1: MVP ✅
- [x] Core transcription engine
- [x] Gradio UI
- [x] JSON + TXT output
- [x] Progress tracking
- [x] Error handling

### Phase 2: RAG + Chat ✅
- [x] Vector database integration
- [x] Semantic search
- [x] Conversational chat interface
- [x] Source citations

### Phase 3: Management ✅
- [x] Web-based management interface
- [x] CLI management tools
- [x] Vector database monitoring
- [x] Bulk operations
- [x] Statistics and reporting

### Future Features 🌟
- [ ] Batch parallel processing
- [ ] Automatic summarization
- [ ] PDF/Markdown export
- [ ] Playlist support
- [ ] Speaker detection
- [ ] Auto-translation
- [ ] Export/Import functionality
- [ ] Advanced search filters

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://openai.com/research/whisper) for transcription
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube downloads
- [Gradio](https://www.gradio.app/) for the UI framework
- [LangChain](https://www.langchain.com/) for RAG capabilities

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ by @inginddie**
