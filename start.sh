#!/bin/bash

# AI Dashboard App Docker Startup Script

echo "🚀 Starting AI Dashboard App with Docker..."
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true

# Start the application with Docker Compose
echo "🐳 Starting all services with Docker Compose..."
echo "   • Ollama (LLM service)"
echo "   • Backend (FastAPI)"
echo "   • Frontend (Next.js)"
echo ""

# Use docker-compose or docker compose based on availability
if command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    docker compose up --build -d
fi

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Wait for Ollama to be ready and model to be pulled
echo "🤖 Setting up AI model (this may take a few minutes on first run)..."
echo "   Pulling llama3.2:1b model (fast & lightweight)..."

# Wait for ollama-setup to complete
timeout=300  # 5 minutes timeout
counter=0
while [ $counter -lt $timeout ]; do
    if docker ps -a --format "table {{.Names}}\t{{.Status}}" | grep -q "ollama-setup.*Exited (0)"; then
        echo "✅ AI model setup complete!"
        break
    fi
    sleep 5
    counter=$((counter + 5))
    if [ $((counter % 30)) -eq 0 ]; then
        echo "   Still setting up AI model... ($counter/$timeout seconds)"
    fi
done

if [ $counter -ge $timeout ]; then
    echo "⚠️  AI model setup is taking longer than expected, but services should still work"
fi

echo ""
echo "🎉 AI Dashboard App is ready!"
echo "=========================================="
echo "   🌐 Frontend: http://localhost:3000"
echo "   🤖 Backend API: http://localhost:8000"
echo "   📚 API Docs: http://localhost:8000/docs"
echo "   🧠 Ollama: http://localhost:11434"
echo ""
echo "💡 Open http://localhost:3000 in your browser to get started!"
echo ""
echo "🔧 To stop the application:"
echo "   docker-compose down"
echo ""
echo "📊 To view logs:"
echo "   docker-compose logs -f"
