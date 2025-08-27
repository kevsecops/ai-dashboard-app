import pandas as pd
import sqlite3
import os
from typing import Dict, Any, List
import json

class DataProcessor:
    def __init__(self):
        self.db_path = "dashboard.db"
        self.data_files = {
            "Q1_2022": "data/Q1_2022.csv",
            "Q1_2024": "data/Q1_2024.csv"
        }
        self.dataframes = {}
        
    async def load_data(self):
        """Load CSV files into pandas DataFrames and SQLite"""
        conn = sqlite3.connect(self.db_path)
        
        for name, file_path in self.data_files.items():
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                # Clean the data
                df = self._clean_dataframe(df)
                self.dataframes[name] = df
                # Store in SQLite for complex queries
                df.to_sql(name.lower(), conn, if_exists='replace', index=False)
                print(f"Loaded {name}: {len(df)} rows")
            else:
                print(f"Warning: {file_path} not found")
        
        conn.close()
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare dataframe"""
        # Remove empty rows
        df = df.dropna(how='all')
        
        # Convert date column to datetime if it exists
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = [
            'Revenue', 'COGS', 'Gross_Profit', 'Operating_Expenses', 'Net_Profit',
            'Units_Sold', 'Number_of_Transactions', 'Average_Transaction_Value',
            'Marketing_Spend', 'Website_Visits', 'New_Customers', 'Returning_Customers',
            'Customer_Acquisition_Cost', 'Customer_Satisfaction_Score', 'Inventory_Level',
            'Production_Volume', 'Supplier_Lead_Time_Days'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    async def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of available data"""
        summary = {
            "datasets": {},
            "total_records": 0,
            "date_range": {},
            "columns": {},
            "sample_data": {}
        }
        
        for name, df in self.dataframes.items():
            dataset_summary = {
                "rows": len(df),
                "columns": list(df.columns),
                "date_range": None,
                "numeric_columns": [],
                "categorical_columns": []
            }
            
            # Date range
            if 'Date' in df.columns:
                dataset_summary["date_range"] = {
                    "start": df['Date'].min().isoformat() if pd.notna(df['Date'].min()) else None,
                    "end": df['Date'].max().isoformat() if pd.notna(df['Date'].max()) else None
                }
            
            # Column types
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    dataset_summary["numeric_columns"].append(col)
                else:
                    dataset_summary["categorical_columns"].append(col)
            
            summary["datasets"][name] = dataset_summary
            summary["total_records"] += len(df)
            
            # Sample data (first 3 rows) - fix timestamp serialization
            sample_records = df.head(3).to_dict('records')
            for record in sample_records:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif hasattr(value, 'isoformat'):  # Handle datetime/timestamp
                        record[key] = value.isoformat()
            summary["sample_data"][name] = sample_records
        
        return summary
    
    async def process_data_for_visualization(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Process data based on LLM analysis"""
        try:
            chart_type = analysis.get('chart_type', 'line')
            datasets = analysis.get('datasets', list(self.dataframes.keys()))
            filters = analysis.get('filters', {})
            aggregations = analysis.get('aggregations', {})
            
            # Combine datasets if multiple are specified
            if len(datasets) > 1:
                combined_df = pd.concat([self.dataframes[ds] for ds in datasets if ds in self.dataframes])
            else:
                dataset_name = datasets[0] if datasets else list(self.dataframes.keys())[0]
                combined_df = self.dataframes[dataset_name].copy()
            
            # Apply filters
            filtered_df = self._apply_filters(combined_df, filters)
            
            # Apply aggregations
            processed_df = self._apply_aggregations(filtered_df, aggregations)
            
            # Convert timestamps to strings for JSON serialization
            processed_data = processed_df.to_dict('records')
            for record in processed_data:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
                    elif hasattr(value, 'isoformat'):  # Handle datetime/timestamp
                        record[key] = value.isoformat()
            
            return {
                "data": processed_data,
                "columns": list(processed_df.columns),
                "chart_type": chart_type,
                "x_axis": analysis.get('x_axis'),
                "y_axis": analysis.get('y_axis'),
                "group_by": analysis.get('group_by'),
                "title": analysis.get('title', 'Generated Visualization')
            }
            
        except Exception as e:
            print(f"Error processing data: {e}")
            # Return sample data as fallback
            return await self.get_sample_data()
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to dataframe"""
        filtered_df = df.copy()
        
        for column, condition in filters.items():
            if column in df.columns:
                if isinstance(condition, dict):
                    if 'min' in condition:
                        filtered_df = filtered_df[filtered_df[column] >= condition['min']]
                    if 'max' in condition:
                        filtered_df = filtered_df[filtered_df[column] <= condition['max']]
                    if 'equals' in condition:
                        filtered_df = filtered_df[filtered_df[column] == condition['equals']]
                    if 'in' in condition:
                        filtered_df = filtered_df[filtered_df[column].isin(condition['in'])]
        
        return filtered_df
    
    def _apply_aggregations(self, df: pd.DataFrame, aggregations: Dict[str, Any]) -> pd.DataFrame:
        """Apply aggregations to dataframe"""
        if not aggregations:
            return df
        
        group_by = aggregations.get('group_by')
        agg_functions = aggregations.get('functions', {})
        
        if group_by and group_by in df.columns:
            grouped = df.groupby(group_by)
            
            if agg_functions:
                result = grouped.agg(agg_functions).reset_index()
                # Flatten column names if multi-level
                if isinstance(result.columns, pd.MultiIndex):
                    result.columns = ['_'.join(col).strip() for col in result.columns.values]
                return result
            else:
                return grouped.sum().reset_index()
        
        return df
    
    async def get_sample_data(self) -> Dict[str, Any]:
        """Get sample data for testing"""
        if not self.dataframes:
            return {"data": [], "columns": [], "chart_type": "line"}
        
        # Use first available dataset
        df_name = list(self.dataframes.keys())[0]
        df = self.dataframes[df_name].head(10)
        
        # Convert timestamps to strings for JSON serialization
        sample_data = df.to_dict('records')
        for record in sample_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif hasattr(value, 'isoformat'):  # Handle datetime/timestamp
                    record[key] = value.isoformat()
        
        return {
            "data": sample_data,
            "columns": list(df.columns),
            "chart_type": "line",
            "x_axis": "Date",
            "y_axis": "Revenue",
            "title": f"Sample Data from {df_name}"
        }
