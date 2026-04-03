import React, { useState } from 'react';
import { Download, FileText, Loader2 } from 'lucide-react';

interface ExportButtonProps {
  tailoredResumeId: number;
  title?: string;
  disabled?: boolean;
  className?: string;
}

export const ExportButton: React.FC<ExportButtonProps> = ({
  tailoredResumeId,
  title = "Export Resume",
  disabled = false,
  className = ""
}) => {
  const [isExporting, setIsExporting] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState('professional');
  const [showTemplateSelector, setShowTemplateSelector] = useState(false);

  const templates = [
    { value: 'professional', label: 'Professional', description: 'Clean, traditional format' },
    { value: 'modern', label: 'Modern', description: 'Contemporary design' },
    { value: 'technical', label: 'Technical', description: 'Optimized for tech roles' },
    { value: 'creative', label: 'Creative', description: 'Expressive design' }
  ];

  const handleExport = async () => {
    if (isExporting) return;

    try {
      setIsExporting(true);
      
      // Call export API
      const response = await fetch('/api/v1/exports/docx/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tailored_resume_id: tailoredResumeId,
          template: selectedTemplate
        }),
      });

      if (!response.ok) {
        throw new Error('Export failed');
      }

      const result = await response.json();
      
      if (!result.success) {
        throw new Error(result.error || 'Export failed');
      }

      // Download the file
      const downloadUrl = result.file_metadata.download_url;
      window.open(downloadUrl, '_blank');
      
      setShowTemplateSelector(false);
      
    } catch (error) {
      console.error('Export error:', error);
      alert('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  if (showTemplateSelector) {
    return (
      <div className="relative">
        <div className="absolute top-full mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          <div className="p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Choose Template</h3>
            <div className="space-y-2">
              {templates.map((template) => (
                <label
                  key={template.value}
                  className="flex items-start space-x-2 cursor-pointer hover:bg-gray-50 p-2 rounded"
                >
                  <input
                    type="radio"
                    name="template"
                    value={template.value}
                    checked={selectedTemplate === template.value}
                    onChange={(e) => setSelectedTemplate(e.target.value)}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-900">
                      {template.label}
                    </div>
                    <div className="text-xs text-gray-500">
                      {template.description}
                    </div>
                  </div>
                </label>
              ))}
            </div>
            <div className="flex gap-2 mt-4">
              <button
                onClick={() => setShowTemplateSelector(false)}
                className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                onClick={handleExport}
                disabled={isExporting}
                className="flex-1 px-3 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                {isExporting ? (
                  <div className="flex items-center justify-center">
                    <Loader2 className="w-4 h-4 animate-spin mr-1" />
                    Exporting...
                  </div>
                ) : (
                  'Export'
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={() => setShowTemplateSelector(true)}
        disabled={disabled || isExporting}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isExporting ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Exporting...
          </>
        ) : (
          <>
            <Download className="w-4 h-4" />
            {title}
          </>
        )}
      </button>
    </div>
  );
};
