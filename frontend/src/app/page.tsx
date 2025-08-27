'use client';

import { useState } from 'react';
import Dashboard from '@/components/Dashboard';
import PromptInput from '@/components/PromptInput';
import Header from '@/components/Header';

export default function Home() {
  const [visualization, setVisualization] = useState(null);
  const [insights, setInsights] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handlePromptSubmit = async (prompt: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/generate-dashboard`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate dashboard');
      }

      const data = await response.json();
      setVisualization(data.visualization);
      setInsights(data.insights);
    } catch (error) {
      console.error('Error generating dashboard:', error);
      setInsights('Error generating dashboard. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Prompt Input Section */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Ask Your Data Anything
            </h2>
            <p className="text-gray-600 mb-6">
              Describe what you want to see and our AI will create the perfect visualization for you.
            </p>
            <PromptInput onSubmit={handlePromptSubmit} isLoading={isLoading} />
          </div>

          {/* Dashboard Section */}
          {(visualization || isLoading) && (
            <Dashboard 
              visualization={visualization}
              insights={insights}
              isLoading={isLoading}
            />
          )}

          {/* Sample Prompts */}
          {!visualization && !isLoading && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">
                Try These Sample Prompts
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  "Show me revenue trends over time",
                  "Compare revenue by region",
                  "What's the relationship between marketing spend and revenue?",
                  "Show customer satisfaction scores by region",
                  "Display the top selling categories",
                  "How has profit margin changed over time?"
                ].map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => handlePromptSubmit(prompt)}
                    className="text-left p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                  >
                    <span className="text-blue-600 font-medium">&quot;{prompt}&quot;</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}