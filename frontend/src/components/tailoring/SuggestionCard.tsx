import React from 'react';
import { Check, X, Edit, Eye, AlertCircle } from 'lucide-react';
import { SuggestionCardProps, SuggestionApproval } from '@/types/tailoring';

export const SuggestionCard: React.FC<SuggestionCardProps> = ({
  suggestion,
  section,
  index,
  onAction
}) => {
  const handleAction = (action: 'approve' | 'reject' | 'edit') => {
    onAction({
      section,
      suggestionIndex: index,
      action,
      user_edits: action === 'edit' ? suggestion.suggested_text || suggestion.suggested_bullet || suggestion.suggested_addition : undefined
    });
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4">
      {/* Suggestion Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-700">
              {suggestion.type.replace('_', ' ')}
            </span>
            {suggestion.jd_requirement && (
              <span className="px-2 py-1 text-xs font-medium rounded bg-blue-100 text-blue-700">
                {suggestion.jd_requirement}
              </span>
            )}
            <div className="flex items-center gap-1 ml-auto">
              <Eye className="w-4 h-4 text-gray-500" />
              <span className={`text-sm font-medium ${
                suggestion.truthfulness_score >= 0.8 ? 'text-green-600' :
                suggestion.truthfulness_score >= 0.6 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {(suggestion.truthfulness_score * 100).toFixed(0)}%
              </span>
            </div>
          </div>
          
          {/* Reasoning */}
          <div className="flex items-start gap-2 mb-3">
            <AlertCircle className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
            <p className="text-sm text-gray-700">{suggestion.reasoning}</p>
          </div>

          {/* Evidence */}
          <div className="bg-gray-50 rounded p-3 mb-3">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium text-gray-700">Evidence Source</span>
              <span className={`px-2 py-1 text-xs rounded ${
                suggestion.evidence.confidence === 'high' ? 'bg-green-100 text-green-700' :
                suggestion.evidence.confidence === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                'bg-red-100 text-red-700'
              }`}>
                {suggestion.evidence.confidence} confidence
              </span>
            </div>
            <p className="text-sm text-gray-600">{suggestion.evidence.reference}</p>
          </div>
        </div>
      </div>

      {/* Content Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        {/* Original Content */}
        {(suggestion.current_text || suggestion.current_bullet) && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Original</h4>
            <div className="p-3 bg-red-50 border border-red-200 rounded">
              <p className="text-sm text-gray-800">
                {suggestion.current_text || suggestion.current_bullet}
              </p>
            </div>
          </div>
        )}

        {/* Suggested Content */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Suggested</h4>
          <div className="p-3 bg-green-50 border border-green-200 rounded">
            <p className="text-sm text-gray-800">
              {suggestion.user_edits || suggestion.suggested_text || suggestion.suggested_bullet || suggestion.suggested_addition}
            </p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {!suggestion.approved && !suggestion.rejected && (
            <>
              <button
                onClick={() => handleAction('approve')}
                className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
              >
                <Check className="w-4 h-4" />
                Approve
              </button>
              <button
                onClick={() => handleAction('reject')}
                className="flex items-center gap-1 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
              >
                <X className="w-4 h-4" />
                Reject
              </button>
              <button
                onClick={() => handleAction('edit')}
                className="flex items-center gap-1 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
              >
                <Edit className="w-4 h-4" />
                Edit
              </button>
            </>
          )}
          
          {suggestion.approved && (
            <span className="flex items-center gap-1 px-3 py-1 bg-green-100 text-green-700 text-sm rounded">
              <Check className="w-4 h-4" />
              Approved
            </span>
          )}
          
          {suggestion.rejected && (
            <span className="flex items-center gap-1 px-3 py-1 bg-red-100 text-red-700 text-sm rounded">
              <X className="w-4 h-4" />
              Rejected
            </span>
          )}
        </div>

        {suggestion.user_edits && (
          <div className="text-xs text-blue-600">
            Custom edit applied
          </div>
        )}
      </div>
    </div>
  );
};
