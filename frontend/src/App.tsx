import React, { useState, useCallback } from 'react';
import { CloudArrowUpIcon, DocumentTextIcon, SparklesIcon } from '@heroicons/react/24/outline';
import ImageUpload from './components/ImageUpload';
import AnalysisResults from './components/AnalysisResults';
import { AnalysisResponse } from './types/analysis';
import './App.css';

function App() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGeneratingPrompt, setIsGeneratingPrompt] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageAnalysis = useCallback(async (file: File) => {
    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      // For development, use localhost directly
      const backendUrl = '/api/analyze';
      
      console.log('Attempting to connect to:', backendUrl);
      
      const response = await fetch(backendUrl, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const result: AnalysisResponse = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setIsAnalyzing(false);
    }
  }, []);

  const resetAnalysis = useCallback(() => {
    setAnalysisResult(null);
    setError(null);
  }, []);

  const handleGeneratePrompt = useCallback(async () => {
    if (!analysisResult) return;

    setIsGeneratingPrompt(true);
    setError(null);

    try {
      const response = await fetch('/api/generate-prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ analysis: analysisResult }),
      });

      if (!response.ok) {
        throw new Error(`Prompt generation failed: ${response.statusText}`);
      }

      const updatedResult: AnalysisResponse = await response.json();
      setAnalysisResult(updatedResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate prompt');
    } finally {
      setIsGeneratingPrompt(false);
    }
  }, [analysisResult]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-500 rounded-lg">
                <SparklesIcon className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Image AI</h1>
                <p className="text-sm text-gray-600">Advanced Webpage Scanner & Analyzer</p>
              </div>
            </div>
            <div className="hidden md:flex items-center space-x-6 text-sm text-gray-600">
              <div className="flex items-center space-x-2">
                <CloudArrowUpIcon className="w-5 h-5" />
                <span>Upload Screenshot</span>
              </div>
              <div className="flex items-center space-x-2">
                <DocumentTextIcon className="w-5 h-5" />
                <span>Get Detailed Analysis</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!analysisResult && !isAnalyzing && (
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Analyze Website Screenshots with AI
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Upload a website or app screenshot and get hyper-detailed analysis including 
              layout structure, colors, typography, interactive elements, and more.
            </p>
          </div>
        )}

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Analysis Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="space-y-6">
            <ImageUpload 
              onImageSelect={handleImageAnalysis}
              isAnalyzing={isAnalyzing}
              onReset={resetAnalysis}
              showReset={!!analysisResult}
            />
            
            {/* Features Section */}
            {!analysisResult && (
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Features</h3>
                <div className="space-y-3">
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <div>
                      <h4 className="font-medium text-gray-900">Layout Detection</h4>
                      <p className="text-sm text-gray-600">CSS Grid/Flexbox structure, spacing, and alignment</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <div>
                      <h4 className="font-medium text-gray-900">Color Extraction</h4>
                      <p className="text-sm text-gray-600">Precise HEX/RGB colors with usage context</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <div>
                      <h4 className="font-medium text-gray-900">Typography Analysis</h4>
                      <p className="text-sm text-gray-600">Font families, sizes, weights, and hierarchy</p>
                    </div>
                  </div>
                  <div className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                    <div>
                      <h4 className="font-medium text-gray-900">Interactive Elements</h4>
                      <p className="text-sm text-gray-600">Buttons, forms, inputs with styling details</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div>
            {analysisResult && (
              <AnalysisResults 
                result={analysisResult}
                onReset={resetAnalysis}
                onGeneratePrompt={handleGeneratePrompt}
                isGeneratingPrompt={isGeneratingPrompt}
              />
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2024 Image AI. Advanced webpage analysis powered by computer vision and machine learning.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
