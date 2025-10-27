#!/bin/bash

# RAG Chatbot Startup Script

echo "🚀 Starting RAG Chatbot..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys!"
    exit 1
fi

# Check if Ollama is running
echo "🔍 Checking Ollama connection..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Warning: Ollama is not running!"
    echo "Please start Ollama with: ollama serve"
    echo "And pull the model with: ollama pull nomic-embed-text"
    exit 1
fi

# Check if model is available
if ! ollama list | grep -q "nomic-embed-text"; then
    echo "📥 Pulling nomic-embed-text model..."
    ollama pull nomic-embed-text
fi

echo "✅ All checks passed!"
echo "================================"
echo "🌐 Starting server..."
echo "📖 Access the app at: http://localhost:8050"
echo "📚 API docs at: http://localhost:8050/docs"
echo "================================"

# Start the application
cd backend
python main.py
