---
inclusion: auto
---

# AI Job Application Copilot - Technical Steering Document

## Architecture Overview

### Stack

**Frontend**
- Framework: Next.js (React)
- Language: TypeScript
- Styling: Tailwind CSS (recommended) or CSS Modules
- State Management: React Context or Zustand (keep simple)

**Backend**
- Framework: FastAPI (Python)
- Language: Python 3.11+
- API Style: RESTful with typed request/response models

**Database**
- Primary: Supabase Postgres
- ORM: SQLAlchemy or Supabase client
- Migrations: Alembic

**Storage**
- File Storage: Supabase Storage
- Store: Uploaded resumes, generated documents

**AI Layer**
- Provider: OpenAI API
- Models: GPT-4 or GPT-3.5-turbo
- Output Format: Structured JSON with function calling

**Document Generation**
- Library: python-docx (DOCX generation)
- PDF Export: Future enhancement (reportlab or weasyprint)


## Core Technical Principles

### 1. Modularity
- Separate concerns: parsing, analysis, generation, storage
- Each module should have a single, well-defined responsibility
- Modules communicate through clear interfaces
- Easy to test, replace, or extend individual components

### 2. Clear Service Boundaries
- Frontend handles UI/UX and user interactions only
- Backend handles business logic, AI orchestration, data persistence
- AI layer is abstracted behind service interfaces
- Storage operations isolated in repository pattern

### 3. Type Safety
- Use Pydantic models for all API request/response
- Use TypeScript interfaces for frontend data structures
- Validate data at service boundaries
- No implicit type conversions

### 4. Structured AI Outputs
- Always use OpenAI function calling for structured responses
- Define JSON schemas for all AI outputs
- Validate AI responses against schemas before use
- Never parse freeform text when structured output is possible

### 5. Separation of Concerns
- Orchestration logic: Coordinates between services
- Business logic: Domain rules and validations
- Data access: Repository pattern for database operations
- Keep these layers distinct and testable

### 6. Frontend-Backend Decoupling
- Backend exposes RESTful API only
- Frontend consumes API as external service
- No shared code between frontend and backend (except API types)
- Version API endpoints for future compatibility

### 7. Cost Optimization
- Cache AI responses where appropriate
- Use cheaper models for simple tasks
- Batch operations when possible
- Minimize token usage with focused prompts
- Store parsed data to avoid re-parsing

### 8. Solo Developer Maintainability
- Keep architecture simple and conventional
- Minimize dependencies
- Prefer boring, proven technologies
- Write self-documenting code
- Automate repetitive tasks
- Use clear naming conventions


## Data Models

### Resume Data Structure (JSON)

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Software Engineer Resume v1",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "parsed_data": {
    "contact": {
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "linkedin": "string",
      "github": "string",
      "portfolio": "string"
    },
    "summary": "string",
    "education": [
      {
        "institution": "string",
        "degree": "string",
        "field": "string",
        "start_date": "string",
        "end_date": "string",
        "gpa": "string",
        "achievements": ["string"]
      }
    ],
    "experience": [
      {
        "company": "string",
        "title": "string",
        "start_date": "string",
        "end_date": "string",
        "location": "string",
        "bullets": ["string"]
      }
    ],
    "projects": [
      {
        "name": "string",
        "description": "string",
        "technologies": ["string"],
        "bullets": ["string"],
        "url": "string"
      }
    ],
    "skills": {
      "languages": ["string"],
      "frameworks": ["string"],
      "tools": ["string"],
      "other": ["string"]
    },
    "certifications": [
      {
        "name": "string",
        "issuer": "string",
        "date": "string"
      }
    ]
  },
  "original_file_url": "string"
}
```


### Job Description Data Structure (JSON)

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "company": "string",
  "title": "string",
  "created_at": "timestamp",
  "raw_text": "string",
  "parsed_data": {
    "company": "string",
    "title": "string",
    "location": "string",
    "job_type": "string",
    "salary_range": "string",
    "requirements": {
      "technical_skills": [
        {
          "skill": "string",
          "required": true,
          "years": "number"
        }
      ],
      "soft_skills": ["string"],
      "education": ["string"],
      "experience_years": "number",
      "certifications": ["string"]
    },
    "responsibilities": ["string"],
    "nice_to_have": ["string"],
    "keywords": ["string"]
  }
}
```

### Fit Analysis Data Structure (JSON)

