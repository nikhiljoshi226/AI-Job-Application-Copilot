export interface TailoringSuggestion {
  type: 'enhancement' | 'addition' | 'bullet_enhancement' | 'description_enhancement';
  current_text?: string;
  suggested_text?: string;
  suggested_addition?: string;
  current_bullet?: string;
  suggested_bullet?: string;
  skill_name?: string;
  category?: string;
  jd_requirement?: string;
  reasoning: string;
  evidence: {
    source: string;
    confidence: string;
    reference: string;
  };
  truthfulness_score: number;
  approved?: boolean;
  rejected?: boolean;
  user_edits?: string;
}

export interface TailoringSuggestions {
  summary: TailoringSuggestion[];
  skills: TailoringSuggestion[];
  experience: TailoringSuggestion[];
  projects: TailoringSuggestion[];
}

export interface UnsupportedRequirement {
  requirement: string;
  jd_section: string;
  impact: 'low' | 'medium' | 'high';
  suggestion: string;
}

export interface GuardrailViolation {
  type: string;
  suggestion: TailoringSuggestion;
  reason: string;
}

export interface TailoringMetadata {
  total_suggestions: number;
  truthfulness_score: number;
  generated_at: string;
  processing_time_ms: number;
}

export interface TailoringResponse {
  suggestions: TailoringSuggestions;
  unsupported_requirements: UnsupportedRequirement[];
  guardrail_violations: GuardrailViolation[];
  metadata: TailoringMetadata;
  warnings?: Array<{
    type: string;
    message: string;
    violations?: GuardrailViolation[];
    unsupported?: UnsupportedRequirement[];
  }>;
}

export interface TailoringRequest {
  resume_id: number;
  job_description_id: number;
}

export interface TailoredResume {
  id: number;
  title: string;
  original_resume?: {
    id: number;
    title: string;
  };
  job_description?: {
    id: number;
    job_title: string;
    company: string;
  };
  tailored_content: TailoringResponse;
  suggestions: TailoringSuggestions;
  final_alignment_score: number;
  truthfulness_score: number;
  status: 'draft' | 'approved' | 'applied';
  created_at: string;
  updated_at: string;
}

export interface SuggestionApproval {
  section: keyof TailoringSuggestions;
  suggestionIndex: number;
  action: 'approve' | 'reject' | 'edit';
  user_edits?: string;
}

export interface DiffPreviewProps {
  suggestions: TailoringSuggestions;
  unsupportedRequirements: UnsupportedRequirement[];
  guardrailViolations: GuardrailViolation[];
  metadata: TailoringMetadata;
  onSuggestionAction: (approval: SuggestionApproval) => void;
  onApplyAll: () => void;
  onSave: () => void;
  loading?: boolean;
}

export interface SuggestionCardProps {
  suggestion: TailoringSuggestion;
  section: keyof TailoringSuggestions;
  index: number;
  onAction: (approval: SuggestionApproval) => void;
}

export interface UnsupportedRequirementCardProps {
  requirement: UnsupportedRequirement;
}

export interface SectionSuggestionsProps {
  title: string;
  icon: string;
  suggestions: TailoringSuggestion[];
  section: keyof TailoringSuggestions;
  onAction: (approval: SuggestionApproval) => void;
}
