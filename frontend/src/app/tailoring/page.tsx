'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { DiffPreview } from '@/components/tailoring/DiffPreview';
import { 
  TailoringResponse, 
  TailoringRequest, 
  SuggestionApproval, 
  TailoredResume 
} from '@/types/tailoring';

export default function TailoringPage() {
  const params = useParams();
  const router = useRouter();
  const resumeId = parseInt(params.resumeId as string);
  const jobDescriptionId = parseInt(params.jobDescriptionId as string);

  const [tailoringData, setTailoringData] = useState<TailoringResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [applying, setApplying] = useState(false);

  // Generate tailoring suggestions
  useEffect(() => {
    const generateSuggestions = async () => {
      if (!resumeId || !jobDescriptionId) {
        setError('Missing resume or job description ID');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const request: TailoringRequest = {
          resume_id: resumeId,
          job_description_id: jobDescriptionId
        };

        const response = await fetch('/api/v1/tailoring/generate-suggestions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request),
        });

        if (!response.ok) {
          throw new Error(`Failed to generate suggestions: ${response.statusText}`);
        }

        const data = await response.json();
        setTailoringData(data.suggestions);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to generate suggestions');
      } finally {
        setLoading(false);
      }
    };

    generateSuggestions();
  }, [resumeId, jobDescriptionId]);

  // Handle suggestion actions (approve, reject, edit)
  const handleSuggestionAction = async (approval: SuggestionApproval) => {
    if (!tailoringData) return;

    // Update local state immediately for responsive UI
    const updatedSuggestions = { ...tailoringData.suggestions };
    const suggestion = updatedSuggestions[approval.section][approval.suggestionIndex];

    if (approval.action === 'approve') {
      suggestion.approved = true;
      suggestion.rejected = false;
      suggestion.user_edits = approval.user_edits;
    } else if (approval.action === 'reject') {
      suggestion.approved = false;
      suggestion.rejected = true;
    } else if (approval.action === 'edit') {
      suggestion.approved = true;
      suggestion.rejected = false;
      suggestion.user_edits = approval.user_edits;
    }

    setTailoringData({
      ...tailoringData,
      suggestions: updatedSuggestions
    });
  };

  // Save progress
  const handleSave = async () => {
    if (!tailoringData) return;

    try {
      setSaving(true);
      
      // Create a tailored resume with current state
      const response = await fetch('/api/v1/tailoring/apply-suggestions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_id: resumeId,
          job_description_id: jobDescriptionId,
          suggestions: tailoringData
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to save progress: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Progress saved:', result);
      
      // Show success message (you could add a toast notification here)
      alert('Progress saved successfully!');
    } catch (err) {
      console.error('Save error:', err);
      alert(err instanceof Error ? err.message : 'Failed to save progress');
    } finally {
      setSaving(false);
    }
  };

  // Apply all approved suggestions
  const handleApplyAll = async () => {
    if (!tailoringData) return;

    // Check if there are approved suggestions
    let approvedCount = 0;
    Object.values(tailoringData.suggestions).forEach(sectionSuggestions => {
      sectionSuggestions.forEach(suggestion => {
        if (suggestion.approved && !suggestion.rejected) {
          approvedCount++;
        }
      });
    });

    if (approvedCount === 0) {
      alert('No approved suggestions to apply. Please approve some suggestions first.');
      return;
    }

    try {
      setApplying(true);
      
      const response = await fetch('/api/v1/tailoring/apply-suggestions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          resume_id: resumeId,
          job_description_id: jobDescriptionId,
          suggestions: tailoringData
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to apply suggestions: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Suggestions applied:', result);
      
      // Redirect to the tailored resume page
      router.push(`/tailored-resumes/${result.tailored_resume_id}`);
    } catch (err) {
      console.error('Apply error:', err);
      alert(err instanceof Error ? err.message : 'Failed to apply suggestions');
    } finally {
      setApplying(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Generating Tailoring Suggestions</h2>
          <p className="text-gray-600">Analyzing your resume and the job description...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="bg-red-100 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => router.back()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!tailoringData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Data Available</h2>
          <p className="text-gray-600">Unable to load tailoring suggestions.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <DiffPreview
        suggestions={tailoringData.suggestions}
        unsupportedRequirements={tailoringData.unsupported_requirements}
        guardrailViolations={tailoringData.guardrail_violations}
        metadata={tailoringData.metadata}
        onSuggestionAction={handleSuggestionAction}
        onApplyAll={handleApplyAll}
        onSave={handleSave}
        loading={saving || applying}
      />
    </div>
  );
}
