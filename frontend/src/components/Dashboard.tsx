'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { Loader2, TrendingUp, AlertCircle } from 'lucide-react';

// Dynamically import Plotly to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { 
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-96">
      <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
    </div>
  )
});

interface DashboardProps {
  visualization: {
    plotly_json?: string;
    chart_type?: string;
    title?: string;
  } | null;
  insights: string;
  isLoading: boolean;
}

export default function Dashboard({ visualization, insights, isLoading }: DashboardProps) {
  const [plotData, setPlotData] = useState(null);
  const [plotLayout, setPlotLayout] = useState(null);

  useEffect(() => {
    if (visualization?.plotly_json) {
      try {
        const plotlyData = JSON.parse(visualization.plotly_json);
        setPlotData(plotlyData.data);
        setPlotLayout({
          ...plotlyData.layout,
          autosize: true,
          responsive: true,
          margin: { l: 50, r: 50, t: 80, b: 50 }
        });
      } catch (error) {
        console.error('Error parsing Plotly data:', error);
      }
    }
  }, [visualization]);

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-700 mb-2">
              Analyzing Your Request
            </h3>
            <p className="text-gray-500">
              Our AI is processing your data and creating the perfect visualization...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!visualization) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Visualization Section */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-gray-800">
            {visualization.title || 'Data Visualization'}
          </h3>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <TrendingUp className="h-4 w-4" />
            <span>{visualization.chart_type || 'Chart'}</span>
          </div>
        </div>

        {plotData && plotLayout ? (
          <div className="w-full">
            <Plot
              data={plotData}
              layout={plotLayout}
              config={{
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
              }}
              style={{ width: '100%', height: '500px' }}
            />
          </div>
        ) : (
          <div className="flex items-center justify-center h-96 bg-gray-50 rounded-lg">
            <div className="text-center">
              <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Unable to load visualization</p>
            </div>
          </div>
        )}
      </div>

      {/* Insights Section */}
      {insights && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
            Key Insights
          </h3>
          <div className="bg-blue-50 border-l-4 border-blue-400 p-6 rounded-r-lg">
            <div className="text-gray-700 leading-relaxed space-y-4">
              {insights.split('\n').map((line, index) => {
                // Skip empty lines
                if (!line.trim()) return null;
                
                // Handle headers (### or ##)
                if (line.startsWith('###') || line.startsWith('##')) {
                  const text = line.replace(/^#+\s*/, '').replace(/:/g, '');
                  return (
                    <h4 key={index} className="font-semibold text-lg text-blue-800 mt-6 mb-3">
                      {text}
                    </h4>
                  );
                }
                
                // Handle bullet points
                if (line.startsWith('*') || line.startsWith('-')) {
                  const text = line.replace(/^\*+\s*/, '').replace(/^\-+\s*/, '');
                  // Remove markdown bold formatting
                  const cleanText = text.replace(/\*\*(.*?)\*\*/g, '$1');
                  return (
                    <div key={index} className="flex items-start space-x-3 ml-4">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                      <p className="text-gray-700">{cleanText}</p>
                    </div>
                  );
                }
                
                // Handle regular paragraphs
                if (line.trim()) {
                  const cleanText = line.replace(/\*\*(.*?)\*\*/g, '$1');
                  return (
                    <p key={index} className="text-gray-700">
                      {cleanText}
                    </p>
                  );
                }
                
                return null;
              }).filter(Boolean)}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
