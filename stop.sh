#!/bin/bash

# AI Dashboard App Stop Script

echo "🛑 Stopping AI Dashboard App..."
echo "==============================="

# Stop Docker Compose services
if command -v docker-compose &> /dev/null; then
    docker-compose down
else
    docker compose down
fi

echo ""
echo "✅ AI Dashboard App stopped successfully!"
echo ""
echo "🔧 To start again, run: ./start.sh"
