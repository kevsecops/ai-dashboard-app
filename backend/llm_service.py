import ollama
import json
import os
from typing import Dict, Any
import asyncio

class LLMService:
    def __init__(self, model_name: str = "llama3.2:1b"):
        self.model_name = model_name
        # Use environment variable for Ollama host, default to localhost
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.client = ollama.AsyncClient(host=ollama_host)
    
    async def check_connection(self) -> bool:
        """Check if Ollama is available"""
        try:
            models = await self.client.list()
            return any(model['name'].startswith(self.model_name) for model in models['models'])
        except Exception as e:
            print(f"Ollama connection error: {e}")
            return False
    
    async def analyze_prompt(self, prompt: str, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user prompt and determine visualization requirements"""
        
        system_prompt = f"""
You are a data visualization expert. Analyze the user's prompt and the available data to determine the best visualization approach.

Available Data Summary:
{json.dumps(data_summary, indent=2)}

Based on the user's request, provide a JSON response with the following structure:
{{
    "chart_type": "line|bar|scatter|pie|heatmap|histogram",
    "datasets": ["Q1_2022", "Q1_2024"],
    "x_axis": "column_name",
    "y_axis": "column_name_or_list",
    "group_by": "column_name_for_grouping",
    "filters": {{
        "column_name": {{"min": value, "max": value, "equals": value, "in": [values]}}
    }},
    "aggregations": {{
        "group_by": "column_name",
        "functions": {{"column": "sum|mean|count|max|min"}}
    }},
    "title": "Descriptive title for the chart",
    "reasoning": "Brief explanation of why this visualization was chosen"
}}

Guidelines:
1. Choose the most appropriate chart type for the data and question
2. Use time-based charts (line) for trends over time
3. Use bar charts for comparisons between categories
4. Use scatter plots for correlations
5. Use pie charts for proportions (limit to <8 categories)
6. Consider aggregating data when appropriate
7. Filter data to focus on relevant subsets when needed

User Prompt: {prompt}
"""

        try:
            response = await self.client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this request: {prompt}"}
                ]
            )
            
            # Extract JSON from response
            content = response['message']['content']
            
            # Try to extract JSON from the response
            try:
                # Look for JSON block
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    analysis = json.loads(json_str)
                else:
                    raise ValueError("No JSON found in response")
            except (json.JSONDecodeError, ValueError):
                # Fallback to default analysis
                analysis = self._create_fallback_analysis(prompt, data_summary)
            
            return analysis
            
        except Exception as e:
            print(f"LLM analysis error: {e}")
            return self._create_fallback_analysis(prompt, data_summary)
    
    async def generate_insights(self, processed_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate insights about the visualization"""
        
        data_sample = processed_data.get('data', [])[:5]  # First 5 rows for context
        
        system_prompt = f"""
You are a business analyst. Generate clear, professional insights about the data visualization.

Visualization Details:
- Chart Type: {analysis.get('chart_type')}
- Title: {analysis.get('title')}
- Data Sample: {json.dumps(data_sample, indent=2)}

Provide insights in this clean format:

## Notable Trends or Patterns
- Key trend 1
- Key trend 2

## Business Implications  
- Implication 1
- Implication 2

## Recommendations
- Recommendation 1
- Recommendation 2

Keep insights concise, actionable, and avoid excessive markdown formatting.
"""

        try:
            response = await self.client.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Generate insights for this visualization."}
                ]
            )
            
            return response['message']['content']
            
        except Exception as e:
            print(f"Insight generation error: {e}")
            return "Unable to generate insights at this time. The visualization shows the requested data analysis."
    
    def _create_fallback_analysis(self, prompt: str, data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fallback analysis when LLM fails"""
        
        # Simple keyword-based fallback
        prompt_lower = prompt.lower()
        
        # Determine chart type based on keywords
        if any(word in prompt_lower for word in ['trend', 'time', 'over time', 'timeline']):
            chart_type = 'line'
            x_axis = 'Date'
            y_axis = 'Revenue'
        elif any(word in prompt_lower for word in ['compare', 'comparison', 'vs', 'versus']):
            chart_type = 'bar'
            x_axis = 'Region'
            y_axis = 'Revenue'
        elif any(word in prompt_lower for word in ['correlation', 'relationship', 'scatter']):
            chart_type = 'scatter'
            x_axis = 'Marketing_Spend'
            y_axis = 'Revenue'
        elif any(word in prompt_lower for word in ['distribution', 'proportion', 'pie']):
            chart_type = 'pie'
            x_axis = 'Region'
            y_axis = 'Revenue'
        else:
            chart_type = 'line'
            x_axis = 'Date'
            y_axis = 'Revenue'
        
        return {
            "chart_type": chart_type,
            "datasets": list(data_summary.get('datasets', {}).keys()),
            "x_axis": x_axis,
            "y_axis": y_axis,
            "group_by": None,
            "filters": {},
            "aggregations": {},
            "title": f"Analysis: {prompt}",
            "reasoning": "Fallback analysis based on keyword detection"
        }
