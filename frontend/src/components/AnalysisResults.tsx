import React, { useState } from 'react';
import { 
  SwatchIcon, 
  DocumentTextIcon, 
  CursorArrowRaysIcon,
  PhotoIcon,
  PaintBrushIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { AnalysisResponse } from '../types/analysis';
import PromptGenerator from './PromptGenerator';

interface AnalysisResultsProps {
  result: AnalysisResponse;
  onReset: () => void;
  onGeneratePrompt?: () => void;
  isGeneratingPrompt?: boolean;
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ 
  result, 
  onReset, 
  onGeneratePrompt,
  isGeneratingPrompt = false 
}) => {
  const [activeTab, setActiveTab] = useState<'layout' | 'colors' | 'typography' | 'elements' | 'assets' | 'guide' | 'prompt'>('layout');

  const tabs = [
    { id: 'layout' as const, name: 'Layout', icon: DocumentTextIcon },
    { id: 'colors' as const, name: 'Colors', icon: SwatchIcon },
    { id: 'typography' as const, name: 'Typography', icon: DocumentTextIcon },
    { id: 'elements' as const, name: 'Elements', icon: CursorArrowRaysIcon },
    { id: 'assets' as const, name: 'Assets', icon: PhotoIcon },
    { id: 'guide' as const, name: 'Style Guide', icon: PaintBrushIcon },
    { id: 'prompt' as const, name: 'AI Prompt', icon: DocumentTextIcon },
  ];

  const renderColorPalette = (colors: string[], title: string) => (
    <div className="space-y-2">
      <h4 className="font-medium text-gray-900">{title}</h4>
      <div className="flex flex-wrap gap-2">
        {colors.map((color, index) => (
          <div key={index} className="flex items-center space-x-2">
            <div
              className="w-8 h-8 rounded border border-gray-300"
              style={{ backgroundColor: color }}
              title={color}
            />
            <span className="text-sm font-mono text-gray-600">{color}</span>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="border-b border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Analysis Results</h2>
            <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600">
              <div className="flex items-center space-x-1">
                <ClockIcon className="w-4 h-4" />
                <span>{result.processing_time}s</span>
              </div>
              <div className="flex items-center space-x-1">
                <span>Confidence: {Math.round(result.confidence_score * 100)}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Warnings */}
        {result.warnings.length > 0 && (
          <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded-md p-3">
            <div className="flex">
              <ExclamationTriangleIcon className="w-5 h-5 text-yellow-400" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">Warnings</h3>
                <ul className="text-sm text-yellow-700 mt-1 list-disc list-inside">
                  {result.warnings.map((warning, index) => (
                    <li key={index}>{warning}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8 px-6" aria-label="Tabs">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.name}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="p-6 max-h-96 overflow-y-auto">
        {activeTab === 'layout' && (
          <div className="space-y-4">
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Layout Structure</h3>
              <div className="bg-gray-50 rounded-md p-4 space-y-2">
                <div><strong>Type:</strong> {result.layout.layout_type}</div>
                {result.layout.grid_structure && (
                  <div><strong>Grid:</strong> {result.layout.grid_structure}</div>
                )}
                <div><strong>Alignment:</strong> {result.layout.alignment}</div>
              </div>
            </div>

            <div>
              <h3 className="font-medium text-gray-900 mb-2">Spacing</h3>
              <div className="bg-gray-50 rounded-md p-4 space-y-1">
                {Object.entries(result.layout.spacing).map(([key, value]) => (
                  <div key={key}><strong>{key}:</strong> {value}</div>
                ))}
              </div>
            </div>

            {result.layout.responsive_hints && (
              <div>
                <h3 className="font-medium text-gray-900 mb-2">Responsive Hints</h3>
                <div className="bg-gray-50 rounded-md p-4">
                  <ul className="list-disc list-inside space-y-1">
                    {result.layout.responsive_hints.map((hint, index) => (
                      <li key={index}>{hint}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'colors' && (
          <div className="space-y-6">
            <div>
              <h3 className="font-medium text-gray-900 mb-4">Detected Colors</h3>
              <div className="space-y-4">
                {result.colors.map((color, index) => (
                  <div key={index} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-md">
                    <div
                      className="w-12 h-12 rounded border border-gray-300"
                      style={{ backgroundColor: color.hex_code }}
                    />
                    <div className="flex-1">
                      <div className="font-mono text-sm">{color.hex_code}</div>
                      <div className="text-sm text-gray-600">{color.usage_context}</div>
                      <div className="text-xs text-gray-500">
                        RGB: {color.rgb[0]}, {color.rgb[1]}, {color.rgb[2]} • 
                        Confidence: {Math.round(color.confidence * 100)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'typography' && (
          <div className="space-y-4">
            <h3 className="font-medium text-gray-900 mb-4">Typography Elements</h3>
            <div className="space-y-4">
              {result.typography.map((typo, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-md">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><strong>Font:</strong> {typo.font_family}</div>
                    <div><strong>Size:</strong> {typo.font_size}</div>
                    <div><strong>Weight:</strong> {typo.font_weight}</div>
                    <div><strong>Color:</strong> {typo.color}</div>
                    <div><strong>Type:</strong> {typo.element_type}</div>
                    <div><strong>Alignment:</strong> {typo.alignment}</div>
                  </div>
                  {typo.text_content && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      <strong>Content:</strong> &quot;{typo.text_content}&quot;
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'elements' && (
          <div className="space-y-4">
            <h3 className="font-medium text-gray-900 mb-4">Interactive Elements</h3>
            <div className="space-y-4">
              {result.interactive_elements.map((element, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-md">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><strong>Type:</strong> {element.element_type}</div>
                    <div><strong>Position:</strong> x: {element.position.x}, y: {element.position.y}</div>
                    <div><strong>Size:</strong> {element.dimensions.width} × {element.dimensions.height}</div>
                    {element.text_content && (
                      <div><strong>Text:</strong> {element.text_content}</div>
                    )}
                  </div>
                  {element.styling && Object.keys(element.styling).length > 0 && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      <strong>Styling:</strong>
                      <ul className="mt-1 text-sm">
                        {Object.entries(element.styling).map(([key, value]) => (
                          <li key={key}>• {key}: {value}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'assets' && (
          <div className="space-y-4">
            <h3 className="font-medium text-gray-900 mb-4">Visual Assets</h3>
            <div className="space-y-4">
              {result.assets.map((asset, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-md">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div><strong>Type:</strong> {asset.asset_type}</div>
                    <div><strong>Size:</strong> {asset.dimensions.width} × {asset.dimensions.height}</div>
                    <div><strong>Position:</strong> x: {asset.position.x}, y: {asset.position.y}</div>
                    {asset.alt_text_intent && (
                      <div><strong>Purpose:</strong> {asset.alt_text_intent}</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'guide' && (
          <div className="space-y-6">
            <div>
              <h3 className="font-medium text-gray-900 mb-4">Style Guide</h3>
              
              {renderColorPalette(result.style_guide.primary_colors, 'Primary Colors')}
              
              {result.style_guide.secondary_colors.length > 0 && (
                <div className="mt-4">
                  {renderColorPalette(result.style_guide.secondary_colors, 'Secondary Colors')}
                </div>
              )}

              <div className="mt-6">
                <h4 className="font-medium text-gray-900 mb-2">Typography Stack</h4>
                <div className="space-y-1">
                  {result.style_guide.font_stack.map((font, index) => (
                    <div key={index} className="text-sm font-mono text-gray-600">{font}</div>
                  ))}
                </div>
              </div>

              <div className="mt-6">
                <h4 className="font-medium text-gray-900 mb-2">Spacing Scale</h4>
                <div className="flex flex-wrap gap-2">
                  {result.style_guide.spacing_scale.map((space, index) => (
                    <span key={index} className="px-2 py-1 bg-gray-100 rounded text-sm font-mono">
                      {space}
                    </span>
                  ))}
                </div>
              </div>

              {Object.keys(result.style_guide.design_tokens).length > 0 && (
                <div className="mt-6">
                  <h4 className="font-medium text-gray-900 mb-2">Design Tokens</h4>
                  <div className="bg-gray-50 rounded-md p-4 space-y-1">
                    {Object.entries(result.style_guide.design_tokens).map(([key, value]) => (
                      <div key={key} className="text-sm"><strong>{key}:</strong> {value}</div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'prompt' && (
          <div className="mt-4">
            <PromptGenerator
              prompt={result.generated_prompt || null}
              onGeneratePrompt={onGeneratePrompt || (() => {})}
              isGenerating={isGeneratingPrompt}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisResults;
