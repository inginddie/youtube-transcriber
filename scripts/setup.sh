#!/bin/bash
# Setup script for YouTube Transcriber Pro

echo "🚀 Setting up YouTube Transcriber Pro..."
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version"

# Check FFmpeg
echo ""
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n1)
    echo "✅ FFmpeg installed"
else
    echo "❌ FFmpeg not found"
    echo "Please install FFmpeg:"
    echo "  - Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  - macOS: brew install ffmpeg"
    echo "  - Windows: choco install ffmpeg"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
else
    echo "✅ .env file already exists"
fi

# Create directories
echo ""
echo "Creating directories..."
python3 -c "from config import create_directories; create_directories()"
echo "✅ Directories created"

# Run tests
echo ""
echo "Running tests..."
pytest --tb=short
echo "✅ Tests passed"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your OpenAI API key"
echo "  2. Run: python app_gradio.py (for UI)"
echo "  3. Or: python main.py <youtube-url> (for CLI)"
echo ""
