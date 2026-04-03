import React, { useState } from 'react';
import { Check, X, Edit, Eye, AlertTriangle, Info, Save, Zap } from 'lucide-react';
import { 
  DiffPreviewProps, 
  SuggestionApproval, 
  TailoringSuggestions,
  UnsupportedRequirement 
} from '@/types/tailoring';
import { SectionSuggestions } from './SectionSuggestions';
import { UnsupportedRequirements } from './UnsupportedRequirements';
import { GuardrailWarnings } from './GuardrailWarnings';

export const DiffPreview: React.FC<DiffPreviewProps> = ({
  suggestions,
  unsupportedRequirements,
  guardrailViolations,
  metadata,
  onSuggestionAction,
  onApplyAll,
  onSave,
  loading = false
}) => {
  const [activeTab, setActiveTab] = useState<'suggestions' | 'unsupported' | 'warnings'>('suggestions');
  const [expandedSections, setExpandedSections] = useState<Set<keyof TailoringSuggestions>>(
    new Set(['summary', 'skills', 'experience', 'projects'])
  );

  const handleSuggestionAction = (approval: SuggestionApproval) => {
    onSuggestionAction(approval);
  };

  const toggleSection = (section: keyof TailoringSuggestions) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  const getSuggestionStats = () => {
    let total = 0;
    let approved = 0;
    let rejected = 0;

    Object.values(suggestions).forEach(sectionSuggestions => {
      sectionSuggestions.forEach(suggestion => {
        total++;
        if (suggestion.approved) approved++;
        if (suggestion.rejected) rejected++;
      });
    });

    return { total, approved, rejected, pending: total - approved - rejected };
  };

  const stats = getSuggestionStats();

  const getTruthfulnessColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200';
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low': return 'text-blue-600 bg-blue-50 border-blue-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Tailoring Suggestions</h1>
            <p className="text-gray-600 mt-1">Review and approve resume enhancements</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={onApplyAll}
              disabled={loading || stats.pending === 0}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Zap className="w-4 h-4" />
              Apply All Approved
            </button>
            <button
              onClick={onSave}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Save className="w-4 h-4" />
              Save Progress
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-4 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
            <div className="text-sm text-gray-600">Total Suggestions</div>
          </div>
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{stats.approved}</div>
            <div className="text-sm text-gray-600">Approved</div>
          </div>
          <div className="text-center p-3 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">{stats.rejected}</div>
            <div className="text-sm text-gray-600">Rejected</div>
          </div>
          <div className="text-center p-3 bg-yellow-50 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
            <div className="text-sm text-gray-600">Pending Review</div>
          </div>
        </div>

        {/* Metadata */}
        <div className="mt-4 flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <Info className="w-4 h-4 text-gray-500" />
              Processing time: {metadata.processing_time_ms}ms
            </span>
            <span className={`flex items-center gap-1 ${getTruthfulnessColor(metadata.truthfulness_score)}`}>
              <Eye className="w-4 h-4" />
              Truthfulness score: {(metadata.truthfulness_score * 100).toFixed(0)}%
            </span>
          </div>
          <span className="text-gray-500">
            Generated: {new Date(metadata.generated_at).toLocaleString()}
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {[
              { key: 'suggestions', label: 'Suggestions', count: stats.total },
              { key: 'unsupported', label: 'Unsupported Requirements', count: unsupportedRequirements.length },
              { key: 'warnings', label: 'Guardrail Warnings', count: guardrailViolations.length }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`py-3 px-6 border-b-2 font-medium text-sm ${
                  activeTab === tab.key
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
                {tab.count > 0 && (
                  <span className="ml-2 px-2 py-1 text-xs rounded-full bg-gray-100">
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="space-y-6">
        {activeTab === 'suggestions' && (
          <div className="space-y-4">
            {Object.entries(suggestions).map(([section, sectionSuggestions]) => (
              sectionSuggestions.length > 0 && (
                <SectionSuggestions
                  key={section}
                  title={section.charAt(0).toUpperCase() + section.slice(1)}
                  icon={getSectionIcon(section)}
                  suggestions={sectionSuggestions}
                  section={section as keyof TailoringSuggestions}
                  onAction={handleSuggestionAction}
                  expanded={expandedSections.has(section as keyof TailoringSuggestions)}
                  onToggle={() => toggleSection(section as keyof TailoringSuggestions)}
                />
              )
            ))}
          </div>
        )}

        {activeTab === 'unsupported' && (
          <UnsupportedRequirements requirements={unsupportedRequirements} />
        )}

        {activeTab === 'warnings' && (
          <GuardrailWarnings violations={guardrailViolations} />
        )}
      </div>

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 flex items-center gap-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span>Processing...</span>
          </div>
        </div>
      )}
    </div>
  );
};

const getSectionIcon = (section: string): string => {
  switch (section) {
    case 'summary': return '📝';
    case 'skills': return '🛠️';
    case 'experience': return '💼';
    case 'projects': return '🚀';
    default: return '📄';
  }
};
