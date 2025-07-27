import React, { useState } from 'react';
import { GeneratedPrompt } from '../types/analysis';
import { DocumentTextIcon, ClipboardDocumentIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';

interface PromptGeneratorProps {
  prompt: GeneratedPrompt | null;
  onGeneratePrompt: () => void;
  isGenerating: boolean;
}

const PromptGenerator: React.FC<PromptGeneratorProps> = ({
  prompt,
  onGeneratePrompt,
  isGenerating,
}) => {
  const [copiedSection, setCopiedSection] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<string>('overview');

  const copyToClipboard = async (text: string, section: string = 'full') => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedSection(section);
      setTimeout(() => setCopiedSection(null), 2000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
    }
  };

  const downloadPrompt = () => {
    if (!prompt) return;
    
    const element = document.createElement('a');
    const file = new Blob([prompt.full_prompt], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `${prompt.title.toLowerCase().replace(/\s+/g, '-')}-prompt.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (!prompt) {
    return (
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
        <div className="text-center">
          <DocumentTextIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Generate Design Recreation Prompt
          </h3>
          <p className="text-gray-600 mb-6">
            Create a comprehensive markdown prompt with detailed specifications for recreating this exact design.
          </p>
          <button
            onClick={onGeneratePrompt}
            disabled={isGenerating}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isGenerating ? (
              <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2" />
            ) : (
              <DocumentTextIcon className="w-4 h-4 mr-2" />
            )}
            {isGenerating ? 'Generating...' : 'Generate Prompt'}
          </button>
        </div>
      </div>
    );
  }

  const sections = Object.entries(prompt.sections).filter(([, content]) => content.trim());

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div className="border-b border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-gray-900">{prompt.title}</h3>
            <p className="text-sm text-gray-600 mt-1">{prompt.description}</p>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => copyToClipboard(prompt.full_prompt)}
              className="inline-flex items-center px-3 py-1.5 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors text-sm"
            >
              <ClipboardDocumentIcon className="w-4 h-4 mr-1" />
              {copiedSection === 'full' ? 'Copied!' : 'Copy All'}
            </button>
            <button
              onClick={downloadPrompt}
              className="inline-flex items-center px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm"
            >
              <ArrowDownTrayIcon className="w-4 h-4 mr-1" />
              Download
            </button>
          </div>
        </div>
        
        {/* Metadata */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 pt-4 border-t border-gray-100">
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {prompt.metadata.total_colors || 0}
            </div>
            <div className="text-xs text-gray-600">Colors</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {prompt.metadata.total_typography_elements || 0}
            </div>
            <div className="text-xs text-gray-600">Typography</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {prompt.metadata.total_interactive_elements || 0}
            </div>
            <div className="text-xs text-gray-600">Components</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {Math.round((prompt.metadata.prompt_length || 0) / 1000)}k
            </div>
            <div className="text-xs text-gray-600">Characters</div>
          </div>
        </div>
      </div>

      {/* Section Navigation */}
      <div className="border-b border-gray-200">
        <div className="flex overflow-x-auto">
          {sections.map(([key, content]) => (
            <button
              key={key}
              onClick={() => setActiveSection(key)}
              className={`flex-shrink-0 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeSection === key
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Section Content */}
      <div className="p-6">
        {sections.map(([key, content]) => (
          <div
            key={key}
            className={`${activeSection === key ? 'block' : 'hidden'}`}
          >
            <div className="flex justify-between items-center mb-4">
              <h4 className="text-lg font-medium text-gray-900 capitalize">
                {key.replace('_', ' ')} Section
              </h4>
              <button
                onClick={() => copyToClipboard(content, key)}
                className="inline-flex items-center px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs hover:bg-gray-200 transition-colors"
              >
                <ClipboardDocumentIcon className="w-3 h-3 mr-1" />
                {copiedSection === key ? 'Copied!' : 'Copy'}
              </button>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
              <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono leading-relaxed">
                {content}
              </pre>
            </div>
          </div>
        ))}
      </div>

      {/* Full Prompt Preview (Hidden by default) */}
      <div className={`border-t border-gray-200 ${activeSection === 'full' ? 'block' : 'hidden'}`}>
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h4 className="text-lg font-medium text-gray-900">Complete Prompt</h4>
            <div className="text-sm text-gray-500">
              {prompt.metadata.prompt_length} characters
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
            <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono leading-relaxed">
              {prompt.full_prompt}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PromptGenerator;
