@echo off
echo 🤖 Enhanced Telegram Bot Setup
echo ================================

echo.
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 🔧 Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ FFmpeg is installed and available
) else (
    echo ❌ FFmpeg not found. Please install FFmpeg:
    echo    1. Download from https://ffmpeg.org/download.html
    echo    2. Add to your PATH environment variable
    echo.
)

echo.
echo 🦙 To set up Llama 3.1:8b AI:
echo    1. Install Ollama from https://ollama.ai/
echo    2. Run: ollama pull llama3.1:8b
echo    3. Run: ollama serve
echo.

echo.
echo 🚀 Setup complete! 
echo    - Your bot token is already configured
echo    - Run: python oizo.py
echo    - Use /commands in Telegram to see all features
echo.
pause
