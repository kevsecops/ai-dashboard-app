import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List
import pandas as pd

class VisualizationGenerator:
    def __init__(self):
        self.color_palette = [
            '#3B82F6', '#EF4444', '#10B981', '#F59E0B', 
            '#8B5CF6', '#06B6D4', '#F97316', '#84CC16'
        ]
    
    async def create_visualization(self, analysis: Dict[str, Any], processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Plotly visualization based on analysis and data"""
        
        chart_type = analysis.get('chart_type', 'line')
        data = processed_data.get('data', [])
        
        if not data:
            return self._create_empty_chart()
        
        df = pd.DataFrame(data)
        
        try:
            if chart_type == 'line':
                fig = self._create_line_chart(df, analysis)
            elif chart_type == 'bar':
                fig = self._create_bar_chart(df, analysis)
            elif chart_type == 'scatter':
                fig = self._create_scatter_chart(df, analysis)
            elif chart_type == 'pie':
                fig = self._create_pie_chart(df, analysis)
            elif chart_type == 'histogram':
                fig = self._create_histogram(df, analysis)
            elif chart_type == 'heatmap':
                fig = self._create_heatmap(df, analysis)
            else:
                fig = self._create_line_chart(df, analysis)  # Default fallback
            
            # Apply common styling
            self._apply_styling(fig, analysis.get('title', 'Visualization'))
            
            return {
                "plotly_json": fig.to_json(),
                "chart_type": chart_type,
                "title": analysis.get('title', 'Visualization')
            }
            
        except Exception as e:
            print(f"Visualization error: {e}")
            return self._create_error_chart(str(e))
    
    def _create_line_chart(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> go.Figure:
        """Create a line chart"""
        x_col = analysis.get('x_axis')
        y_col = analysis.get('y_axis')
        group_col = analysis.get('group_by')
        
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            # Fallback to first numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            x_col = df.columns[0] if len(df.columns) > 0 else 'x'
            y_col = numeric_cols[0] if numeric_cols else df.columns[1] if len(df.columns) > 1 else 'y'
        
        if group_col and group_col in df.columns:
            fig = px.line(df, x=x_col, y=y_col, color=group_col, 
                         color_discrete_sequence=self.color_palette)
        else:
            fig = px.line(df, x=x_col, y=y_col, 
                         color_discrete_sequence=self.color_palette)
        
        return fig
    
    def _create_bar_chart(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> go.Figure:
        """Create a bar chart"""
        x_col = analysis.get('x_axis')
        y_col = analysis.get('y_axis')
        group_col = analysis.get('group_by')
        
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            # Fallback
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            x_col = categorical_cols[0] if categorical_cols else df.columns[0]
            y_col = numeric_cols[0] if numeric_cols else df.columns[1] if len(df.columns) > 1 else 'y'
        
        if group_col and group_col in df.columns:
            fig = px.bar(df, x=x_col, y=y_col, color=group_col,
                        color_discrete_sequence=self.color_palette)
        else:
            fig = px.bar(df, x=x_col, y=y_col,
                        color_discrete_sequence=self.color_palette)
        
        return fig
    
    def _create_scatter_chart(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> go.Figure:
        """Create a scatter plot"""
        x_col = analysis.get('x_axis')
        y_col = analysis.get('y_axis')
        group_col = analysis.get('group_by')
        
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            x_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[0]
            y_col = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0] if numeric_cols else df.columns[1]
        
        if group_col and group_col in df.columns:
            fig = px.scatter(df, x=x_col, y=y_col, color=group_col,
                           color_discrete_sequence=self.color_palette)
        else:
            fig = px.scatter(df, x=x_col, y=y_col,
                           color_discrete_sequence=self.color_palette)
        
        return fig
    
    def _create_pie_chart(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> go.Figure:
        """Create a pie chart"""
        x_col = analysis.get('x_axis')  # categories
        y_col = analysis.get('y_axis')  # values
        
        if not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            x_col = categorical_cols[0] if categorical_cols else df.columns[0]
            y_col = numeric_cols[0] if numeric_cols else df.columns[1] if len(df.columns) > 1 else 'count'
        
        # Aggregate data for pie chart
        if y_col in df.columns:
            pie_data = df.groupby(x_col)[y_col].sum().reset_index()
        else:
            pie_data = df[x_col].value_counts().reset_index()
            pie_data.columns = [x_col, 'count']
            y_col = 'count'
        
        fig = px.pie(pie_data, names=x_col, values=y_col,
                    color_discrete_sequence=self.color_palette)
        
        return fig
    
    def _create_histogram(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> go.Figure:
        """Create a histogram"""
        x_col = analysis.get('x_axis')
        
        if not x_col or x_col not in df.columns:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            x_col = numeric_cols[0] if numeric_cols else df.columns[0]
        
        fig = px.histogram(df, x=x_col, color_discrete_sequence=self.color_palette)
        
        return fig
    
    def _create_heatmap(self, df: pd.DataFrame, analysis: Dict[str, Any]) -> go.Figure:
        """Create a heatmap"""
        # Use correlation matrix for numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            return self._create_empty_chart()
        
        corr_matrix = numeric_df.corr()
        
        fig = px.imshow(corr_matrix, 
                       color_continuous_scale='RdBu_r',
                       aspect='auto')
        
        return fig
    
    def _apply_styling(self, fig: go.Figure, title: str):
        """Apply consistent styling to the figure"""
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'family': 'Arial, sans-serif'}
            },
            font={'family': 'Arial, sans-serif'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=60, b=40),
            height=500
        )
        
        # Update axes styling
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(128,128,128,0.3)'
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128,128,128,0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(128,128,128,0.3)'
        )
    
    def _create_empty_chart(self) -> Dict[str, Any]:
        """Create an empty chart when no data is available"""
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for visualization",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        self._apply_styling(fig, "No Data")
        
        return {
            "plotly_json": fig.to_json(),
            "chart_type": "empty",
            "title": "No Data"
        }
    
    def _create_error_chart(self, error_message: str) -> Dict[str, Any]:
        """Create an error chart"""
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating visualization: {error_message}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="red")
        )
        self._apply_styling(fig, "Error")
        
        return {
            "plotly_json": fig.to_json(),
            "chart_type": "error",
            "title": "Error"
        }
    
    async def create_sample_visualization(self, sample_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a sample visualization for testing"""
        analysis = {
            "chart_type": "line",
            "x_axis": sample_data.get('x_axis', 'Date'),
            "y_axis": sample_data.get('y_axis', 'Revenue'),
            "title": sample_data.get('title', 'Sample Visualization')
        }
        
        return await self.create_visualization(analysis, sample_data)
