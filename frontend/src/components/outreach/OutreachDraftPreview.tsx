import React, { useState } from 'react';
import { FileText, Eye, Edit, Copy, CheckCircle, AlertCircle, Loader2, Mail, MessageSquare, Send } from 'lucide-react';

interface OutreachDraftPreviewProps {
  outreachDraftId: number;
  className?: string;
}

interface OutreachDraftData {
  id: number;
  title: string;
  draft_type: string;
  content: any;
  raw_text: string;
  scores: {
    truthfulness_score: number;
    conciseness_score: number;
    professionalism_score: number;
  };
  status: string;
  created_at: string;
  updated_at: string;
}

export const OutreachDraftPreview: React.FC<OutreachDraftPreviewProps> = ({
  outreachDraftId,
  className = ""
}) => {
  const [draft, setDraft] = useState<OutreachDraftData | null>(null);
  const [loading, setLoading] = useState(true);
  const [format, setFormat] = useState<'text' | 'structured'>('text');
  const [showEdit, setShowEdit] = useState(false);
  const [editText, setEditText] = useState('');
  const [copied, setCopied] = useState(false);

  // Fetch draft data
  React.useEffect(() => {
    const fetchDraft = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/v1/outreach-drafts/${outreachDraftId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch outreach draft');
        }
        
        const data = await response.json();
        setDraft(data);
        setEditText(data.raw_text);
      } catch (error) {
        console.error('Error fetching outreach draft:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDraft();
  }, [outreachDraftId]);

  const handleEdit = async () => {
    if (!draft) return;

    try {
      const response = await fetch(`/api/v1/outreach-drafts/${outreachDraftId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: {
            ...draft.content,
            full_text: editText
          },
          raw_text: editText
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update outreach draft');
      }

      const updatedData = await response.json();
      setDraft(updatedData);
      setShowEdit(false);
    } catch (error) {
      console.error('Error updating outreach draft:', error);
      alert('Failed to update outreach draft. Please try again.');
    }
  };

  const handleCopy = async () => {
    if (!draft) return;

    try {
      await navigator.clipboard.writeText(draft.raw_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Error copying text:', error);
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

  const getDraftIcon = (draftType: string) => {
    switch (draftType) {
      case 'email_intro': return <Mail className="w-4 h-4" />;
      case 'linkedin_note': return <MessageSquare className="w-4 h-4" />;
      case 'formal_message': return <Send className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  const getDraftTypeLabel = (draftType: string) => {
    switch (draftType) {
      case 'email_intro': return 'Email Intro';
      case 'linkedin_note': return 'LinkedIn Note';
      case 'formal_message': return 'Formal Message';
      default: return draftType.replace('_', ' ').title();
    }
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center p-8 ${className}`}>
        <Loader2 className="w-8 h-8 animate-spin mr-3" />
        <span>Loading outreach draft...</span>
      </div>
    );
  }

  if (!draft) {
    return (
      <div className={`text-center p-8 ${className}`}>
        <p className="text-gray-500">Outreach draft not found.</p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            {getDraftIcon(draft.draft_type)}
            <h2 className="text-xl font-semibold text-gray-900">{draft.title}</h2>
            <span className="px-2 py-1 text-xs font-medium rounded bg-blue-100 text-blue-700">
              {getDraftTypeLabel(draft.draft_type)}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(draft.status)} bg-gray-100`}>
              {getStatusLabel(draft.status)}
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
              <button
                onClick={handleCopy}
                className={`px-3 py-1 text-sm font-medium rounded ${
                  copied
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                <Copy className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Scores */}
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(draft.scores.truthfulness_score)}`}>
              {(draft.scores.truthfulness_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Truthfulness</div>
            <div className="text-xs text-gray-500">{getScoreLabel(draft.scores.truthfulness_score)}</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(draft.scores.conciseness_score)}`}>
              {(draft.scores.conciseness_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Conciseness</div>
            <div className="text-xs text-gray-500">{getScoreLabel(draft.scores.conciseness_score)}</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(draft.scores.professionalism_score)}`}>
              {(draft.scores.professionalism_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Professionalism</div>
            <div className="text-xs text-gray-500">{getScoreLabel(draft.scores.professionalism_score)}</div>
          </div>
        </div>

        {/* Metadata */}
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>Created: {new Date(draft.created_at).toLocaleDateString()}</span>
          <span>Updated: {new Date(draft.updated_at).toLocaleDateString()}</span>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {showEdit ? (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">Edit Outreach Draft</h3>
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
              placeholder="Edit your outreach draft..."
            />
          </div>
        ) : (
          <div className="space-y-4">
            {format === 'text' ? (
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap font-serif text-sm leading-relaxed bg-gray-50 p-4 rounded-lg">
                  {draft.raw_text}
                </pre>
              </div>
            ) : (
              <div className="space-y-4">
                {Object.entries(draft.content.sections).map(([key, value]) => (
                  <div key={key} className="space-y-2">
                    <h3 className="text-lg font-medium text-gray-900 capitalize">
                      {key.replace('_', ' ')}
                    </h3>
                    <div className="text-sm text-gray-700 bg-gray-50 p-3 rounded">
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
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span>Word count: {draft.content?.metadata?.word_count || 0}</span>
            <span>Paragraphs: {draft.content?.metadata?.paragraph_count || 0}</span>
            <span>Type: {getDraftTypeLabel(draft.draft_type)}</span>
          </div>
          {copied && (
            <div className="flex items-center gap-2 text-green-600 text-sm">
              <CheckCircle className="w-4 h-4" />
              <span>Copied to clipboard!</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
