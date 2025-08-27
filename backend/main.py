from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import json
import os
from typing import Dict, Any
from data_processor import DataProcessor
from llm_service import LLMService
from visualization_generator import VisualizationGenerator

app = FastAPI(title="AI Dashboard API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize services
data_processor = DataProcessor()
llm_service = LLMService()
viz_generator = VisualizationGenerator()

class PromptRequest(BaseModel):
    prompt: str

class DashboardResponse(BaseModel):
    visualization: Dict[str, Any]
    insights: str
    data_summary: Dict[str, Any]

@app.on_event("startup")
async def startup_event():
    """Initialize data on startup"""
    await data_processor.load_data()

@app.get("/")
async def root():
    return {"message": "AI Dashboard API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ollama_available": await llm_service.check_connection()}

@app.get("/data/summary")
async def get_data_summary():
    """Get a summary of available data"""
    return await data_processor.get_data_summary()

@app.post("/generate-dashboard", response_model=DashboardResponse)
async def generate_dashboard(request: PromptRequest):
    """Generate a dashboard based on user prompt"""
    try:
        # Get data summary for context
        data_summary = await data_processor.get_data_summary()
        
        # Analyze prompt with LLM
        analysis = await llm_service.analyze_prompt(request.prompt, data_summary)
        
        # Process data based on analysis
        processed_data = await data_processor.process_data_for_visualization(analysis)
        
        # Generate visualization
        visualization = await viz_generator.create_visualization(analysis, processed_data)
        
        # Generate insights
        insights = await llm_service.generate_insights(processed_data, analysis)
        
        return DashboardResponse(
            visualization=visualization,
            insights=insights,
            data_summary=data_summary
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {str(e)}")

@app.get("/visualizations/sample")
async def get_sample_visualization():
    """Get a sample visualization for testing"""
    sample_data = await data_processor.get_sample_data()
    return await viz_generator.create_sample_visualization(sample_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
