# AI Dashboard App

A dynamic dashboard application that generates visualizations based on natural language prompts using a local LLM.

## 🚀 Features

- **Natural Language Interface**: Ask questions about your data in plain English
- **AI-Powered Visualizations**: Local LLM analyzes prompts and creates optimal charts
- **Interactive Charts**: Plotly-powered visualizations with zoom, pan, and hover
- **Real-time Insights**: AI-generated business insights and recommendations
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- **Local Processing**: All data stays on your machine with Ollama

## 🏗️ Architecture

- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Python for data processing
- **LLM**: Ollama (llama3.2:1b) for fast local AI processing
- **Visualization**: Plotly.js for interactive charts
- **Data**: CSV files processed with pandas and SQLite

## ⚡ Quick Start

### 🐳 Docker Setup (Recommended)
Everything runs in Docker containers - no local installations needed!

```bash
# Start the complete application (includes Ollama!)
./start.sh

# Stop the application
./stop.sh
```

**That's it!** The script will:
- Start Ollama in a container
- Pull the llama3.1 AI model automatically
- Start the backend API
- Start the frontend interface
- Set up all networking between services

### 🛠️ Manual Development Setup
For development with hot-reload:

```bash
# Setup development environment
./dev-setup.sh

# Start individual services
cd backend && source venv/bin/activate && uvicorn main:app --reload
cd frontend && npm run dev
```

### 📋 Prerequisites
- **Docker & Docker Compose** (for containerized setup)
- **Python 3.9+** (for manual setup)
- **Node.js 18+** (for manual setup)

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Ollama API**: http://localhost:11434
- **Health Check**: http://localhost:8000/health

## 📊 Sample Prompts

Try these example prompts to explore your data:

- "Show me revenue trends over time"
- "Compare revenue by region"
- "What's the relationship between marketing spend and revenue?"
- "Display customer satisfaction scores by region"
- "Show the top selling categories"
- "How has profit margin changed over time?"
- "Create a scatter plot of website visits vs new customers"

## 📁 Project Structure

```
AI Dashboard App/
├── frontend/                 # Next.js React frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   └── components/      # React components
│   ├── Dockerfile
│   └── package.json
├── backend/                 # FastAPI Python backend
│   ├── main.py             # FastAPI application
│   ├── data_processor.py   # CSV data processing
│   ├── llm_service.py      # Ollama LLM integration
│   ├── visualization_generator.py  # Plotly chart generation
│   ├── Dockerfile
│   └── requirements.txt
├── data/                   # CSV data files
│   ├── Q1_2022.csv
│   └── Q1_2024.csv
├── docker-compose.yml      # Docker orchestration
├── start.sh               # Production startup script
├── dev-setup.sh          # Development setup script
└── README.md
```

## 🔧 Configuration

### Environment Variables

**Frontend** (`frontend/next.config.js`):
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

**Backend**:
- `OLLAMA_HOST`: Ollama service URL (default: localhost:11434)

### Data Format

The application expects CSV files with columns like:
- Date, Revenue, Region, Marketing_Spend, Customer_Satisfaction_Score, etc.
- See `data/` directory for example format

## 🛠️ Development

### Adding New Data Sources
1. Place CSV files in the `data/` directory
2. Update `data_processor.py` to include new files in `self.data_files`
3. Restart the backend service

### Customizing Visualizations
- Modify `visualization_generator.py` to add new chart types
- Update the LLM prompts in `llm_service.py` for better analysis

### Frontend Customization
- Components are in `frontend/src/components/`
- Styling uses Tailwind CSS classes
- Charts are rendered with react-plotly.js

## 🐛 Troubleshooting

### Common Issues

1. **Ollama not found**: Install Ollama and pull the llama3.1 model
2. **Port conflicts**: Change ports in docker-compose.yml if needed
3. **CORS errors**: Ensure frontend URL is in backend CORS settings
4. **Memory issues**: Ollama requires significant RAM for larger models

### Logs
```bash
# Docker logs
docker-compose logs -f

# Backend logs
cd backend && uvicorn main:app --reload --log-level debug

# Frontend logs
cd frontend && npm run dev
```

## 📈 Performance Tips

- Use smaller LLM models for faster responses (e.g., llama3.1:8b)
- Limit data size for complex visualizations
- Enable caching for repeated queries
- Use SSD storage for better Ollama performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details
