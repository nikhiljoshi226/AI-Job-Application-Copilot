import React, { useState } from 'react';
import { FileText, Eye, Edit, Download, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';

interface CoverLetterPreviewProps {
  coverLetterId: number;
  className?: string;
}

interface CoverLetterData {
  id: number;
  title: string;
  content: any;
  raw_text: string;
  scores: {
    truthfulness_score: number;
    grammar_score: number;
    personalization_score: number;
  };
  status: string;
  created_at: string;
  updated_at: string;
}

export const CoverLetterPreview: React.FC<CoverLetterPreviewProps> = ({
  coverLetterId,
  className = ""
}) => {
  const [coverLetter, setCoverLetter] = useState<CoverLetterData | null>(null);
  const [loading, setLoading] = useState(true);
  const [format, setFormat] = useState<'text' | 'structured'>('text');
  const [showEdit, setShowEdit] = useState(false);
  const [editText, setEditText] = useState('');

  // Fetch cover letter data
  React.useEffect(() => {
    const fetchCoverLetter = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/v1/cover-letters/${coverLetterId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch cover letter');
        }
        
        const data = await response.json();
        setCoverLetter(data);
        setEditText(data.raw_text);
      } catch (error) {
        console.error('Error fetching cover letter:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCoverLetter();
  }, [coverLetterId]);

  const handleEdit = async () => {
    if (!coverLetter) return;

    try {
      const response = await fetch(`/api/v1/cover-letters/${coverLetterId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: {
            ...coverLetter.content,
            full_text: editText
          },
          raw_text: editText
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update cover letter');
      }

      const updatedData = await response.json();
      setCoverLetter(updatedData);
      setShowEdit(false);
    } catch (error) {
      console.error('Error updating cover letter:', error);
      alert('Failed to update cover letter. Please try again.');
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    return 'Needs Improvement';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'text-gray-600';
      case 'approved': return 'text-green-600';
      case 'sent': return 'text-blue-600';
      case 'archived': return 'text-gray-400';
      default: return 'text-gray-600';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'draft': return 'Draft';
      case 'approved': return 'Approved';
      case 'sent': return 'Sent';
      case 'archived': return 'Archived';
      default: return status;
    }
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center p-8 ${className}`}>
        <Loader2 className="w-8 h-8 animate-spin mr-3" />
        <span>Loading cover letter...</span>
      </div>
    );
  }

  if (!coverLetter) {
    return (
      <div className={`text-center p-8 ${className}`}>
        <p className="text-gray-500">Cover letter not found.</p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">{coverLetter.title}</h2>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(coverLetter.status)} bg-gray-100`}>
              {getStatusLabel(coverLetter.status)}
            </span>
            <div className="flex gap-1">
              <button
                onClick={() => setFormat(format === 'text' ? 'structured' : 'text')}
                className={`px-3 py-1 text-sm font-medium rounded ${
                  format === 'text' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                {format === 'text' ? <FileText className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
              <button
                onClick={() => setShowEdit(!showEdit)}
                className={`px-3 py-1 text-sm font-medium rounded ${
                  showEdit 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                <Edit className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Scores */}
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(coverLetter.scores.truthfulness_score)}`}>
              {(coverLetter.scores.truthfulness_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Truthfulness</div>
            <div className="text-xs text-gray-500">{getScoreLabel(coverLetter.scores.truthfulness_score)}</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(coverLetter.scores.grammar_score)}`}>
              {(coverLetter.scores.grammar_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Grammar</div>
            <div className="text-xs text-gray-500">{getScoreLabel(coverLetter.scores.grammar_score)}</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(coverLetter.scores.personalization_score)}`}>
              {(coverLetter.scores.personalization_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Personalization</div>
            <div className="text-xs text-gray-500">{getScoreLabel(coverLetter.scores.personalization_score)}</div>
          </div>
        </div>

        {/* Metadata */}
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>Created: {new Date(coverLetter.created_at).toLocaleDateString()}</span>
          <span>Updated: {new Date(coverLetter.updated_at).toLocaleDateString()}</span>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {showEdit ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">Edit Cover Letter</h3>
              <div className="flex gap-2">
                <button
                  onClick={handleEdit}
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  <CheckCircle className="w-4 h-4 mr-1" />
                  Save
                </button>
                <button
                  onClick={() => setShowEdit(false)}
                  className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
                >
                  Cancel
                </button>
              </div>
            </div>
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              className="w-full h-64 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Edit your cover letter..."
            />
          </div>
        ) : (
          <div className="space-y-4">
            {format === 'text' ? (
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap font-serif text-sm leading-relaxed">
                  {coverLetter.raw_text}
                </pre>
              </div>
            ) : (
              <div className="space-y-4">
                {Object.entries(coverLetter.content.sections).map(([key, value]) => (
                  <div key={key} className="space-y-2">
                    <h3 className="text-lg font-medium text-gray-900 capitalize">
                      {key.replace('_', ' ')}
                    </h3>
                    <div className="text-sm text-gray-700">
                      {typeof value === 'string' ? (
                        value
                      ) : (
                        <div className="space-y-2">
                          {Array.isArray(value) ? (
                            value.map((item, index) => (
                              <div key={index}>{item}</div>
                            ))
                          ) : (
                            <div>{String(value)}</div>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>Word count: {coverLetter.content?.metadata?.word_count || 0}</span>
          <span>Paragraphs: {coverLetter.content?.metadata?.paragraph_count || 0}</span>
        </div>
      </div>
    </div>
  );
};
