@echo off
REM Setup script for YouTube Transcriber Pro (Windows)

echo Setting up YouTube Transcriber Pro...
echo.

REM Check Python version
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Python not found! Please install Python 3.8+
    exit /b 1
)
echo Python OK
echo.

REM Check FFmpeg
echo Checking FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg not found!
    echo Please install FFmpeg: choco install ffmpeg
    exit /b 1
)
echo FFmpeg OK
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Create .env file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created
    echo.
    echo WARNING: Please edit .env and add your OPENAI_API_KEY
) else (
    echo .env file already exists
)
echo.

REM Create directories
echo Creating directories...
python -c "from config import create_directories; create_directories()"
echo Directories created
echo.

REM Run tests
echo Running tests...
pytest --tb=short
echo Tests passed
echo.

echo Setup complete!
echo.
echo Next steps:
echo   1. Edit .env and add your OpenAI API key
echo   2. Run: python app_gradio.py (for UI)
echo   3. Or: python main.py ^<youtube-url^> (for CLI)
echo.

pause