```json
{
  "id": "uuid",
  "resume_id": "uuid",
  "job_description_id": "uuid",
  "created_at": "timestamp",
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
        "gap": "No specific AWS experience mentioned"
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


### Tailoring Suggestions Data Structure (JSON)

```json
{
  "id": "uuid",
  "fit_analysis_id": "uuid",
  "created_at": "timestamp",
  "suggestions": [
    {
      "type": "reorder",
      "section": "experience",
      "item_id": "string",
      "current_position": 2,
      "suggested_position": 1,
      "reason": "Most relevant to JD requirements"
    },
    {
      "type": "rephrase",
      "section": "experience",
      "item_id": "string",
      "bullet_index": 0,
      "original": "Built web application",
      "suggested": "Developed full-stack web application using React and Node.js",
      "reason": "Emphasize technologies mentioned in JD"
    },
    {
      "type": "emphasize",
      "section": "projects",
      "item_id": "string",
      "reason": "Directly relevant to role requirements"
    }
  ],
  "user_approved": false
}
```


## Service Architecture

### Backend Services

**ResumeParsingService**
- Responsibility: Extract structured data from uploaded resume files
- Input: File (PDF, DOCX, TXT)
- Output: Structured resume JSON
- Dependencies: OpenAI API, file storage

**JobDescriptionParsingService**
- Responsibility: Extract structured requirements from JD text
- Input: Raw JD text
- Output: Structured JD JSON
- Dependencies: OpenAI API

**FitAnalysisService**
- Responsibility: Compare resume against JD requirements
- Input: Resume JSON, JD JSON
- Output: Fit analysis JSON with matches/gaps
- Dependencies: OpenAI API

**TailoringService**
- Responsibility: Generate resume modification suggestions
- Input: Resume JSON, JD JSON, Fit analysis JSON
- Output: Tailoring suggestions JSON
- Dependencies: OpenAI API

**ResumeGenerationService**
- Responsibility: Generate DOCX from resume JSON and approved suggestions
- Input: Resume JSON, approved suggestions
- Output: DOCX file
- Dependencies: python-docx, file storage

**CoverLetterService**
- Responsibility: Generate cover letter content
- Input: Resume JSON, JD JSON
- Output: Cover letter text
- Dependencies: OpenAI API

**ApplicationTrackingService**
- Responsibility: CRUD operations for application records
- Input: Application data
- Output: Application records
- Dependencies: Database


### API Endpoints (Backend)

**Resumes**
- `POST /api/resumes/upload` - Upload and parse resume
- `GET /api/resumes` - List user's resumes
- `GET /api/resumes/{id}` - Get resume details
- `DELETE /api/resumes/{id}` - Delete resume

**Job Descriptions**
- `POST /api/job-descriptions` - Parse and save JD
- `GET /api/job-descriptions` - List user's JDs
- `GET /api/job-descriptions/{id}` - Get JD details
- `DELETE /api/job-descriptions/{id}` - Delete JD

**Analysis**
- `POST /api/analysis/fit` - Analyze resume-JD fit
- `GET /api/analysis/fit/{id}` - Get fit analysis
- `POST /api/analysis/tailoring` - Generate tailoring suggestions
- `GET /api/analysis/tailoring/{id}` - Get tailoring suggestions

**Generation**
- `POST /api/generate/resume` - Generate tailored resume DOCX
- `POST /api/generate/cover-letter` - Generate cover letter
- `POST /api/generate/outreach` - Generate recruiter outreach

**Applications**
- `POST /api/applications` - Create application record
- `GET /api/applications` - List applications
- `GET /api/applications/{id}` - Get application details
- `PATCH /api/applications/{id}` - Update application status
- `DELETE /api/applications/{id}` - Delete application

**Interview Prep**
- `POST /api/interview-prep` - Generate interview prep materials
- `GET /api/interview-prep/{application_id}` - Get prep materials


## AI Integration Guidelines

### OpenAI Function Calling

Always use structured outputs via function calling:

```python
# Example: Resume parsing
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a resume parser..."},
        {"role": "user", "content": resume_text}
    ],
    functions=[{
        "name": "parse_resume",
        "description": "Extract structured data from resume",
        "parameters": {
            "type": "object",
            "properties": {
                "contact": {"type": "object", "properties": {...}},
                "experience": {"type": "array", "items": {...}},
                # ... full schema
            },
            "required": ["contact", "experience", "skills"]
        }
    }],
    function_call={"name": "parse_resume"}
)
```

### Prompt Engineering Principles

1. Be specific about constraints (no fabrication)
2. Provide examples in system prompts
3. Request structured outputs explicitly
4. Include validation criteria in prompts
5. Keep prompts focused on single tasks

### AI Output Validation

```python
from pydantic import BaseModel, ValidationError

