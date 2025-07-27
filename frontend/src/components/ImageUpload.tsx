import React, { useCallback, useState } from 'react';
import { CloudArrowUpIcon, PhotoIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  isAnalyzing: boolean;
  onReset: () => void;
  showReset: boolean;
}

const ImageUpload: React.FC<ImageUploadProps> = ({
  onImageSelect,
  isAnalyzing,
  onReset,
  showReset,
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileSelect = useCallback((file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file (PNG, JPG, SVG)');
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      alert('File size must be less than 10MB');
      return;
    }

    setSelectedFile(file);
    
    // Create preview URL
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    
    // Automatically start analysis
    onImageSelect(file);
  }, [onImageSelect]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  }, [handleFileSelect]);

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    onReset();
  };

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-blue-400 bg-blue-50'
            : selectedFile
            ? 'border-green-300 bg-green-50'
            : 'border-gray-300 bg-white hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept="image/*"
          onChange={handleFileInputChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={isAnalyzing}
        />
        
        <div className="space-y-4">
          {previewUrl ? (
            <div className="space-y-4">
              <img
                src={previewUrl}
                alt="Preview"
                className="max-w-full max-h-64 mx-auto rounded-lg shadow-sm"
              />
              <div className="flex items-center justify-center space-x-2 text-green-600">
                <PhotoIcon className="w-5 h-5" />
                <span className="font-medium">{selectedFile?.name}</span>
              </div>
            </div>
          ) : (
            <>
              <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mx-auto" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Drop your website screenshot here
                </p>
                <p className="text-sm text-gray-600">
                  or <span className="text-blue-600 font-medium">browse files</span>
                </p>
              </div>
              <div className="text-xs text-gray-500">
                Supports PNG, JPG, SVG • Max 10MB
              </div>
            </>
          )}
        </div>
      </div>

      {/* Analysis Status */}
      {isAnalyzing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <ArrowPathIcon className="w-5 h-5 text-blue-500 animate-spin" />
            <div>
              <p className="font-medium text-blue-900">Analyzing Image...</p>
              <p className="text-sm text-blue-700">
                Processing layout, colors, typography, and interactive elements
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      {showReset && !isAnalyzing && (
        <div className="flex space-x-3">
          <button
            onClick={handleReset}
            className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors font-medium"
          >
            Upload New Image
          </button>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
