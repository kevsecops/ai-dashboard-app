#!/bin/bash

echo "🚀 Starting AI Dashboard (Simple Setup)"
echo "======================================="
echo ""

# Start Ollama with Docker
echo "🤖 Starting Ollama in Docker..."
docker-compose -f docker-compose.dev.yml up -d

echo "⏳ Waiting for Ollama to start..."
sleep 10

# Start backend locally
echo "🔧 Starting Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start backend in background
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend locally
echo "🎨 Starting Frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "⏳ Waiting for all services to be ready..."
sleep 10

echo ""
echo "🎉 AI Dashboard is ready!"
echo "========================"
echo "🌐 Frontend: http://localhost:3000"
echo "🤖 Backend:  http://localhost:8000"
echo "🧠 Ollama:   http://localhost:11434"
echo ""
echo "🛑 To stop everything:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   docker-compose -f docker-compose.dev.yml down"
echo ""
echo "💡 Open http://localhost:3000 to start using the AI Dashboard!"

# Keep script running
wait