class ResumeData(BaseModel):
    contact: ContactInfo
    experience: List[Experience]
    # ... fields

def validate_ai_output(raw_output: dict) -> ResumeData:
    try:
        return ResumeData(**raw_output)
    except ValidationError as e:
        # Log error, retry, or return error to user
        raise ValueError(f"Invalid AI output: {e}")
```

### Cost Optimization Strategies

1. Use GPT-3.5-turbo for simple parsing tasks
2. Use GPT-4 for complex analysis and generation
3. Cache parsed resumes and JDs (don't re-parse)
4. Limit token usage with focused prompts
5. Batch similar requests when possible
6. Set max_tokens appropriately for each task


## Database Schema

### Tables

**users**
- id: UUID (PK)
- email: VARCHAR
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

**resumes**
- id: UUID (PK)
- user_id: UUID (FK)
- name: VARCHAR
- parsed_data: JSONB
- original_file_url: VARCHAR
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

**job_descriptions**
- id: UUID (PK)
- user_id: UUID (FK)
- company: VARCHAR
- title: VARCHAR
- raw_text: TEXT
- parsed_data: JSONB
- created_at: TIMESTAMP

**fit_analyses**
- id: UUID (PK)
- resume_id: UUID (FK)
- job_description_id: UUID (FK)
- analysis_data: JSONB
- overall_score: DECIMAL
- created_at: TIMESTAMP

**tailoring_suggestions**
- id: UUID (PK)
- fit_analysis_id: UUID (FK)
- suggestions: JSONB
- user_approved: BOOLEAN
- created_at: TIMESTAMP

**applications**
- id: UUID (PK)
- user_id: UUID (FK)
- resume_id: UUID (FK)
- job_description_id: UUID (FK)
- company: VARCHAR
- title: VARCHAR
- status: VARCHAR (applied, interviewing, rejected, offer)
- applied_date: DATE
- notes: TEXT
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

**generated_documents**
- id: UUID (PK)
- application_id: UUID (FK)
- document_type: VARCHAR (resume, cover_letter, outreach)
- file_url: VARCHAR
- created_at: TIMESTAMP

### Indexes

- resumes(user_id)
- job_descriptions(user_id)
- applications(user_id, status)
- fit_analyses(resume_id, job_description_id)


## Frontend Architecture

### Directory Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── (auth)/            # Auth routes
│   ├── dashboard/         # Main app routes
│   ├── resumes/
│   ├── applications/
│   └── layout.tsx
├── components/
│   ├── ui/                # Reusable UI components
│   ├── resume/            # Resume-specific components
│   ├── analysis/          # Analysis display components
│   └── forms/             # Form components
├── lib/
│   ├── api/               # API client functions
│   ├── types/             # TypeScript types
│   ├── utils/             # Utility functions
│   └── hooks/             # Custom React hooks
└── public/
```

### State Management

Keep it simple:
- Server state: React Query or SWR
- UI state: React useState/useReducer
- Global state (if needed): React Context or Zustand

### API Client Pattern

```typescript
// lib/api/resumes.ts
export async function uploadResume(file: File): Promise<Resume> {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('/api/resumes/upload', {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    throw new Error('Upload failed');
  }
  
  return response.json();
}
```

### Component Patterns

- Use server components by default (Next.js 13+)
- Use client components only when needed (interactivity, hooks)
- Keep components small and focused
- Extract reusable logic into custom hooks
- Use composition over prop drilling


## Document Generation

### Resume Generation with python-docx

```python
from docx import Document
from docx.shared import Pt, Inches

def generate_resume_docx(resume_data: dict, suggestions: dict) -> Document:
    doc = Document()
    
    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Apply tailoring suggestions to resume_data
    tailored_data = apply_suggestions(resume_data, suggestions)
    
    # Generate sections deterministically
    add_contact_section(doc, tailored_data['contact'])
    add_summary_section(doc, tailored_data.get('summary'))
    add_experience_section(doc, tailored_data['experience'])
    add_education_section(doc, tailored_data['education'])
    add_skills_section(doc, tailored_data['skills'])
    
    return doc
```

### Formatting Guidelines

