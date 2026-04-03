export enum ApplicationStatus {
  PLANNED = 'planned',
  APPLIED = 'applied',
  INTERVIEW = 'interview',
  REJECTED = 'rejected',
  OFFER = 'offer'
}

export enum ApplicationPriority {
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low'
}

export enum EmploymentType {
  FULL_TIME = 'full-time',
  PART_TIME = 'part-time',
  CONTRACT = 'contract',
  INTERNSHIP = 'internship'
}

export enum RemotePolicy {
  ON_SITE = 'on-site',
  HYBRID = 'hybrid',
  REMOTE = 'remote'
}

export interface Application {
  id: number;
  company: string;
  position_title: string;
  position_level?: string;
  department?: string;
  employment_type?: EmploymentType;
  salary_min?: number;
  salary_max?: number;
  currency: string;
  location?: string;
  remote_policy?: RemotePolicy;
  status: ApplicationStatus;
  priority: ApplicationPriority;
  source?: string;
  source_url?: string;
  notes?: string;
  tags?: string[];
  created_at: string;
  planned_date?: string;
  applied_date?: string;
  interview_date?: string;
  status_updated_at?: string;
  final_status?: string;
  rejection_reason?: string;
  feedback?: string;
  // Linked resources
  job_description_id: number;
  resume_id?: number;
  tailored_resume_id?: number;
  cover_letter_id?: number;
  outreach_draft_id?: number;
}

export interface ApplicationCreate {
  company: string;
  position_title: string;
  position_level?: string;
  department?: string;
  employment_type?: EmploymentType;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  location?: string;
  remote_policy?: RemotePolicy;
  priority?: ApplicationPriority;
  source?: string;
  source_url?: string;
  notes?: string;
  tags?: string[];
  planned_date?: string;
  // Linked resources
  job_description_id: number;
  resume_id?: number;
  tailored_resume_id?: number;
  cover_letter_id?: number;
  outreach_draft_id?: number;
}

export interface ApplicationUpdate {
  company?: string;
  position_title?: string;
  position_level?: string;
  department?: string;
  employment_type?: EmploymentType;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  location?: string;
  remote_policy?: RemotePolicy;
  status?: ApplicationStatus;
  priority?: ApplicationPriority;
  source?: string;
  source_url?: string;
  notes?: string;
  tags?: string[];
  planned_date?: string;
  applied_date?: string;
  interview_date?: string;
  final_status?: string;
  rejection_reason?: string;
  feedback?: string;
  // Linked resources
  resume_id?: number;
  tailored_resume_id?: number;
  cover_letter_id?: number;
  outreach_draft_id?: number;
}

export interface ApplicationSummary {
  id: number;
  company: string;
  position_title: string;
  status: ApplicationStatus;
  priority: ApplicationPriority;
  location?: string;
  created_at: string;
  applied_date?: string;
  interview_date?: string;
  final_status?: string;
}

export interface ApplicationDashboard {
  applications: ApplicationSummary[];
  total_count: number;
  status_counts: Record<string, number>;
  priority_counts: Record<string, number>;
  recent_activity: ApplicationSummary[];
}

export interface ApplicationStatistics {
  total_applications: number;
  recent_applications: number;
  success_rate: number;
  status_distribution: Record<string, number>;
  priority_distribution: Record<string, number>;
  offers_count: number;
}

export interface ApplicationFilters {
  status?: string;
  priority?: string;
  company?: string;
  search?: string;
  skip?: number;
  limit?: number;
}

export interface ApplicationStatusOption {
  value: ApplicationStatus;
  label: string;
  description: string;
}

export interface ApplicationPriorityOption {
  value: ApplicationPriority;
  label: string;
  description: string;
}

export interface ApplicationSourceOption {
  value: string;
  label: string;
  description: string;
}

export interface ApplicationFormData {
  company: string;
  position_title: string;
  position_level: string;
  department: string;
  employment_type: string;
  salary_min: string;
  salary_max: string;
  currency: string;
  location: string;
  remote_policy: string;
  priority: ApplicationPriority;
  source: string;
  source_url: string;
  notes: string;
  tags: string[];
  planned_date: string;
  job_description_id: number;
  resume_id?: number;
  tailored_resume_id?: number;
  cover_letter_id?: number;
  outreach_draft_id?: number;
}
