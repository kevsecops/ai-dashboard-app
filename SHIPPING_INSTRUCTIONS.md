# 🚀 AI Dashboard - Shipping Instructions

## 📦 What to Ship to Your Colleague

Send them this entire folder: `AI Dashboard App/`

## 🎯 One-Command Setup for Your Colleague

Your colleague only needs to run:

```bash
./start.sh
```

That's it! Everything will be set up automatically.

## 📋 Prerequisites (for your colleague)

- **Docker Desktop** installed and running
- **Git** (if cloning from repository)

## 🔧 What the start.sh Script Does

1. ✅ Starts Ollama container with AI model
2. ✅ Builds and starts backend API container  
3. ✅ Builds and starts frontend UI container
4. ✅ Downloads llama3.2:1b model automatically (fast & lightweight)
5. ✅ Sets up all networking between services

## 🌐 Access Points

After running `./start.sh`, the application will be available at:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Ollama API**: http://localhost:11434

## 🛑 To Stop Everything

```bash
./stop.sh
```

Or manually:
```bash
docker-compose down
```

## 📊 Sample Prompts to Test

- "Show me revenue trends over time"
- "Compare revenue by region"
- "What's the relationship between marketing spend and revenue?"
- "Display customer satisfaction scores by region"

## 🔍 Troubleshooting

**If containers fail to start:**
```bash
docker-compose down --volumes
docker-compose up --build
```

**To view logs:**
```bash
docker-compose logs -f
```

**To check container status:**
```bash
docker-compose ps
```

## 📁 Project Structure

```
AI Dashboard App/
├── start.sh              # One-command startup
├── stop.sh               # One-command shutdown  
├── docker-compose.yml    # Container orchestration
├── frontend/             # Next.js UI
├── backend/              # FastAPI server
├── data/                 # Business data (CSV files)
└── README.md             # Full documentation
```

## 🎉 Ready to Ship!

Your colleague can now run the complete AI Dashboard with just Docker - no local Python, Node.js, or Ollama installation required!