- Use consistent fonts (Calibri, Arial, or Times New Roman)
- Font sizes: Name (16-18pt), Headings (12pt), Body (11pt)
- Single line spacing within sections, 1.15 between sections
- Use bullet points for experience/project items
- Keep formatting simple and ATS-friendly
- No tables, text boxes, or complex layouts

### Deterministic Output

- Always generate sections in the same order
- Use consistent formatting rules
- Don't randomize content or structure
- Make generation reproducible for testing


## Error Handling

### Backend Error Responses

Use consistent error response format:

```python
from fastapi import HTTPException
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    detail: str
    code: str

# Usage
raise HTTPException(
    status_code=400,
    detail={
        "error": "Invalid resume format",
        "detail": "Unable to extract text from uploaded file",
        "code": "PARSE_ERROR"
    }
)
```

### Error Categories

- `PARSE_ERROR`: Resume or JD parsing failed
- `VALIDATION_ERROR`: Invalid input data
- `AI_ERROR`: OpenAI API error
- `STORAGE_ERROR`: File storage operation failed
- `NOT_FOUND`: Resource not found
- `UNAUTHORIZED`: Authentication/authorization failed

### Frontend Error Handling

```typescript
try {
  const resume = await uploadResume(file);
} catch (error) {
  if (error.code === 'PARSE_ERROR') {
    showToast('Unable to parse resume. Please try a different format.');
  } else {
    showToast('Upload failed. Please try again.');
  }
}
```


## Testing Strategy

### Backend Testing

**Unit Tests**
- Test individual service methods
- Mock external dependencies (OpenAI, database, storage)
- Test validation logic thoroughly
- Use pytest

```python
def test_resume_parsing_service():
    service = ResumeParsingService(mock_openai_client)
    result = service.parse_resume(sample_resume_text)
    assert result.contact.email == "test@example.com"
    assert len(result.experience) > 0
```

**Integration Tests**
- Test API endpoints end-to-end
- Use test database
- Test error scenarios
- Use pytest with TestClient

**AI Output Validation Tests**
- Test that AI outputs match expected schemas
- Test validation logic catches malformed outputs
- Use recorded AI responses for consistency

### Frontend Testing

**Component Tests**
- Test UI components in isolation
- Use React Testing Library
- Test user interactions
- Mock API calls

**E2E Tests (Optional for MVP)**
- Test critical user flows
- Use Playwright or Cypress
- Keep minimal for solo developer

### Testing Priorities for MVP

1. AI output validation (critical)
2. Resume parsing accuracy
3. API endpoint functionality
4. Document generation correctness
5. Frontend component rendering


## Security Considerations

### Authentication & Authorization

