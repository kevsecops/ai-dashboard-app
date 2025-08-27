# 🚀 AI Dashboard - Quick Start Guide

## Current Status
✅ **Ollama is running in Docker** (port 11434)

## Start the Application (3 Simple Steps)

### Step 1: Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```
*Keep this terminal open*

### Step 2: Start Frontend (New Terminal)
```bash
cd frontend  
npm run dev
```
*Keep this terminal open*

### Step 3: Open Browser
Go to: **http://localhost:3000**

## 🎯 Test the AI Dashboard

Try these prompts:
- "Show me revenue trends over time"
- "Compare revenue by region"
- "What's the relationship between marketing spend and revenue?"

## 🔧 Troubleshooting

**If backend fails:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**If frontend fails:**
```bash
cd frontend
npm install
npm run dev
```

**If Ollama isn't running:**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

## 🛑 To Stop Everything

1. **Stop Backend & Frontend**: Ctrl+C in their terminals
2. **Stop Ollama**: `docker-compose -f docker-compose.dev.yml down`

## ✅ Working Setup Summary

- **Ollama**: Docker container (AI model)
- **Backend**: Local Python (FastAPI)  
- **Frontend**: Local Node.js (Next.js)
- **Data**: 181 business records loaded

**This hybrid approach works reliably!** 🎉
