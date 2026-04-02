# AI Job Application Copilot - MVP Implementation Specification

## Document Information

**Version:** 1.0  
**Date:** April 1, 2026  
**Status:** Ready for Implementation  
**Estimated Timeline:** 6-8 weeks (solo developer)

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Architecture](#architecture)
4. [Data Models](#data-models)
5. [API Endpoints](#api-endpoints)
6. [Frontend Pages & Components](#frontend-pages--components)
7. [Backend Services](#backend-services)
8. [Validation Rules](#validation-rules)
9. [Test Strategy](#test-strategy)
10. [Implementation Tasks](#implementation-tasks)

---

## Overview

### MVP Scope

The MVP delivers the core job application workflow:
1. User uploads resume → System parses into structured JSON
2. User pastes job description → System parses into structured JSON
3. System analyzes fit between resume and JD
4. System generates truthful tailoring suggestions
5. User reviews suggestions with diff preview
6. User approves/rejects individual suggestions
7. System generates tailored resume as DOCX
8. User downloads tailored resume
9. System creates application tracker entry

### Out of Scope (Post-MVP)

- Cover letter generation
- Recruiter outreach drafts
- Interview prep generation
- Skill gap analysis
- Multiple resume versions
- PDF export
- Resume editing UI
- Email notifications
- Advanced analytics

### Success Criteria

- User can complete full flow in < 5 minutes
- Resume parsing accuracy > 90%
- JD parsing extracts all key requirements
- Fit analysis clearly shows matches/gaps
- Tailoring suggestions are truthful (no fabrication)
- Generated resume is ATS-friendly
- All critical paths have test coverage



---

## Requirements

### Functional Requirements

**FR1: Resume Management**
- FR1.1: User can upload resume (PDF, DOCX, TXT)
- FR1.2: System validates file type and size (max 5MB)
- FR1.3: System extracts text from uploaded file
- FR1.4: System parses resume into structured JSON
- FR1.5: User can view parsed resume data
- FR1.6: User can delete uploaded resumes
- FR1.7: System stores original file in cloud storage

**FR2: Job Description Management**
- FR2.1: User can paste job description text
- FR2.2: System parses JD into structured requirements
- FR2.3: System extracts: company, title, skills, responsibilities
- FR2.4: User can view parsed JD data
- FR2.5: System stores JD for future reference

**FR3: Fit Analysis**
- FR3.1: System compares resume against JD requirements
- FR3.2: System categorizes matches: Strong, Partial, Missing
- FR3.3: System provides evidence for each match
- FR3.4: System calculates overall match percentage
- FR3.5: User can view fit analysis results visually

**FR4: Resume Tailoring**
- FR4.1: System generates tailoring suggestions based on fit analysis
- FR4.2: Suggestions include: reorder, rephrase, emphasize
- FR4.3: Each suggestion includes reasoning and evidence
- FR4.4: System never fabricates experience or skills
- FR4.5: User can view before/after diff for each suggestion
- FR4.6: User can accept, reject, or edit individual suggestions
- FR4.7: System tracks which suggestions are approved

**FR5: Resume Generation**
- FR5.1: System generates tailored resume only after user approval
- FR5.2: System applies approved suggestions to resume data
- FR5.3: System generates DOCX file with proper formatting
- FR5.4: User can preview generated resume
- FR5.5: User can download DOCX file
- FR5.6: Generated resume is ATS-friendly

**FR6: Application Tracking**
- FR6.1: System creates application record after resume generation
- FR6.2: Application includes: company, title, date, status
- FR6.3: User can view list of applications
- FR6.4: User can update application status
- FR6.5: Application links to resume and JD used

### Non-Functional Requirements

**NFR1: Performance**
- Resume parsing: < 15 seconds
- JD parsing: < 10 seconds
- Fit analysis: < 10 seconds
- Tailoring generation: < 15 seconds
- Resume generation: < 10 seconds
- Page load time: < 2 seconds

**NFR2: Security**
- All API endpoints require authentication
- Users can only access their own data
- File uploads are validated and sanitized
- Sensitive data is encrypted at rest
- API keys stored in environment variables

**NFR3: Reliability**
- AI output validation prevents fabrication
- Graceful error handling for all operations
- Data persistence for all user actions
- Automatic retry for transient failures

**NFR4: Usability**
- Clear error messages for all failures
- Loading states for all async operations
- Responsive design (mobile, tablet, desktop)
- Accessible (WCAG AA minimum)

**NFR5: Maintainability**
- Clean code following style guidelines
- Comprehensive logging for debugging
- Test coverage > 70% for critical paths
- Clear documentation for setup and deployment



---

## Architecture

### Technology Stack

**Frontend:**
- Framework: Next.js 14 (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- State: React Context + Custom Hooks
- HTTP Client: Fetch API

**Backend:**
- Framework: FastAPI (Python 3.11+)
- Database: Supabase Postgres
- ORM: SQLAlchemy
- Migrations: Alembic
- File Storage: Supabase Storage
- AI: OpenAI API (GPT-4 for analysis, GPT-3.5 for parsing)

**Infrastructure:**
- Frontend Hosting: Vercel
- Backend Hosting: Railway / Render
- Database: Supabase (managed Postgres)
- Storage: Supabase Storage
- Auth: Supabase Auth

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Resumes  │  │   New    │  │   Apps   │   │
│  │          │  │          │  │   App    │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    API Routes                         │  │
│  │  /resumes  /job-descriptions  /analysis  /generate   │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Services                           │  │
│  │  ResumeParser  JDParser  FitAnalysis  Tailoring      │  │
│  │  ResumeGenerator  ApplicationService                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Repositories                         │  │
│  │  ResumeRepo  JDRepo  AnalysisRepo  ApplicationRepo   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                    │                    │
                    │                    │
                    ▼                    ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  Supabase        │  │  OpenAI API      │
        │  - Postgres      │  │  - GPT-4         │
        │  - Storage       │  │  - GPT-3.5       │
        │  - Auth          │  │                  │
        └──────────────────┘  └──────────────────┘
```

### Service Layer Architecture

```
Router (HTTP) → Service (Business Logic) → Repository (Data Access)
                    ↓
                AI Client (External API)
                    ↓
                Validation (Schema + Business Rules)
```

### Data Flow: Resume Upload to Tailored Resume

```
1. User uploads file
   ↓
2. Frontend validates file (type, size)
   ↓
3. POST /api/resumes/upload
   ↓
4. Backend validates file
   ↓
5. Extract text from file
   ↓
6. Send to OpenAI for parsing
   ↓
7. Validate parsed data (Pydantic)
   ↓
8. Store file in Supabase Storage
   ↓
9. Save parsed data to database
   ↓
10. Return resume to frontend
    ↓
11. User pastes JD
    ↓
12. POST /api/job-descriptions
    ↓
13. Parse JD with OpenAI
    ↓
14. Validate and store
    ↓
15. POST /api/analysis/fit
    ↓
16. Compare resume vs JD
    ↓
17. Return fit analysis
    ↓
18. POST /api/analysis/tailoring
    ↓
19. Generate suggestions
    ↓
20. User reviews and approves
    ↓
21. POST /api/generate/resume
    ↓
22. Apply approved suggestions
    ↓
23. Generate DOCX with python-docx
    ↓
24. Upload to storage
    ↓
25. Return download URL
    ↓
26. POST /api/applications
    ↓
27. Create application record
    ↓
28. User downloads resume
```



---

## Data Models

### Database Schema

**users** (managed by Supabase Auth)
```sql
id: UUID (PK)
email: VARCHAR(255)
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

**resumes**
```sql
id: UUID (PK)
user_id: UUID (FK → users.id)
name: VARCHAR(255)
parsed_data: JSONB
original_file_url: VARCHAR(500)
created_at: TIMESTAMP
updated_at: TIMESTAMP

INDEX idx_resumes_user_id ON resumes(user_id)
INDEX idx_resumes_created_at ON resumes(created_at)
```

**job_descriptions**
```sql
id: UUID (PK)
user_id: UUID (FK → users.id)
company: VARCHAR(255)
title: VARCHAR(255)
raw_text: TEXT
parsed_data: JSONB
created_at: TIMESTAMP

INDEX idx_jd_user_id ON job_descriptions(user_id)
INDEX idx_jd_created_at ON job_descriptions(created_at)
```

**fit_analyses**
```sql
id: UUID (PK)
user_id: UUID (FK → users.id)
resume_id: UUID (FK → resumes.id)
job_description_id: UUID (FK → job_descriptions.id)
analysis_data: JSONB
overall_score: DECIMAL(5,2)
created_at: TIMESTAMP

INDEX idx_fit_resume_id ON fit_analyses(resume_id)
INDEX idx_fit_jd_id ON fit_analyses(job_description_id)
```

**tailoring_suggestions**
```sql
id: UUID (PK)
user_id: UUID (FK → users.id)
fit_analysis_id: UUID (FK → fit_analyses.id)
suggestions: JSONB
approved_suggestions: JSONB
user_approved: BOOLEAN DEFAULT FALSE
created_at: TIMESTAMP
updated_at: TIMESTAMP

INDEX idx_tailoring_fit_id ON tailoring_suggestions(fit_analysis_id)
```

**generated_resumes**
```sql
id: UUID (PK)
user_id: UUID (FK → users.id)
resume_id: UUID (FK → resumes.id)
tailoring_id: UUID (FK → tailoring_suggestions.id)
file_url: VARCHAR(500)
created_at: TIMESTAMP

INDEX idx_generated_user_id ON generated_resumes(user_id)
```

**applications**
```sql
id: UUID (PK)
user_id: UUID (FK → users.id)
resume_id: UUID (FK → resumes.id)
job_description_id: UUID (FK → job_descriptions.id)
generated_resume_id: UUID (FK → generated_resumes.id, nullable)
company: VARCHAR(255)
title: VARCHAR(255)
status: VARCHAR(50) DEFAULT 'applied'
applied_date: DATE
notes: TEXT
created_at: TIMESTAMP
updated_at: TIMESTAMP

INDEX idx_app_user_id ON applications(user_id)
INDEX idx_app_status ON applications(status)
INDEX idx_app_date ON applications(applied_date)
```



### JSON Data Structures

**ResumeData (parsed_data in resumes table)**
```json
{
  "contact": {
    "name": "string",
    "email": "string",
    "phone": "string | null",
    "location": "string | null",
    "linkedin": "string | null",
    "github": "string | null",
    "portfolio": "string | null"
  },
  "summary": "string | null",
  "experience": [
    {
      "company": "string",
      "title": "string",
      "start_date": "string | null",
      "end_date": "string | null",
      "location": "string | null",
      "bullets": ["string"]
    }
  ],
  "education": [
    {
      "institution": "string",
      "degree": "string",
      "field": "string | null",
      "start_date": "string | null",
      "end_date": "string | null",
      "gpa": "string | null",
      "achievements": ["string"]
    }
  ],
  "skills": {
    "languages": ["string"],
    "frameworks": ["string"],
    "tools": ["string"],
    "other": ["string"]
  },
  "projects": [
    {
      "name": "string",
      "description": "string",
      "technologies": ["string"],
      "bullets": ["string"],
      "url": "string | null"
    }
  ],
  "certifications": [
    {
      "name": "string",
      "issuer": "string | null",
      "date": "string | null"
    }
  ]
}
```

**JobDescriptionData (parsed_data in job_descriptions table)**
```json
{
  "company": "string",
  "title": "string",
  "location": "string | null",
  "job_type": "string | null",
  "salary_range": "string | null",
  "requirements": {
    "technical_skills": [
      {
        "skill": "string",
        "required": true,
        "years": "number | null"
      }
    ],
    "soft_skills": ["string"],
    "education": ["string"],
    "experience_years": "number | null",
    "certifications": ["string"]
  },
  "responsibilities": ["string"],
  "nice_to_have": ["string"],
  "keywords": ["string"]
}
```

**FitAnalysisData (analysis_data in fit_analyses table)**
```json
{
  "overall_score": 0.75,
  "matches": {
    "strong": [
      {
        "requirement": "Python",
        "evidence": ["Built REST API with FastAPI", "3 Python projects"],
        "confidence": "high"
      }
    ],
    "partial": [
      {
        "requirement": "AWS",
        "evidence": ["Used cloud deployment"],
        "confidence": "medium",
        "gap": "No specific AWS services mentioned"
      }
    ],
    "missing": [
      {
        "requirement": "Kubernetes",
        "evidence": [],
        "confidence": "none"
      }
    ]
  },
  "keyword_coverage": 0.68
}
```

**TailoringSuggestions (suggestions in tailoring_suggestions table)**
```json
{
  "suggestions": [
    {
      "id": "string",
      "type": "reorder | rephrase | emphasize",
      "section": "experience | projects | skills | education | summary",
      "item_id": "string",
      "bullet_index": "number | null",
      "original": "string | null",
      "suggested": "string | null",
      "reason": "string",
      "evidence": ["string"],
      "jd_alignment": ["string"]
    }
  ]
}
```

**ApprovedSuggestions (approved_suggestions in tailoring_suggestions table)**
```json
{
  "approved": ["suggestion_id_1", "suggestion_id_2"],
  "rejected": ["suggestion_id_3"],
  "edited": [
    {
      "suggestion_id": "string",
      "custom_text": "string"
    }
  ]
}
```



---

## API Endpoints

### Authentication
All endpoints require Bearer token authentication (Supabase JWT).

### Resume Endpoints

**POST /api/resumes/upload**
- Description: Upload and parse resume
- Request: multipart/form-data with file
- Response: ResumeResponse
- Status: 201 Created
- Errors: 400 (invalid file), 401 (unauthorized), 422 (parsing failed)

```typescript
// Response
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Software Engineer Resume",
  "parsed_data": ResumeData,
  "original_file_url": "https://...",
  "created_at": "2026-04-01T10:00:00Z",
  "updated_at": "2026-04-01T10:00:00Z"
}
```

**GET /api/resumes**
- Description: List user's resumes
- Response: ResumeListResponse
- Status: 200 OK

```typescript
// Response
{
  "resumes": [ResumeResponse],
  "total": 5
}
```

**GET /api/resumes/{id}**
- Description: Get resume by ID
- Response: ResumeResponse
- Status: 200 OK
- Errors: 404 (not found), 403 (forbidden)

**DELETE /api/resumes/{id}**
- Description: Delete resume
- Response: 204 No Content
- Errors: 404 (not found), 403 (forbidden)

### Job Description Endpoints

**POST /api/job-descriptions**
- Description: Parse and save job description
- Request: CreateJobDescriptionRequest
- Response: JobDescriptionResponse
- Status: 201 Created

```typescript
// Request
{
  "raw_text": "string",
  "company": "string (optional, auto-extracted)",
  "title": "string (optional, auto-extracted)"
}

// Response
{
  "id": "uuid",
  "user_id": "uuid",
  "company": "string",
  "title": "string",
  "raw_text": "string",
  "parsed_data": JobDescriptionData,
  "created_at": "2026-04-01T10:00:00Z"
}
```

**GET /api/job-descriptions**
- Description: List user's job descriptions
- Response: JobDescriptionListResponse
- Status: 200 OK

**GET /api/job-descriptions/{id}**
- Description: Get job description by ID
- Response: JobDescriptionResponse
- Status: 200 OK

**DELETE /api/job-descriptions/{id}**
- Description: Delete job description
- Response: 204 No Content

### Analysis Endpoints

**POST /api/analysis/fit**
- Description: Analyze fit between resume and JD
- Request: CreateFitAnalysisRequest
- Response: FitAnalysisResponse
- Status: 201 Created

```typescript
// Request
{
  "resume_id": "uuid",
  "job_description_id": "uuid"
}

// Response
{
  "id": "uuid",
  "resume_id": "uuid",
  "job_description_id": "uuid",
  "analysis_data": FitAnalysisData,
  "overall_score": 0.75,
  "created_at": "2026-04-01T10:00:00Z"
}
```

**GET /api/analysis/fit/{id}**
- Description: Get fit analysis by ID
- Response: FitAnalysisResponse
- Status: 200 OK

**POST /api/analysis/tailoring**
- Description: Generate tailoring suggestions
- Request: CreateTailoringRequest
- Response: TailoringResponse
- Status: 201 Created

```typescript
// Request
{
  "fit_analysis_id": "uuid"
}

// Response
{
  "id": "uuid",
  "fit_analysis_id": "uuid",
  "suggestions": TailoringSuggestions,
  "user_approved": false,
  "created_at": "2026-04-01T10:00:00Z"
}
```

**PATCH /api/analysis/tailoring/{id}/approve**
- Description: Approve/reject suggestions
- Request: ApproveSuggestionsRequest
- Response: TailoringResponse
- Status: 200 OK

```typescript
// Request
{
  "approved": ["suggestion_id_1"],
  "rejected": ["suggestion_id_2"],
  "edited": [
    {
      "suggestion_id": "string",
      "custom_text": "string"
    }
  ]
}
```

**GET /api/analysis/tailoring/{id}**
- Description: Get tailoring suggestions by ID
- Response: TailoringResponse
- Status: 200 OK

### Generation Endpoints

**POST /api/generate/resume**
- Description: Generate tailored resume DOCX
- Request: GenerateResumeRequest
- Response: GeneratedResumeResponse
- Status: 201 Created

```typescript
// Request
{
  "resume_id": "uuid",
  "tailoring_id": "uuid"
}

// Response
{
  "id": "uuid",
  "resume_id": "uuid",
  "tailoring_id": "uuid",
  "file_url": "https://...",
  "created_at": "2026-04-01T10:00:00Z"
}
```

**GET /api/generate/resume/{id}**
- Description: Get generated resume info
- Response: GeneratedResumeResponse
- Status: 200 OK

### Application Endpoints

**POST /api/applications**
- Description: Create application record
- Request: CreateApplicationRequest
- Response: ApplicationResponse
- Status: 201 Created

```typescript
// Request
{
  "resume_id": "uuid",
  "job_description_id": "uuid",
  "generated_resume_id": "uuid (optional)",
  "company": "string",
  "title": "string",
  "applied_date": "2026-04-01",
  "notes": "string (optional)"
}

// Response
{
  "id": "uuid",
  "user_id": "uuid",
  "resume_id": "uuid",
  "job_description_id": "uuid",
  "generated_resume_id": "uuid | null",
  "company": "string",
  "title": "string",
  "status": "applied",
  "applied_date": "2026-04-01",
  "notes": "string | null",
  "created_at": "2026-04-01T10:00:00Z",
  "updated_at": "2026-04-01T10:00:00Z"
}
```

**GET /api/applications**
- Description: List user's applications
- Query: ?status=applied&limit=20&offset=0
- Response: ApplicationListResponse
- Status: 200 OK

**GET /api/applications/{id}**
- Description: Get application by ID
- Response: ApplicationResponse
- Status: 200 OK

**PATCH /api/applications/{id}**
- Description: Update application
- Request: UpdateApplicationRequest
- Response: ApplicationResponse
- Status: 200 OK

```typescript
// Request
{
  "status": "interviewing | offer | rejected | withdrawn",
  "notes": "string (optional)"
}
```

**DELETE /api/applications/{id}**
- Description: Delete application
- Response: 204 No Content



---

## Frontend Pages & Components

### Page Structure

**1. Dashboard (`/dashboard`)**
- Purpose: Central hub for quick actions and recent activity
- Components:
  - QuickActionCards (Upload Resume, New Application)
  - RecentApplicationsList (5 most recent)
  - ResumeLibraryPreview (3 most recent resumes)
- State: Fetch recent applications and resumes on mount
- Actions: Navigate to upload, new application, or view details

**2. Resumes List (`/resumes`)**
- Purpose: View and manage all uploaded resumes
- Components:
  - ResumeCard (grid layout)
  - UploadResumeButton
  - EmptyState (if no resumes)
- State: List of resumes, loading, error
- Actions: Upload, view, delete resume

**3. Resume Upload (`/resumes/upload`)**
- Purpose: Upload and parse new resume
- Components:
  - FileDropZone
  - FileUploadProgress
  - ParsedResumePreview
- Flow:
  1. User drops/selects file
  2. Validate file client-side
  3. Upload to API
  4. Show parsing progress
  5. Display parsed data for review
  6. Confirm or re-upload
- State: file, uploading, parsing, parsed data, error

**4. Resume Detail (`/resumes/[id]`)**
- Purpose: View parsed resume data
- Components:
  - ResumeDataDisplay (structured view)
  - ActionButtons (Use for Application, Delete)
- State: Resume data, loading, error
- Actions: Navigate to new application, delete

**5. New Application Flow (`/applications/new`)**
- Multi-step flow with progress indicator

**Step 1: Select Resume (`/applications/new/select-resume`)**
- Components:
  - ResumeSelectionGrid
  - UploadNewResumeLink
- State: Resumes list, selected resume
- Actions: Select resume, proceed to JD input

**Step 2: Job Description Input (`/applications/new/job-description`)**
- Components:
  - JDTextarea (large, with character count)
  - CompanyTitleInputs (optional, auto-filled from parsing)
  - AnalyzeButton
- State: JD text, company, title, parsing, error
- Actions: Parse JD, proceed to fit analysis

**Step 3: Fit Analysis (`/applications/new/fit-analysis`)**
- Components:
  - OverallMatchScore (progress bar)
  - StrongMatchesList (green, expandable)
  - PartialMatchesList (amber, expandable)
  - MissingRequirementsList (red, expandable)
  - ContinueButton
- State: Fit analysis data, loading, error
- Actions: View details, proceed to tailoring

**Step 4: Tailoring Suggestions (`/applications/new/tailoring`)**
- Components:
  - SuggestionCard (for each suggestion)
  - DiffViewer (before/after comparison)
  - ApprovalButtons (Accept, Reject, Edit)
  - BulkActions (Accept All, Reject All)
  - PreviewButton
- State: Suggestions, approved/rejected/edited, loading, error
- Actions: Accept, reject, edit suggestions, preview

**Step 5: Preview & Generate (`/applications/new/preview`)**
- Components:
  - ResumePreview (formatted view with highlights)
  - ChangesSummary (X suggestions applied)
  - GenerateButton
  - BackButton
- State: Preview data, generating, generated resume URL
- Actions: Go back to edit, generate resume

**Step 6: Success & Download (`/applications/new/success`)**
- Components:
  - SuccessMessage
  - DownloadButton
  - SaveToApplicationsButton
  - StartNewApplicationButton
- State: Generated resume URL, application saved
- Actions: Download, save to tracker, start new

**6. Applications List (`/applications`)**
- Purpose: View and manage all applications
- Components:
  - ApplicationCard (list layout)
  - FilterButtons (All, Applied, Interviewing, Offer, Rejected)
  - SortDropdown (Date, Company, Status)
  - EmptyState
- State: Applications list, filters, loading, error
- Actions: View details, update status, delete

**7. Application Detail (`/applications/[id]`)**
- Purpose: View application details
- Components:
  - ApplicationHeader (company, title, status, date)
  - JobDescriptionSection (collapsible)
  - ResumeUsedSection (link to resume)
  - FitAnalysisSection (link to analysis)
  - GeneratedResumeSection (download link)
  - NotesSection (editable)
  - StatusUpdateButtons
  - TimelineSection (status changes)
- State: Application data, loading, error
- Actions: Update status, edit notes, download resume, delete



### Component Library

**UI Components (components/ui/)**
- Button (variants: primary, secondary, danger, ghost)
- Card (container with header, content, actions)
- Input (text, textarea, with validation)
- Badge (status indicators)
- Modal (confirmations, forms)
- Toast (notifications)
- LoadingSpinner
- ProgressBar
- Dropdown

**Resume Components (components/resume/)**
- ResumeCard (display resume in grid)
- ResumeUpload (file drop zone)
- ResumePreview (formatted display)
- ResumeDataDisplay (structured view)

**Analysis Components (components/analysis/)**
- FitAnalysisDisplay (overall view)
- MatchCard (individual match with evidence)
- MatchTypeSection (strong/partial/missing)
- ProgressBar (match percentage)

**Tailoring Components (components/tailoring/)**
- SuggestionCard (individual suggestion)
- DiffViewer (before/after comparison)
- SuggestionList (all suggestions)
- ApprovalControls (accept/reject/edit)

**Application Components (components/application/)**
- ApplicationCard (display in list)
- ApplicationList (grid of cards)
- StatusBadge (color-coded status)
- StatusUpdateButtons

**Layout Components (components/layout/)**
- Sidebar (navigation)
- TopNav (user menu)
- PageHeader (title + actions)
- EmptyState (no data placeholder)

### State Management

**Custom Hooks:**
- useResumes() - Fetch and manage resumes
- useJobDescriptions() - Fetch and manage JDs
- useApplications() - Fetch and manage applications
- useFitAnalysis() - Fetch fit analysis
- useTailoring() - Fetch and approve suggestions
- useToast() - Show notifications
- useAuth() - Authentication state

**Context Providers:**
- AuthProvider - User authentication
- ToastProvider - Global notifications



---

## Backend Services

### Service Layer

**ResumeParsingService**
- Responsibilities:
  - Extract text from uploaded files (PDF, DOCX, TXT)
  - Send text to OpenAI for parsing
  - Validate parsed data against schema
  - Store file in Supabase Storage
  - Save parsed data to database
- Dependencies: AIClient, StorageClient, ResumeRepository
- Key Methods:
  - `upload_and_parse(file: UploadFile, user_id: str) -> Resume`
  - `_extract_text(file: UploadFile) -> str`
  - `_parse_with_ai(text: str) -> dict`
  - `_validate_parsed_data(data: dict) -> ResumeData`

**JobDescriptionParsingService**
- Responsibilities:
  - Parse JD text with OpenAI
  - Extract requirements, skills, responsibilities
  - Validate parsed data
  - Save to database
- Dependencies: AIClient, JobDescriptionRepository
- Key Methods:
  - `parse_and_save(raw_text: str, user_id: str) -> JobDescription`
  - `_parse_with_ai(text: str) -> dict`
  - `_validate_parsed_data(data: dict) -> JobDescriptionData`

**FitAnalysisService**
- Responsibilities:
  - Compare resume against JD requirements
  - Categorize matches (strong, partial, missing)
  - Provide evidence for each match
  - Calculate overall score
  - Save analysis to database
- Dependencies: AIClient, FitAnalysisRepository, ResumeRepository, JDRepository
- Key Methods:
  - `analyze_fit(resume_id: str, jd_id: str, user_id: str) -> FitAnalysis`
  - `_compare_with_ai(resume: ResumeData, jd: JobDescriptionData) -> dict`
  - `_calculate_score(matches: dict) -> float`
  - `_validate_analysis(data: dict) -> FitAnalysisData`

**TailoringService**
- Responsibilities:
  - Generate tailoring suggestions based on fit analysis
  - Ensure suggestions are truthful (no fabrication)
  - Provide reasoning and evidence for each suggestion
  - Save suggestions to database
  - Track user approvals
- Dependencies: AIClient, TailoringRepository, FitAnalysisRepository
- Key Methods:
  - `generate_suggestions(fit_analysis_id: str, user_id: str) -> Tailoring`
  - `_generate_with_ai(resume: ResumeData, jd: JobDescriptionData, fit: FitAnalysisData) -> dict`
  - `_validate_suggestions(suggestions: dict, resume: ResumeData) -> TailoringSuggestions`
  - `_check_no_fabrication(suggestion: dict, resume: ResumeData) -> bool`
  - `approve_suggestions(tailoring_id: str, approved: dict, user_id: str) -> Tailoring`

**ResumeGenerationService**
- Responsibilities:
  - Apply approved suggestions to resume data
  - Generate DOCX file with python-docx
  - Format resume for ATS compatibility
  - Upload to storage
  - Save record to database
- Dependencies: StorageClient, GeneratedResumeRepository, TailoringRepository, ResumeRepository
- Key Methods:
  - `generate_resume(resume_id: str, tailoring_id: str, user_id: str) -> GeneratedResume`
  - `_apply_suggestions(resume: ResumeData, approved: dict) -> ResumeData`
  - `_generate_docx(resume: ResumeData) -> Document`
  - `_format_section(section: str, data: dict) -> None`
  - `_upload_document(doc: Document, user_id: str) -> str`

**ApplicationService**
- Responsibilities:
  - Create application records
  - Update application status
  - Link to resume, JD, and generated resume
  - Manage application lifecycle
- Dependencies: ApplicationRepository
- Key Methods:
  - `create_application(data: CreateApplicationRequest, user_id: str) -> Application`
  - `update_status(app_id: str, status: str, user_id: str) -> Application`
  - `get_applications(user_id: str, filters: dict) -> List[Application]`
  - `delete_application(app_id: str, user_id: str) -> None`

### Utility Services

**AIClient**
- Responsibilities:
  - Wrapper for OpenAI API calls
  - Handle function calling for structured outputs
  - Retry logic for transient failures
  - Token usage tracking
- Key Methods:
  - `parse_resume(text: str) -> dict`
  - `parse_job_description(text: str) -> dict`
  - `analyze_fit(resume: dict, jd: dict) -> dict`
  - `generate_tailoring(resume: dict, jd: dict, fit: dict) -> dict`
  - `_call_with_retry(messages: list, functions: list) -> dict`

**StorageClient**
- Responsibilities:
  - Upload files to Supabase Storage
  - Generate signed URLs
  - Delete files
- Key Methods:
  - `upload_file(file: UploadFile, user_id: str, folder: str) -> str`
  - `delete_file(file_url: str) -> None`
  - `get_signed_url(file_url: str, expires_in: int) -> str`

**FileExtractor**
- Responsibilities:
  - Extract text from PDF files
  - Extract text from DOCX files
  - Extract text from TXT files
- Key Methods:
  - `extract_text(file: UploadFile) -> str`
  - `_extract_from_pdf(file: bytes) -> str`
  - `_extract_from_docx(file: bytes) -> str`

### Repository Layer

**ResumeRepository**
- Methods:
  - `create(user_id: str, name: str, parsed_data: dict, file_url: str) -> Resume`
  - `get_by_id(resume_id: str) -> Resume | None`
  - `get_by_user(user_id: str) -> List[Resume]`
  - `delete(resume_id: str) -> None`

**JobDescriptionRepository**
- Methods:
  - `create(user_id: str, company: str, title: str, raw_text: str, parsed_data: dict) -> JobDescription`
  - `get_by_id(jd_id: str) -> JobDescription | None`
  - `get_by_user(user_id: str) -> List[JobDescription]`
  - `delete(jd_id: str) -> None`

**FitAnalysisRepository**
- Methods:
  - `create(user_id: str, resume_id: str, jd_id: str, analysis_data: dict, score: float) -> FitAnalysis`
  - `get_by_id(analysis_id: str) -> FitAnalysis | None`
  - `get_by_resume_and_jd(resume_id: str, jd_id: str) -> FitAnalysis | None`

**TailoringRepository**
- Methods:
  - `create(user_id: str, fit_analysis_id: str, suggestions: dict) -> Tailoring`
  - `get_by_id(tailoring_id: str) -> Tailoring | None`
  - `update_approvals(tailoring_id: str, approved: dict) -> Tailoring`

**GeneratedResumeRepository**
- Methods:
  - `create(user_id: str, resume_id: str, tailoring_id: str, file_url: str) -> GeneratedResume`
  - `get_by_id(generated_id: str) -> GeneratedResume | None`

**ApplicationRepository**
- Methods:
  - `create(user_id: str, data: dict) -> Application`
  - `get_by_id(app_id: str) -> Application | None`
  - `get_by_user(user_id: str, filters: dict) -> List[Application]`
  - `update(app_id: str, data: dict) -> Application`
  - `delete(app_id: str) -> None`



---

## Validation Rules

### File Upload Validation

**Client-Side:**
- File type: PDF, DOCX, TXT only
- File size: Max 5MB
- File not empty
- Display clear error messages

**Server-Side:**
- Verify file extension
- Verify MIME type
- Verify file size
- Scan for malicious content (basic)
- Extract text successfully

### Resume Parsing Validation

**Schema Validation (Pydantic):**
- Contact: name and email required
- Experience: company, title, bullets required
- Education: institution, degree required
- Skills: at least one category with values
- All arrays must not contain empty strings
- URLs must be valid format or null

**Business Rules:**
- At least one experience or education entry
- Contact email must be valid format
- Dates should be parseable or null
- No fabricated data (validate against source text)

### Job Description Parsing Validation

**Schema Validation:**
- Company and title required
- Requirements must have at least one technical skill
- All extracted content must have source in raw text
- Skills must be specific, not generic

**Business Rules:**
- Raw text minimum length: 100 characters
- At least 3 requirements extracted
- No assumptions about unlisted requirements

### Fit Analysis Validation

**Schema Validation:**
- Matches categorized into strong/partial/missing
- Each match has evidence array
- Overall score between 0 and 1
- Confidence levels: high, medium, low, none

**Business Rules:**
- Strong matches must have direct evidence
- Partial matches must explain the gap
- Missing requirements clearly flagged
- Evidence must reference actual resume content
- No invented connections

### Tailoring Suggestions Validation

**Schema Validation:**
- Each suggestion has type, section, reason, evidence
- Rephrase suggestions have both original and suggested text
- All suggestions have JD alignment
- Suggestion IDs are unique

**Business Rules (Critical):**
- No new skills or experiences added
- Rephrased text preserves factual accuracy
- No inflated metrics or achievements
- All suggestions map to existing resume content
- Evidence exists in original resume
- Reasoning is clear and specific

**Fabrication Detection:**
```python
def validate_no_fabrication(original_resume: ResumeData, suggestion: dict) -> bool:
    """
    Ensure suggestion doesn't add information not in original resume.
    """
    if suggestion['type'] == 'rephrase':
        original_text = suggestion['original']
        suggested_text = suggestion['suggested']
        
        # Extract key facts from both
        original_facts = extract_facts(original_text)
        suggested_facts = extract_facts(suggested_text)
        
        # Check for new facts
        new_facts = suggested_facts - original_facts
        
        if new_facts:
            # Check if new facts exist elsewhere in resume
            for fact in new_facts:
                if not fact_exists_in_resume(fact, original_resume):
                    raise ValueError(f"Fabricated content detected: {fact}")
    
    return True
```

### Resume Generation Validation

**Pre-Generation:**
- User has approved at least one suggestion
- Resume data is valid
- Tailoring suggestions are valid
- User owns all resources

**Post-Generation:**
- DOCX file created successfully
- File uploaded to storage
- File URL is accessible
- File size is reasonable (< 2MB)

### Application Creation Validation

**Schema Validation:**
- Company and title required (min 1 char)
- Applied date is valid date
- Status is valid enum value
- Notes max length: 5000 characters

**Business Rules:**
- Resume exists and user owns it
- JD exists and user owns it
- Generated resume exists (if provided)
- Applied date not in future



---

## Test Strategy

### Testing Priorities

**High Priority (Must Test):**
1. AI output validation (no fabrication)
2. Resume parsing accuracy
3. JD parsing accuracy
4. Fit analysis correctness
5. Tailoring suggestion validation
6. Resume generation correctness
7. File upload validation
8. Authentication and authorization

**Medium Priority (Should Test):**
1. API endpoint functionality
2. Database operations
3. Error handling
4. Edge cases (empty data, malformed input)

**Low Priority (Nice to Test):**
1. UI component rendering
2. User interactions
3. Performance benchmarks

### Backend Testing

**Unit Tests**

Test individual service methods:
```python
# tests/test_services/test_resume_parser.py
def test_parse_resume_success(mock_ai_client, sample_resume_text):
    service = ResumeParsingService(mock_ai_client, mock_storage, mock_repo)
    result = service._parse_with_ai(sample_resume_text)
    
    assert result['contact']['name'] == "John Doe"
    assert len(result['experience']) > 0

def test_parse_resume_validates_schema(mock_ai_client):
    service = ResumeParsingService(mock_ai_client, mock_storage, mock_repo)
    invalid_data = {"contact": {}}  # Missing required fields
    
    with pytest.raises(ValidationError):
        service._validate_parsed_data(invalid_data)

def test_parse_resume_rejects_fabrication(mock_ai_client):
    # AI returns data not in source text
    mock_ai_client.parse_resume.return_value = {
        "skills": {"languages": ["Python", "Java"]}  # Java not in source
    }
    
    service = ResumeParsingService(mock_ai_client, mock_storage, mock_repo)
    
    with pytest.raises(ValueError, match="fabrication"):
        service.upload_and_parse(file, user_id)
```

**Integration Tests**

Test API endpoints end-to-end:
```python
# tests/test_routers/test_resumes.py
def test_upload_resume_success(client, auth_headers, sample_pdf):
    response = client.post(
        "/api/resumes/upload",
        files={"file": sample_pdf},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "parsed_data" in data
    assert data['parsed_data']['contact']['name'] == "John Doe"

def test_upload_resume_invalid_format(client, auth_headers):
    response = client.post(
        "/api/resumes/upload",
        files={"file": ("test.exe", b"content", "application/exe")},
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert "Invalid file type" in response.json()['detail']
```

**AI Validation Tests**

Critical tests for fabrication detection:
```python
# tests/test_validation/test_fabrication_detection.py
def test_rejects_new_skills():
    original_resume = ResumeData(
        skills={"languages": ["Python", "JavaScript"]}
    )
    
    suggestion = {
        "type": "rephrase",
        "original": "Experience with Python",
        "suggested": "Experience with Python, JavaScript, and Java"
    }
    
    with pytest.raises(ValueError, match="fabricated"):
        validate_no_fabrication(original_resume, suggestion)

def test_accepts_valid_rephrase():
    original_resume = ResumeData(
        skills={"languages": ["Python"]}
    )
    
    suggestion = {
        "type": "rephrase",
        "original": "Built REST API with Python",
        "suggested": "Developed RESTful API using Python"
    }
    
    # Should not raise
    validate_no_fabrication(original_resume, suggestion)

def test_rejects_inflated_metrics():
    suggestion = {
        "type": "rephrase",
        "original": "Improved performance by 20%",
        "suggested": "Improved performance by 50%"
    }
    
    with pytest.raises(ValueError, match="inflated"):
        validate_rephrase(suggestion)
```

### Frontend Testing

**For MVP: Manual Testing**

Focus on manual QA for UI:
- Test all user flows end-to-end
- Test on different browsers (Chrome, Firefox, Safari)
- Test on different devices (desktop, tablet, mobile)
- Test error states
- Test loading states
- Test empty states

**Post-MVP: Automated Tests**

Consider adding:
- Component tests with React Testing Library
- E2E tests with Playwright
- Visual regression tests

### Test Coverage Goals

**Backend:**
- Services: 80%+ coverage
- Repositories: 70%+ coverage
- API endpoints: 70%+ coverage
- Utilities: 60%+ coverage
- Overall: 70%+ coverage

**Frontend:**
- Manual QA for MVP
- Automated tests post-MVP

### Test Data

**Fixtures:**
- Sample resumes (PDF, DOCX, TXT)
- Sample job descriptions
- Sample parsed data
- Sample fit analyses
- Sample tailoring suggestions

**Mock Data:**
- Mock AI responses
- Mock database records
- Mock file uploads
- Mock authentication



---

## Implementation Tasks

### Phase 1: Foundation & Setup (Week 1)

**1.1 Project Setup**
- [ ] Initialize backend repository (FastAPI)
- [ ] Initialize frontend repository (Next.js)
- [ ] Set up development environment
- [ ] Configure linting and formatting (Black, Prettier, ESLint)
- [ ] Set up Git repository and .gitignore
- [ ] Create .env.example files

**1.2 Database Setup**
- [ ] Set up Supabase project
- [ ] Configure Supabase Auth
- [ ] Create database schema (users, resumes, job_descriptions, etc.)
- [ ] Set up Alembic for migrations
- [ ] Create initial migration
- [ ] Apply migration to database
- [ ] Set up database indexes

**1.3 Infrastructure Setup**
- [ ] Configure Supabase Storage buckets
- [ ] Set up OpenAI API account
- [ ] Configure environment variables
- [ ] Set up logging infrastructure
- [ ] Create basic README files

**1.4 Authentication**
- [ ] Implement Supabase Auth in backend
- [ ] Create authentication middleware
- [ ] Implement auth endpoints (login, signup, logout)
- [ ] Implement Supabase Auth in frontend
- [ ] Create AuthProvider context
- [ ] Create login/signup pages
- [ ] Implement protected routes

**Deliverable:** Working authentication system, database schema, project structure

---

### Phase 2: Resume Upload & Parsing (Week 2)

**2.1 Backend - File Handling**
- [ ] Create FileExtractor utility
  - [ ] Implement PDF text extraction (PyPDF2 or pdfplumber)
  - [ ] Implement DOCX text extraction (python-docx)
  - [ ] Implement TXT text extraction
  - [ ] Add error handling for corrupted files
- [ ] Create StorageClient utility
  - [ ] Implement file upload to Supabase Storage
  - [ ] Implement file deletion
  - [ ] Implement signed URL generation
- [ ] Add file validation utilities
  - [ ] Validate file type
  - [ ] Validate file size
  - [ ] Validate file content

**2.2 Backend - AI Integration**
- [ ] Create AIClient utility
  - [ ] Implement OpenAI API wrapper
  - [ ] Implement function calling for structured outputs
  - [ ] Add retry logic with exponential backoff
  - [ ] Add token usage tracking
- [ ] Define resume parsing JSON schema
- [ ] Create resume parsing prompt
- [ ] Test parsing with sample resumes

**2.3 Backend - Resume Service**
- [ ] Create ResumeData Pydantic model
- [ ] Create ResumeRepository
  - [ ] Implement create method
  - [ ] Implement get_by_id method
  - [ ] Implement get_by_user method
  - [ ] Implement delete method
- [ ] Create ResumeParsingService
  - [ ] Implement upload_and_parse method
  - [ ] Implement text extraction
  - [ ] Implement AI parsing
  - [ ] Implement validation
  - [ ] Implement storage upload
  - [ ] Implement database save
- [ ] Create resume API endpoints
  - [ ] POST /api/resumes/upload
  - [ ] GET /api/resumes
  - [ ] GET /api/resumes/{id}
  - [ ] DELETE /api/resumes/{id}

**2.4 Frontend - Resume Upload**
- [ ] Create Resume types (TypeScript)
- [ ] Create API client functions
  - [ ] uploadResume()
  - [ ] getResumes()
  - [ ] getResume()
  - [ ] deleteResume()
- [ ] Create useResumes hook
- [ ] Create UI components
  - [ ] FileDropZone
  - [ ] LoadingSpinner
  - [ ] ResumeCard
- [ ] Create resume upload page
  - [ ] File selection/drop
  - [ ] Client-side validation
  - [ ] Upload progress
  - [ ] Parsing progress
  - [ ] Parsed data preview
- [ ] Create resumes list page
  - [ ] Display resume cards
  - [ ] Delete functionality
  - [ ] Empty state
- [ ] Create resume detail page

**2.5 Testing**
- [ ] Write unit tests for FileExtractor
- [ ] Write unit tests for ResumeParsingService
- [ ] Write integration tests for resume endpoints
- [ ] Write AI validation tests
- [ ] Manual testing of upload flow

**Deliverable:** Working resume upload and parsing system

---

### Phase 3: Job Description Parsing (Week 3)

**3.1 Backend - JD Service**
- [ ] Create JobDescriptionData Pydantic model
- [ ] Define JD parsing JSON schema
- [ ] Create JD parsing prompt
- [ ] Create JobDescriptionRepository
  - [ ] Implement create method
  - [ ] Implement get_by_id method
  - [ ] Implement get_by_user method
  - [ ] Implement delete method
- [ ] Create JobDescriptionParsingService
  - [ ] Implement parse_and_save method
  - [ ] Implement AI parsing
  - [ ] Implement validation
  - [ ] Implement database save
- [ ] Create JD API endpoints
  - [ ] POST /api/job-descriptions
  - [ ] GET /api/job-descriptions
  - [ ] GET /api/job-descriptions/{id}
  - [ ] DELETE /api/job-descriptions/{id}

**3.2 Frontend - JD Input**
- [ ] Create JobDescription types
- [ ] Create API client functions
  - [ ] createJobDescription()
  - [ ] getJobDescriptions()
  - [ ] getJobDescription()
  - [ ] deleteJobDescription()
- [ ] Create useJobDescriptions hook
- [ ] Create JD input component
  - [ ] Large textarea
  - [ ] Character count
  - [ ] Company/title inputs
  - [ ] Parse button
- [ ] Create JD display component
- [ ] Integrate into new application flow

**3.3 Testing**
- [ ] Write unit tests for JDParsingService
- [ ] Write integration tests for JD endpoints
- [ ] Write validation tests
- [ ] Manual testing of JD parsing

**Deliverable:** Working JD parsing system

---

### Phase 4: Fit Analysis (Week 4)

**4.1 Backend - Fit Analysis Service**
- [ ] Create FitAnalysisData Pydantic model
- [ ] Define fit analysis JSON schema
- [ ] Create fit analysis prompt
- [ ] Create FitAnalysisRepository
  - [ ] Implement create method
  - [ ] Implement get_by_id method
  - [ ] Implement get_by_resume_and_jd method
- [ ] Create FitAnalysisService
  - [ ] Implement analyze_fit method
  - [ ] Implement AI comparison
  - [ ] Implement match categorization
  - [ ] Implement score calculation
  - [ ] Implement validation
  - [ ] Implement database save
- [ ] Create fit analysis API endpoints
  - [ ] POST /api/analysis/fit
  - [ ] GET /api/analysis/fit/{id}

**4.2 Frontend - Fit Analysis Display**
- [ ] Create FitAnalysis types
- [ ] Create API client functions
  - [ ] createFitAnalysis()
  - [ ] getFitAnalysis()
- [ ] Create useFitAnalysis hook
- [ ] Create fit analysis components
  - [ ] OverallMatchScore (progress bar)
  - [ ] MatchCard (individual match)
  - [ ] MatchTypeSection (strong/partial/missing)
  - [ ] FitAnalysisDisplay (overall view)
- [ ] Integrate into new application flow
- [ ] Add loading and error states

**4.3 Testing**
- [ ] Write unit tests for FitAnalysisService
- [ ] Write integration tests for fit analysis endpoints
- [ ] Write validation tests (evidence mapping)
- [ ] Test match categorization logic
- [ ] Manual testing of fit analysis

**Deliverable:** Working fit analysis system

---

### Phase 5: Tailoring Suggestions (Week 5)

**5.1 Backend - Tailoring Service**
- [ ] Create TailoringSuggestions Pydantic model
- [ ] Define tailoring JSON schema
- [ ] Create tailoring prompt (with strict no-fabrication rules)
- [ ] Create TailoringRepository
  - [ ] Implement create method
  - [ ] Implement get_by_id method
  - [ ] Implement update_approvals method
- [ ] Create TailoringService
  - [ ] Implement generate_suggestions method
  - [ ] Implement AI generation
  - [ ] Implement validation
  - [ ] Implement fabrication detection
  - [ ] Implement database save
  - [ ] Implement approve_suggestions method
- [ ] Create tailoring API endpoints
  - [ ] POST /api/analysis/tailoring
  - [ ] GET /api/analysis/tailoring/{id}
  - [ ] PATCH /api/analysis/tailoring/{id}/approve

**5.2 Frontend - Tailoring Review**
- [ ] Create Tailoring types
- [ ] Create API client functions
  - [ ] createTailoring()
  - [ ] getTailoring()
  - [ ] approveSuggestions()
- [ ] Create useTailoring hook
- [ ] Create tailoring components
  - [ ] SuggestionCard (individual suggestion)
  - [ ] DiffViewer (before/after comparison)
  - [ ] ApprovalControls (accept/reject/edit)
  - [ ] SuggestionList (all suggestions)
- [ ] Integrate into new application flow
- [ ] Implement approval tracking
- [ ] Add bulk actions (accept all, reject all)

**5.3 Testing**
- [ ] Write unit tests for TailoringService
- [ ] Write fabrication detection tests (critical!)
- [ ] Write integration tests for tailoring endpoints
- [ ] Test approval flow
- [ ] Manual testing of suggestions

**Deliverable:** Working tailoring suggestion system with fabrication prevention

---

### Phase 6: Resume Generation (Week 6)

**6.1 Backend - Resume Generation Service**
- [ ] Create GeneratedResume Pydantic model
- [ ] Create GeneratedResumeRepository
  - [ ] Implement create method
  - [ ] Implement get_by_id method
- [ ] Create ResumeGenerationService
  - [ ] Implement generate_resume method
  - [ ] Implement apply_suggestions logic
  - [ ] Implement DOCX generation with python-docx
    - [ ] Format contact section
    - [ ] Format summary section
    - [ ] Format experience section
    - [ ] Format education section
    - [ ] Format skills section
    - [ ] Format projects section
    - [ ] Format certifications section
  - [ ] Implement ATS-friendly formatting
  - [ ] Implement file upload to storage
  - [ ] Implement database save
- [ ] Create generation API endpoints
  - [ ] POST /api/generate/resume
  - [ ] GET /api/generate/resume/{id}

**6.2 Frontend - Resume Generation**
- [ ] Create GeneratedResume types
- [ ] Create API client functions
  - [ ] generateResume()
  - [ ] getGeneratedResume()
- [ ] Create preview component
  - [ ] Display formatted resume
  - [ ] Highlight applied changes
  - [ ] Show changes summary
- [ ] Create success page
  - [ ] Success message
  - [ ] Download button
  - [ ] Save to applications CTA
- [ ] Integrate into new application flow

**6.3 Testing**
- [ ] Write unit tests for ResumeGenerationService
- [ ] Test suggestion application logic
- [ ] Test DOCX generation
- [ ] Test formatting consistency
- [ ] Manual testing of generated resumes
- [ ] Verify ATS compatibility

**Deliverable:** Working resume generation and download

---

### Phase 7: Application Tracking (Week 7)

**7.1 Backend - Application Service**
- [ ] Create Application Pydantic model
- [ ] Create ApplicationRepository
  - [ ] Implement create method
  - [ ] Implement get_by_id method
  - [ ] Implement get_by_user method
  - [ ] Implement update method
  - [ ] Implement delete method
- [ ] Create ApplicationService
  - [ ] Implement create_application method
  - [ ] Implement update_status method
  - [ ] Implement get_applications method (with filters)
  - [ ] Implement delete_application method
- [ ] Create application API endpoints
  - [ ] POST /api/applications
  - [ ] GET /api/applications
  - [ ] GET /api/applications/{id}
  - [ ] PATCH /api/applications/{id}
  - [ ] DELETE /api/applications/{id}

**7.2 Frontend - Application Tracking**
- [ ] Create Application types
- [ ] Create API client functions
  - [ ] createApplication()
  - [ ] getApplications()
  - [ ] getApplication()
  - [ ] updateApplication()
  - [ ] deleteApplication()
- [ ] Create useApplications hook
- [ ] Create application components
  - [ ] ApplicationCard
  - [ ] ApplicationList
  - [ ] StatusBadge
  - [ ] StatusUpdateButtons
- [ ] Create applications list page
  - [ ] Display application cards
  - [ ] Filter by status
  - [ ] Sort options
  - [ ] Empty state
- [ ] Create application detail page
  - [ ] Display all details
  - [ ] Link to resume, JD, generated resume
  - [ ] Status update
  - [ ] Notes editing
  - [ ] Delete functionality
- [ ] Integrate application creation into flow

**7.3 Testing**
- [ ] Write unit tests for ApplicationService
- [ ] Write integration tests for application endpoints
- [ ] Test filtering and sorting
- [ ] Manual testing of application tracking

**Deliverable:** Working application tracking system

---

### Phase 8: Dashboard & Polish (Week 8)

**8.1 Dashboard**
- [ ] Create dashboard page
  - [ ] Quick action cards
  - [ ] Recent applications (5 most recent)
  - [ ] Resume library preview (3 most recent)
  - [ ] Stats overview (optional)
- [ ] Implement navigation
  - [ ] Sidebar with all routes
  - [ ] Active route highlighting
  - [ ] Mobile responsive menu

**8.2 Error Handling & UX Polish**
- [ ] Implement global error boundary
- [ ] Add error messages for all failure cases
- [ ] Add loading states for all async operations
- [ ] Add empty states for all lists
- [ ] Add confirmation modals for destructive actions
- [ ] Add toast notifications for success/error
- [ ] Improve form validation messages
- [ ] Add keyboard shortcuts (optional)

**8.3 Responsive Design**
- [ ] Test on mobile devices
- [ ] Test on tablets
- [ ] Fix responsive issues
- [ ] Optimize touch targets
- [ ] Test on different browsers

**8.4 Accessibility**
- [ ] Add ARIA labels
- [ ] Test keyboard navigation
- [ ] Test with screen reader
- [ ] Fix contrast issues
- [ ] Add focus indicators

**8.5 Documentation**
- [ ] Update README files
- [ ] Document API endpoints
- [ ] Document environment variables
- [ ] Create deployment guide
- [ ] Create user guide (optional)

**8.6 Final Testing**
- [ ] End-to-end testing of full flow
- [ ] Test all error scenarios
- [ ] Test edge cases
- [ ] Performance testing
- [ ] Security review
- [ ] Code review

**8.7 Deployment Preparation**
- [ ] Set up production database
- [ ] Configure production environment variables
- [ ] Set up CI/CD (optional)
- [ ] Deploy backend to Railway/Render
- [ ] Deploy frontend to Vercel
- [ ] Test production deployment
- [ ] Monitor for errors

**Deliverable:** Fully functional MVP ready for users

---

## Timeline Summary

- **Week 1:** Foundation & Setup
- **Week 2:** Resume Upload & Parsing
- **Week 3:** Job Description Parsing
- **Week 4:** Fit Analysis
- **Week 5:** Tailoring Suggestions
- **Week 6:** Resume Generation
- **Week 7:** Application Tracking
- **Week 8:** Dashboard & Polish

**Total:** 6-8 weeks (solo developer, full-time)

---

## Success Metrics

**Technical Metrics:**
- Resume parsing success rate > 90%
- JD parsing extracts all key requirements
- Fit analysis accuracy validated manually
- Zero fabrication incidents in tailoring
- Generated resumes are ATS-compatible
- Test coverage > 70%
- API response times < 3 seconds

**User Metrics:**
- User can complete full flow in < 5 minutes
- Clear error messages for all failures
- No blocking bugs
- Responsive on all devices
- Accessible (WCAG AA)

**Business Metrics:**
- MVP deployed and functional
- Ready for user testing
- Foundation for post-MVP features

---

## Post-MVP Roadmap

**Phase 9: Cover Letter Generation**
- Implement cover letter service
- Add cover letter UI
- Integrate into application flow

**Phase 10: Interview Prep**
- Generate technical questions
- Generate behavioral questions
- Create STAR examples
- Add interview prep page

**Phase 11: Advanced Features**
- Recruiter outreach drafts
- Skill gap analysis
- Multiple resume versions
- PDF export
- Resume editing UI

---

**End of Specification**