- Use Supabase Auth for user authentication
- Implement row-level security (RLS) in Postgres
- Verify user ownership before operations
- Use JWT tokens for API authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # Verify JWT with Supabase
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
```

### Data Privacy

- Store files in user-specific storage buckets
- Never log sensitive resume content
- Implement data deletion on user request
- Don't share data with third parties

### API Security

- Rate limiting on expensive endpoints (AI calls)
- Input validation on all endpoints
- CORS configuration for frontend domain only
- HTTPS only in production

### OpenAI API Key Management

- Store API key in environment variables
- Never expose in frontend code
- Rotate keys periodically
- Monitor usage for anomalies


## Deployment

### Environment Setup

**Development**
- Local Postgres or Supabase local development
- Local file storage or Supabase Storage
- Environment variables in `.env.local`

**Production**
- Frontend: Vercel (recommended for Next.js)
- Backend: Railway, Render, or Fly.io
- Database: Supabase Postgres
- Storage: Supabase Storage

### Environment Variables

**Backend (.env)**
```
DATABASE_URL=postgresql://...
SUPABASE_URL=https://...
SUPABASE_KEY=...
OPENAI_API_KEY=sk-...
STORAGE_BUCKET=resumes
CORS_ORIGINS=https://yourapp.com
```

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=https://api.yourapp.com
NEXT_PUBLIC_SUPABASE_URL=https://...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

### Deployment Checklist

- [ ] Set all environment variables
- [ ] Run database migrations
- [ ] Configure CORS for production domain
- [ ] Set up Supabase RLS policies
- [ ] Configure file storage buckets
- [ ] Test OpenAI API connectivity
- [ ] Set up error monitoring (Sentry optional)
- [ ] Configure rate limiting
- [ ] Test end-to-end user flow


## MVP Scope

### Phase 1: Core Resume Workflow (MVP)

**Must Have**
- User authentication (Supabase Auth)
- Resume upload and parsing (PDF, DOCX)
- Store parsed resume as JSON
- Job description input and parsing
- Store parsed JD as JSON
- Fit analysis (strong/partial/missing matches)
- Display fit analysis results
- Generate tailoring suggestions
- Show diff preview of changes
- User approval flow
- Generate tailored resume DOCX
- Download tailored resume

**Nice to Have (Post-MVP)**
- Cover letter generation
- Application tracking
- Interview prep generation
- Recruiter outreach drafts
- Skill gap analysis
- PDF export
- Multiple resume versions
- Resume editing UI

### Technical Debt to Avoid

- Don't over-engineer abstractions
- Don't add features speculatively
- Don't optimize prematurely
- Don't build custom auth
- Don't build custom file parsing (use AI)
- Don't build complex state management initially

### MVP Success Criteria

- User can upload resume and get structured data
- User can paste JD and get structured requirements
- User can see fit analysis with clear matches/gaps
- User can review and approve tailoring suggestions
- User can download tailored resume DOCX
- End-to-end flow takes < 2 minutes
- Generated resume is ATS-friendly and accurate


## Development Workflow

### Local Development Setup

1. Clone repository
2. Install dependencies:
   - Backend: `pip install -r requirements.txt`
   - Frontend: `npm install`
3. Set up environment variables
4. Run database migrations: `alembic upgrade head`
5. Start backend: `uvicorn main:app --reload`
6. Start frontend: `npm run dev`

### Code Organization

**Backend Structure**
```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── repositories/        # Data access
│   ├── routers/             # API routes
│   └── utils/               # Utilities
├── tests/
├── alembic/                 # Migrations
└── requirements.txt
```

### Git Workflow

- Main branch: `main` (production-ready)
- Feature branches: `feature/resume-parsing`
- Keep commits focused and atomic
- Write descriptive commit messages
- Squash before merging to main

### Code Style

**Python**
- Use Black for formatting
- Use Flake8 for linting
- Type hints on all functions
- Docstrings for public APIs

**TypeScript**
- Use Prettier for formatting
- Use ESLint for linting
- Strict TypeScript mode
- Explicit return types on functions


## Performance Optimization

### Backend Performance

**Database**
- Index frequently queried columns
- Use JSONB for structured data (faster than JSON)
- Limit query results with pagination
- Use connection pooling

**AI Calls**
- Cache parsed resumes (don't re-parse on every request)
- Cache parsed JDs
- Use streaming for long responses (future)
- Implement request queuing for rate limiting

**File Operations**
- Stream large files instead of loading into memory
- Use async file operations
- Set reasonable file size limits (5MB for resumes)

### Frontend Performance

**Next.js Optimization**
- Use server components by default
- Implement proper loading states
- Use Next.js Image component
- Enable static generation where possible

**API Calls**
- Implement request caching (SWR/React Query)
- Show optimistic updates where appropriate
- Debounce user input
- Implement proper loading states

### Monitoring

**Key Metrics to Track**
- API response times
- OpenAI API latency and costs
- Database query performance
- File upload success rate
- Error rates by endpoint

**Tools (Optional for MVP)**
- Vercel Analytics (frontend)
- FastAPI built-in metrics
- Supabase dashboard
- OpenAI usage dashboard


## Dependencies

### Backend Core Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.12.1
python-docx==1.1.0
openai==1.3.0
supabase==2.0.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
```

### Frontend Core Dependencies

```json
{
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@supabase/supabase-js": "^2.38.0",
    "typescript": "5.2.0"
  }
}
```

### Dependency Management

- Pin major versions to avoid breaking changes
- Review dependencies before adding new ones
- Keep dependencies minimal
- Update regularly but test thoroughly
- Use virtual environments (Python) and package-lock (Node)


## Implementation Guidelines

### Resume Parsing Implementation

1. Extract text from uploaded file (PDF/DOCX)
2. Send to OpenAI with structured schema
3. Validate response against Pydantic model
4. Store parsed JSON in database
5. Store original file in Supabase Storage
6. Return parsed data to frontend

### JD Parsing Implementation

1. Receive raw JD text from frontend
2. Send to OpenAI with requirements extraction schema
3. Validate response
4. Store parsed JSON in database
5. Return structured requirements to frontend

### Fit Analysis Implementation

