@echo off
REM RAG Chatbot Startup Script for Windows

echo 🚀 Starting RAG Chatbot...
echo ================================

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📚 Installing dependencies...
pip install -q -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo 📝 Creating .env from .env.example...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your API keys!
    pause
    exit /b 1
)

echo ✅ Setup complete!
echo ================================
echo 🌐 Starting server...
echo 📖 Access the app at: http://localhost:8050
echo 📚 API docs at: http://localhost:8050/docs
echo ================================
echo.
echo ⚠️  Note: Make sure Ollama is running!
echo    Start with: ollama serve
echo    Pull model: ollama pull nomic-embed-text
echo.

REM Start the application
cd backend
python main.py
