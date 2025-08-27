#!/bin/bash

# Development Setup Script for AI Dashboard App

echo "🔧 Setting up AI Dashboard App for development..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Check Ollama setup
echo "🔍 Checking Ollama setup..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Installing now..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Pull model if not available
if ! ollama list | grep -q "llama3.1"; then
    echo "📥 Downloading llama3.1 model..."
    ollama pull llama3.1
fi

echo "✅ Development setup complete!"
echo ""
echo "🚀 To start development servers:"
echo "   Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "🐳 Or use Docker: ./start.sh"