1. Retrieve resume JSON and JD JSON
2. Send both to OpenAI with analysis instructions
3. Request categorized matches (strong/partial/missing)
4. Validate response structure
5. Calculate overall score
6. Store analysis results
7. Return to frontend for display

### Tailoring Suggestions Implementation

1. Retrieve resume, JD, and fit analysis
2. Send to OpenAI with tailoring instructions
3. Request specific suggestion types (reorder, rephrase, emphasize)
4. Validate each suggestion
5. Store suggestions with approval status = false
6. Return to frontend for user review

### Resume Generation Implementation

1. Retrieve original resume JSON
2. Retrieve approved tailoring suggestions
3. Apply suggestions to resume data (deterministic)
4. Generate DOCX using python-docx
5. Upload to Supabase Storage
6. Return download URL to frontend

### User Approval Flow

1. Display suggestions with diff preview
2. Allow individual accept/reject
3. Show final preview of all accepted changes
4. Require explicit "Generate Resume" action
5. Only then trigger document generation


## Common Pitfalls to Avoid

### Architecture Pitfalls

- **Don't mix concerns**: Keep parsing, analysis, and generation separate
- **Don't skip validation**: Always validate AI outputs
- **Don't couple frontend and backend**: Use API contracts only
- **Don't over-abstract**: Start simple, refactor when needed
- **Don't ignore errors**: Handle AI failures gracefully

### AI Integration Pitfalls

- **Don't trust raw AI output**: Always validate structure
- **Don't use freeform text parsing**: Use function calling
- **Don't ignore token limits**: Monitor and optimize prompts
- **Don't retry indefinitely**: Set retry limits for AI calls
- **Don't forget cost tracking**: Monitor OpenAI usage

### Data Pitfalls

- **Don't store unstructured data**: Parse and structure everything
- **Don't lose original files**: Keep originals in storage
- **Don't skip migrations**: Use Alembic for schema changes
- **Don't ignore data privacy**: Implement proper access controls
- **Don't forget backups**: Use Supabase backup features

### UX Pitfalls

- **Don't auto-apply changes**: Always require user approval
- **Don't hide AI reasoning**: Show why suggestions were made
- **Don't skip loading states**: AI calls take time
- **Don't ignore errors**: Show clear error messages
- **Don't overwhelm users**: Progressive disclosure of features

### Development Pitfalls

- **Don't skip types**: Use Pydantic and TypeScript strictly
- **Don't skip tests**: Test AI validation thoroughly
- **Don't commit secrets**: Use environment variables
- **Don't ignore performance**: Monitor slow endpoints
- **Don't build everything at once**: Focus on MVP first


## Future Technical Enhancements

### Post-MVP Features

**PDF Export**
- Add reportlab or weasyprint
- Convert DOCX to PDF
- Maintain formatting consistency

**Resume Editing UI**
- In-app resume editor
- Real-time preview
- Drag-and-drop reordering

**Advanced AI Features**
- Multi-resume comparison
- Skill trend analysis
- Industry-specific tailoring
- Tone adjustment (formal/casual)

**Performance Improvements**
- Background job processing (Celery)
- Redis caching layer
- CDN for static assets
- Database query optimization

**Integration Possibilities**
- LinkedIn profile import
- Job board APIs (Indeed, LinkedIn)
- Calendar integration
- Email integration for outreach

### Scalability Considerations

**When to Scale**
- 1000+ users: Add caching layer
- 10000+ users: Consider microservices
- High AI costs: Implement request queuing
- Slow queries: Add read replicas

**Architecture Evolution**
- Start monolithic (MVP)
- Extract services as needed
- Add message queue for async tasks
- Implement proper observability


## Quick Reference

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend Framework | Next.js | React with SSR, great DX, Vercel deployment |
| Backend Framework | FastAPI | Fast, typed, async, great for AI integration |
| Database | Supabase Postgres | Managed, RLS, auth included, cost-effective |
| File Storage | Supabase Storage | Integrated with database, simple API |
| AI Provider | OpenAI | Best structured outputs, reliable |
| Document Generation | python-docx | Simple, deterministic, DOCX support |
| Auth | Supabase Auth | Integrated, secure, minimal setup |

### Development Commands

**Backend**
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/
```

**Frontend**
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run linter
npm run lint
```

### Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [python-docx Documentation](https://python-docx.readthedocs.io/)

---

**Document Version:** 1.0  
**Last Updated:** April 1, 2026  
**Maintained By:** Engineering Team
