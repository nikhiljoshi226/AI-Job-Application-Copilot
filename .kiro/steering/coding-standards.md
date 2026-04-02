---
inclusion: auto
---

# AI Job Application Copilot - Coding Standards Document

## Philosophy

Code should be clean, maintainable, and easy to understand for a solo developer. Prioritize readability and simplicity over clever abstractions. Write code that you'll understand when you return to it in 6 months.

### Core Principles

1. **Clarity Over Cleverness** - Explicit is better than implicit
2. **Simplicity Over Abstraction** - Don't over-engineer for the MVP
3. **Consistency Over Preference** - Follow established patterns
4. **Maintainability Over Performance** - Optimize only when needed
5. **Safety Over Speed** - Validate inputs, handle errors

## Project Structure

### Backend Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration and settings
│   ├── dependencies.py         # Shared dependencies
│   │
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── resume.py           # Resume request/response models
│   │   ├── job_description.py  # JD models
│   │   ├── analysis.py         # Analysis models
│   │   └── application.py      # Application models
│   │
│   ├── schemas/                # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── resume.py
│   │   ├── job_description.py
│   │   └── application.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── resume_parser.py
│   │   ├── jd_parser.py
│   │   ├── fit_analysis.py
│   │   ├── tailoring.py
│   │   ├── resume_generator.py
│   │   └── cover_letter.py
│   │
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   ├── resume_repository.py
│   │   ├── jd_repository.py
│   │   └── application_repository.py
│   │
│   ├── routers/                # API routes
│   │   ├── __init__.py
│   │   ├── resumes.py
│   │   ├── job_descriptions.py
│   │   ├── analysis.py
│   │   ├── generation.py
│   │   └── applications.py
│   │
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── validation.py
│       ├── file_handler.py
│       ├── ai_client.py
│       └── logger.py
│
├── tests/
│   ├── __init__.py
│   ├── test_services/
│   ├── test_routers/
│   └── test_utils/
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── requirements.txt
├── .env.example
└── README.md
```


### Frontend Structure

```
frontend/
├── app/                        # Next.js app directory
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home/dashboard
│   ├── (auth)/                 # Auth routes
│   │   ├── login/
│   │   └── signup/
│   ├── dashboard/
│   │   └── page.tsx
│   ├── resumes/
│   │   ├── page.tsx            # Resume list
│   │   ├── [id]/
│   │   │   └── page.tsx        # Resume detail
│   │   └── upload/
│   │       └── page.tsx
│   ├── applications/
│   │   ├── page.tsx            # Application list
│   │   ├── [id]/
│   │   │   └── page.tsx        # Application detail
│   │   └── new/
│   │       └── page.tsx        # New application flow
│   └── interview-prep/
│       └── [applicationId]/
│           └── page.tsx
│
├── components/
│   ├── ui/                     # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   ├── Badge.tsx
│   │   └── Toast.tsx
│   │
│   ├── resume/                 # Resume-specific components
│   │   ├── ResumeCard.tsx
│   │   ├── ResumeUpload.tsx
│   │   └── ResumePreview.tsx
│   │
│   ├── analysis/               # Analysis components
│   │   ├── FitAnalysis.tsx
│   │   ├── MatchCard.tsx
│   │   └── ProgressBar.tsx
│   │
│   ├── tailoring/              # Tailoring components
│   │   ├── SuggestionCard.tsx
│   │   ├── DiffViewer.tsx
│   │   └── SuggestionList.tsx
│   │
│   └── application/            # Application components
│       ├── ApplicationCard.tsx
│       └── ApplicationList.tsx
│
├── lib/
│   ├── api/                    # API client functions
│   │   ├── resumes.ts
│   │   ├── jobDescriptions.ts
│   │   ├── analysis.ts
│   │   └── applications.ts
│   │
│   ├── types/                  # TypeScript types
│   │   ├── resume.ts
│   │   ├── jobDescription.ts
│   │   ├── analysis.ts
│   │   └── application.ts
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useResumes.ts
│   │   ├── useApplications.ts
│   │   └── useToast.ts
│   │
│   └── utils/                  # Utility functions
│       ├── format.ts
│       ├── validation.ts
│       └── constants.ts
│
├── public/
│   └── images/
│
├── styles/
│   └── globals.css
│
├── .env.local.example
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```


## Naming Conventions

### General Rules

- Use descriptive, meaningful names
- Avoid abbreviations unless universally understood
- Be consistent across the codebase
- Names should reveal intent

### Backend (Python)

**Files:**
- snake_case: `resume_parser.py`, `fit_analysis.py`
- Descriptive: `cover_letter_service.py` not `cl_svc.py`

**Classes:**
- PascalCase: `ResumeParser`, `FitAnalysisService`
- Nouns: `UserRepository`, `ApplicationModel`

**Functions/Methods:**
- snake_case: `parse_resume()`, `generate_suggestions()`
- Verbs: `create_application()`, `validate_input()`

**Variables:**
- snake_case: `resume_data`, `user_id`, `fit_score`
- Descriptive: `parsed_resume` not `pr`

**Constants:**
- UPPER_SNAKE_CASE: `MAX_FILE_SIZE`, `ALLOWED_EXTENSIONS`

**Pydantic Models:**
- PascalCase: `ResumeData`, `JobDescriptionRequest`
- Suffix with purpose: `ResumeResponse`, `CreateApplicationRequest`

**Example:**
```python
# Good
class ResumeParsingService:
    def parse_resume(self, file_content: str) -> ResumeData:
        parsed_data = self._extract_sections(file_content)
        return ResumeData(**parsed_data)
    
    def _extract_sections(self, content: str) -> dict:
        # Private method
        pass

# Avoid
class ResParser:
    def parse(self, fc: str) -> dict:
        pd = self._ext(fc)
        return pd
```


### Frontend (TypeScript/React)

**Files:**
- PascalCase for components: `ResumeCard.tsx`, `FitAnalysis.tsx`
- camelCase for utilities: `formatDate.ts`, `apiClient.ts`
- kebab-case for routes: `app/job-descriptions/page.tsx`

**Components:**
- PascalCase: `ResumeUpload`, `SuggestionCard`
- Descriptive: `ApplicationList` not `AppList`

**Functions:**
- camelCase: `fetchResumes()`, `handleSubmit()`
- Verbs: `validateForm()`, `formatDate()`

**Variables:**
- camelCase: `resumeData`, `userId`, `isLoading`
- Boolean prefix: `isLoading`, `hasError`, `canSubmit`

**Types/Interfaces:**
- PascalCase: `Resume`, `JobDescription`, `FitAnalysis`
- Prefix interfaces with `I` only if needed for clarity
- Suffix props: `ButtonProps`, `CardProps`

**Constants:**
- UPPER_SNAKE_CASE: `API_BASE_URL`, `MAX_FILE_SIZE`
- Or camelCase for config: `apiBaseUrl`

**Example:**
```typescript
// Good
interface ResumeCardProps {
  resume: Resume;
  onDelete: (id: string) => void;
  isSelected?: boolean;
}

export function ResumeCard({ resume, onDelete, isSelected = false }: ResumeCardProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  
  const handleDelete = async () => {
    setIsDeleting(true);
    await onDelete(resume.id);
  };
  
  return (
    <Card className={isSelected ? 'selected' : ''}>
      {/* ... */}
    </Card>
  );
}

// Avoid
interface Props {
  r: any;
  del: Function;
  sel?: boolean;
}

export function RC({ r, del, sel }: Props) {
  // ...
}
```


## API Design Standards

### Endpoint Naming

**RESTful Conventions:**
- Use nouns, not verbs: `/resumes` not `/getResumes`
- Use plural for collections: `/applications` not `/application`
- Use kebab-case: `/job-descriptions` not `/jobDescriptions`
- Nested resources: `/applications/{id}/interview-prep`

**HTTP Methods:**
- GET: Retrieve resources
- POST: Create resources
- PUT/PATCH: Update resources
- DELETE: Delete resources

**Examples:**
```
GET    /api/resumes                    # List resumes
POST   /api/resumes/upload             # Upload resume
GET    /api/resumes/{id}               # Get resume
DELETE /api/resumes/{id}               # Delete resume

POST   /api/job-descriptions           # Create JD
GET    /api/job-descriptions/{id}      # Get JD

POST   /api/analysis/fit               # Analyze fit
GET    /api/analysis/fit/{id}          # Get fit analysis

POST   /api/analysis/tailoring         # Generate suggestions
GET    /api/analysis/tailoring/{id}    # Get suggestions

POST   /api/generate/resume            # Generate resume
POST   /api/generate/cover-letter      # Generate cover letter

GET    /api/applications               # List applications
POST   /api/applications               # Create application
GET    /api/applications/{id}          # Get application
PATCH  /api/applications/{id}          # Update application
DELETE /api/applications/{id}          # Delete application

POST   /api/interview-prep             # Generate prep
GET    /api/interview-prep/{app_id}    # Get prep
```

### Request/Response Models

**Naming:**
- Request: `CreateResumeRequest`, `UpdateApplicationRequest`
- Response: `ResumeResponse`, `FitAnalysisResponse`
- List response: `ResumeListResponse`

**Structure:**
```python
# Request model
class CreateApplicationRequest(BaseModel):
    resume_id: str
    job_description_id: str
    company: str
    title: str
    notes: Optional[str] = None

# Response model
class ApplicationResponse(BaseModel):
    id: str
    user_id: str
    resume_id: str
    job_description_id: str
    company: str
    title: str
    status: str
    applied_date: date
    created_at: datetime
    updated_at: datetime

# List response
class ApplicationListResponse(BaseModel):
    applications: List[ApplicationResponse]
    total: int
    page: int
    page_size: int
```


### Error Responses

**Consistent Format:**
```python
class ErrorResponse(BaseModel):
    error: str          # Error type
    detail: str         # Human-readable message
    code: str           # Error code for client handling
    field: Optional[str] = None  # For validation errors

# Usage
@router.post("/resumes/upload")
async def upload_resume(file: UploadFile):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "File too large",
                "detail": f"File size must be under {MAX_FILE_SIZE / 1024 / 1024}MB",
                "code": "FILE_TOO_LARGE"
            }
        )
```

**Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity (business logic errors)
- 500: Internal Server Error

## Backend Code Standards

### Service Layer Pattern

**Separation of Concerns:**
- Routers: Handle HTTP, validation, auth
- Services: Business logic, orchestration
- Repositories: Data access only
- Utils: Shared utilities

**Example:**
```python
# routers/resumes.py
@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends()
):
    """Upload and parse a resume."""
    try:
        resume = await resume_service.upload_and_parse(file, current_user.id)
        return resume
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# services/resume_parser.py
class ResumeService:
    def __init__(
        self,
        repository: ResumeRepository,
        ai_client: AIClient,
        storage: StorageClient
    ):
        self.repository = repository
        self.ai_client = ai_client
        self.storage = storage
    
    async def upload_and_parse(self, file: UploadFile, user_id: str) -> Resume:
        # Validate file
        self._validate_file(file)
        
        # Extract text
        text = await self._extract_text(file)
        
        # Parse with AI
        parsed_data = await self.ai_client.parse_resume(text)
        
        # Validate parsed data
        validated_data = ResumeData(**parsed_data)
        
        # Store file
        file_url = await self.storage.upload(file, user_id)
        
        # Save to database
        resume = await self.repository.create(
            user_id=user_id,
            parsed_data=validated_data.dict(),
            file_url=file_url
        )
        
        return resume

# repositories/resume_repository.py
class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    async def create(self, user_id: str, parsed_data: dict, file_url: str) -> Resume:
        resume = ResumeModel(
            user_id=user_id,
            parsed_data=parsed_data,
            original_file_url=file_url
        )
        self.db.add(resume)
        await self.db.commit()
        await self.db.refresh(resume)
        return resume
    
    async def get_by_id(self, resume_id: str) -> Optional[Resume]:
        return await self.db.query(ResumeModel).filter(
            ResumeModel.id == resume_id
        ).first()
```


### Pydantic Models

**Best Practices:**
- Use type hints for all fields
- Provide default values where appropriate
- Use Optional for nullable fields
- Add field descriptions for documentation
- Use validators for complex validation

**Example:**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date

class Experience(BaseModel):
    company: str = Field(..., min_length=1, description="Company name")
    title: str = Field(..., min_length=1, description="Job title")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date or 'Present'")
    location: Optional[str] = None
    bullets: List[str] = Field(..., min_items=1, description="Achievement bullets")
    
    @validator('bullets')
    def validate_bullets(cls, v):
        if not v:
            raise ValueError('At least one bullet point required')
        if any(len(bullet.strip()) < 10 for bullet in v):
            raise ValueError('Bullet points must be at least 10 characters')
        return v

class ResumeData(BaseModel):
    contact: ContactInfo
    summary: Optional[str] = None
    experience: List[Experience] = []
    education: List[Education] = []
    skills: Skills
    projects: List[Project] = []
    certifications: List[Certification] = []
    
    class Config:
        # Allow ORM models
        orm_mode = True
        # Example for documentation
        schema_extra = {
            "example": {
                "contact": {
                    "name": "John Doe",
                    "email": "john@example.com"
                },
                "experience": [
                    {
                        "company": "Tech Corp",
                        "title": "Software Engineer",
                        "bullets": ["Built REST API"]
                    }
                ]
            }
        }
```

### Input Validation

**Always Validate:**
- File uploads (type, size)
- User input (length, format)
- AI outputs (schema, business rules)
- Database queries (existence, ownership)

**Example:**
```python
def validate_file_upload(file: UploadFile) -> None:
    """Validate uploaded file."""
    # Check file extension
    allowed_extensions = {'.pdf', '.docx', '.txt'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise ValueError(
            f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Check file size
    if file.size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Check file is not empty
    if file.size == 0:
        raise ValueError("File is empty")

def validate_user_owns_resource(user_id: str, resource_user_id: str) -> None:
    """Ensure user owns the resource."""
    if user_id != resource_user_id:
        raise PermissionError("You don't have permission to access this resource")
```


### Error Handling & Logging

**Error Handling:**
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ResumeService:
    async def parse_resume(self, file_content: str) -> ResumeData:
        try:
            # Call AI service
            raw_output = await self.ai_client.parse_resume(file_content)
            
            # Validate output
            parsed_data = ResumeData(**raw_output)
            
            logger.info(f"Successfully parsed resume")
            return parsed_data
            
        except ValidationError as e:
            logger.error(f"Resume parsing validation failed: {e}")
            raise ValueError("Failed to parse resume. Please check the format.")
        
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise RuntimeError("AI service temporarily unavailable. Please try again.")
        
        except Exception as e:
            logger.exception(f"Unexpected error parsing resume: {e}")
            raise RuntimeError("An unexpected error occurred. Please try again.")
```

**Logging Levels:**
- DEBUG: Detailed information for debugging
- INFO: General informational messages
- WARNING: Warning messages (recoverable issues)
- ERROR: Error messages (handled exceptions)
- CRITICAL: Critical errors (system failures)

**What to Log:**
```python
# Good logging
logger.info(f"User {user_id} uploaded resume")
logger.info(f"Parsing resume for user {user_id}")
logger.error(f"Failed to parse resume for user {user_id}: {error}")
logger.warning(f"AI validation failed, retrying (attempt {retry_count})")

# Don't log sensitive data
logger.info(f"Resume content: {resume_text}")  # BAD
logger.info(f"User email: {email}")  # BAD
logger.info(f"API key: {api_key}")  # BAD
```

**Logging Configuration:**
```python
# config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'app.log',
                maxBytes=10485760,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```


## Frontend Code Standards

### React Component Structure

**Component Organization:**
```typescript
// ResumeCard.tsx
import { useState } from 'react';
import { Resume } from '@/lib/types/resume';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

// 1. Types/Interfaces
interface ResumeCardProps {
  resume: Resume;
  onDelete: (id: string) => void;
  onSelect?: (id: string) => void;
  isSelected?: boolean;
}

// 2. Component
export function ResumeCard({ 
  resume, 
  onDelete, 
  onSelect,
  isSelected = false 
}: ResumeCardProps) {
  // 3. State
  const [isDeleting, setIsDeleting] = useState(false);
  
  // 4. Handlers
  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this resume?')) {
      return;
    }
    
    setIsDeleting(true);
    try {
      await onDelete(resume.id);
    } catch (error) {
      console.error('Failed to delete resume:', error);
      alert('Failed to delete resume. Please try again.');
    } finally {
      setIsDeleting(false);
    }
  };
  
  const handleSelect = () => {
    onSelect?.(resume.id);
  };
  
  // 5. Render
  return (
    <Card 
      className={`resume-card ${isSelected ? 'selected' : ''}`}
      onClick={handleSelect}
    >
      <div className="resume-card-header">
        <h3>{resume.name}</h3>
        <span className="date">
          {formatDate(resume.created_at)}
        </span>
      </div>
      
      <div className="resume-card-actions">
        <Button 
          variant="secondary" 
          onClick={(e) => {
            e.stopPropagation();
            // View action
          }}
        >
          View
        </Button>
        <Button 
          variant="danger" 
          onClick={(e) => {
            e.stopPropagation();
            handleDelete();
          }}
          disabled={isDeleting}
        >
          {isDeleting ? 'Deleting...' : 'Delete'}
        </Button>
      </div>
    </Card>
  );
}
```

### TypeScript Best Practices

**Type Definitions:**
```typescript
// lib/types/resume.ts

// Use interfaces for object shapes
export interface Resume {
  id: string;
  user_id: string;
  name: string;
  parsed_data: ResumeData;
  original_file_url: string;
  created_at: string;
  updated_at: string;
}

export interface ResumeData {
  contact: ContactInfo;
  summary?: string;
  experience: Experience[];
  education: Education[];
  skills: Skills;
  projects: Project[];
  certifications: Certification[];
}

export interface Experience {
  company: string;
  title: string;
  start_date?: string;
  end_date?: string;
  location?: string;
  bullets: string[];
}

// Use type for unions or aliases
export type ResumeStatus = 'draft' | 'active' | 'archived';

export type ApplicationStatus = 
  | 'applied' 
  | 'interviewing' 
  | 'offer' 
  | 'rejected' 
  | 'withdrawn';

// Use enums sparingly (prefer union types)
export enum MatchType {
  Strong = 'strong',
  Partial = 'partial',
  Missing = 'missing'
}
```


### API Client Pattern

**Centralized API Calls:**
```typescript
// lib/api/resumes.ts
import { Resume, ResumeData } from '@/lib/types/resume';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json();
    throw new APIError(
      error.detail || 'An error occurred',
      response.status,
      error.code
    );
  }
  return response.json();
}

export async function uploadResume(file: File): Promise<Resume> {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/api/resumes/upload`, {
    method: 'POST',
    body: formData,
    headers: {
      'Authorization': `Bearer ${getAuthToken()}`
    }
  });
  
  return handleResponse<Resume>(response);
}

export async function getResumes(): Promise<Resume[]> {
  const response = await fetch(`${API_BASE_URL}/api/resumes`, {
    headers: {
      'Authorization': `Bearer ${getAuthToken()}`
    }
  });
  
  const data = await handleResponse<{ resumes: Resume[] }>(response);
  return data.resumes;
}

export async function deleteResume(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/resumes/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${getAuthToken()}`
    }
  });
  
  await handleResponse<void>(response);
}

function getAuthToken(): string {
  // Get token from storage or context
  return localStorage.getItem('auth_token') || '';
}
```

### Custom Hooks

**Reusable Logic:**
```typescript
// lib/hooks/useResumes.ts
import { useState, useEffect } from 'react';
import { Resume } from '@/lib/types/resume';
import * as resumeApi from '@/lib/api/resumes';

export function useResumes() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    loadResumes();
  }, []);
  
  const loadResumes = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await resumeApi.getResumes();
      setResumes(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load resumes');
    } finally {
      setIsLoading(false);
    }
  };
  
  const uploadResume = async (file: File) => {
    try {
      const newResume = await resumeApi.uploadResume(file);
      setResumes(prev => [...prev, newResume]);
      return newResume;
    } catch (err) {
      throw err;
    }
  };
  
  const deleteResume = async (id: string) => {
    try {
      await resumeApi.deleteResume(id);
      setResumes(prev => prev.filter(r => r.id !== id));
    } catch (err) {
      throw err;
    }
  };
  
  return {
    resumes,
    isLoading,
    error,
    uploadResume,
    deleteResume,
    refresh: loadResumes
  };
}

// Usage in component
function ResumesPage() {
  const { resumes, isLoading, error, uploadResume, deleteResume } = useResumes();
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return (
    <div>
      {resumes.map(resume => (
        <ResumeCard 
          key={resume.id}
          resume={resume}
          onDelete={deleteResume}
        />
      ))}
    </div>
  );
}
```


### Component Reusability

**Create Reusable UI Components:**
```typescript
// components/ui/Button.tsx
import { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  children,
  className = '',
  ...props
}: ButtonProps) {
  const baseClasses = 'button';
  const variantClasses = `button-${variant}`;
  const sizeClasses = `button-${size}`;
  const disabledClasses = (disabled || isLoading) ? 'button-disabled' : '';
  
  return (
    <button
      className={`${baseClasses} ${variantClasses} ${sizeClasses} ${disabledClasses} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <>
          <LoadingSpinner size="sm" />
          <span>Loading...</span>
        </>
      ) : (
        children
      )}
    </button>
  );
}

// Usage
<Button variant="primary" onClick={handleSubmit}>
  Submit
</Button>

<Button variant="danger" isLoading={isDeleting} onClick={handleDelete}>
  Delete
</Button>
```

**Composition Over Props:**
```typescript
// Good - Flexible composition
<Card>
  <CardHeader>
    <h3>Resume Name</h3>
    <Badge>Active</Badge>
  </CardHeader>
  <CardContent>
    <p>Details here</p>
  </CardContent>
  <CardActions>
    <Button>Edit</Button>
    <Button variant="danger">Delete</Button>
  </CardActions>
</Card>

// Avoid - Too many props
<Card 
  title="Resume Name"
  badge="Active"
  content="Details here"
  actions={[
    { label: 'Edit', onClick: handleEdit },
    { label: 'Delete', onClick: handleDelete, variant: 'danger' }
  ]}
/>
```


## Database Standards

### Migration Management

**Alembic Migrations:**
```bash
# Create a new migration
alembic revision --autogenerate -m "Add applications table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

**Migration Best Practices:**
- One logical change per migration
- Descriptive migration messages
- Test migrations before committing
- Include both upgrade and downgrade
- Never edit applied migrations

**Example Migration:**
```python
# alembic/versions/001_add_resumes_table.py
"""Add resumes table

Revision ID: 001
Revises: 
Create Date: 2026-04-01 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'resumes',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('parsed_data', JSONB, nullable=False),
        sa.Column('original_file_url', sa.String(500), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )
    
    # Add indexes
    op.create_index('idx_resumes_user_id', 'resumes', ['user_id'])
    op.create_index('idx_resumes_created_at', 'resumes', ['created_at'])

def downgrade():
    op.drop_index('idx_resumes_created_at')
    op.drop_index('idx_resumes_user_id')
    op.drop_table('resumes')
```

### Database Schema Conventions

**Table Names:**
- Plural, snake_case: `resumes`, `job_descriptions`, `fit_analyses`

**Column Names:**
- snake_case: `user_id`, `created_at`, `parsed_data`
- Use `_id` suffix for foreign keys
- Use `_at` suffix for timestamps
- Use `is_` prefix for booleans

**Primary Keys:**
- Use UUID for all primary keys
- Name: `id`

**Foreign Keys:**
- Name: `{table}_id` (e.g., `user_id`, `resume_id`)
- Add indexes on foreign keys

**Timestamps:**
- Always include: `created_at`, `updated_at`
- Use server defaults

**JSON Columns:**
- Use JSONB in Postgres (not JSON)
- For structured, queryable data


## Environment Variables

### Backend (.env)

**Structure:**
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/jobcopilot

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-supabase-key
SUPABASE_SERVICE_KEY=your-service-key

# OpenAI
OPENAI_API_KEY=sk-xxxxx

# Storage
STORAGE_BUCKET=resumes

# App Config
ENVIRONMENT=development  # development, staging, production
DEBUG=true
LOG_LEVEL=INFO

# Security
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,https://yourapp.com

# Limits
MAX_FILE_SIZE=5242880  # 5MB in bytes
```

**Loading Environment Variables:**
```python
# config.py
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    database_url: str
    
    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    
    # OpenAI
    openai_api_key: str
    
    # Storage
    storage_bucket: str = "resumes"
    
    # App
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    
    # Security
    secret_key: str
    cors_origins: List[str] = []
    
    # Limits
    max_file_size: int = 5242880
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### Frontend (.env.local)

**Structure:**
```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Supabase (public keys only)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# App Config
NEXT_PUBLIC_APP_NAME=AI Job Application Copilot
NEXT_PUBLIC_ENVIRONMENT=development
```

**Usage:**
```typescript
// lib/config.ts
export const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  supabase: {
    url: process.env.NEXT_PUBLIC_SUPABASE_URL!,
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  },
  appName: process.env.NEXT_PUBLIC_APP_NAME || 'Job Copilot',
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT || 'development'
};
```

**Security Rules:**
- Never commit `.env` files
- Provide `.env.example` with dummy values
- Use `NEXT_PUBLIC_` prefix for client-side variables only
- Keep sensitive keys server-side only
- Rotate keys regularly


## Testing Standards

### Testing Philosophy

**For MVP:**
- Focus on critical paths
- Test business logic thoroughly
- Test AI validation rigorously
- Test API endpoints
- Skip UI tests initially (manual QA)

**What to Test:**
- Service layer business logic
- AI output validation
- Data transformations
- Error handling
- API endpoints

**What to Skip (for MVP):**
- UI component tests (manual QA)
- E2E tests (manual QA)
- Performance tests
- Load tests

### Backend Testing

**Test Structure:**
```python
# tests/test_services/test_resume_parser.py
import pytest
from app.services.resume_parser import ResumeService
from app.models.resume import ResumeData

@pytest.fixture
def resume_service():
    """Create resume service with mocked dependencies."""
    return ResumeService(
        repository=MockResumeRepository(),
        ai_client=MockAIClient(),
        storage=MockStorageClient()
    )

@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """
    John Doe
    john@example.com
    
    Experience:
    Software Engineer at Tech Corp
    - Built REST API with Python
    """

class TestResumeParser:
    """Test resume parsing service."""
    
    def test_parse_resume_success(self, resume_service, sample_resume_text):
        """Test successful resume parsing."""
        result = resume_service.parse_resume(sample_resume_text)
        
        assert isinstance(result, ResumeData)
        assert result.contact.name == "John Doe"
        assert result.contact.email == "john@example.com"
        assert len(result.experience) > 0
    
    def test_parse_resume_invalid_format(self, resume_service):
        """Test parsing with invalid format."""
        with pytest.raises(ValueError, match="Failed to parse resume"):
            resume_service.parse_resume("")
    
    def test_parse_resume_missing_contact(self, resume_service):
        """Test parsing with missing contact info."""
        invalid_text = "Some text without contact info"
        
        with pytest.raises(ValueError):
            resume_service.parse_resume(invalid_text)
    
    def test_validate_parsed_data(self, resume_service):
        """Test validation of AI output."""
        # AI returns invalid data
        invalid_data = {"contact": {}}  # Missing required fields
        
        with pytest.raises(ValidationError):
            ResumeData(**invalid_data)
```

**Testing AI Validation:**
```python
# tests/test_services/test_ai_validation.py
import pytest
from app.services.tailoring import TailoringService
from app.models.tailoring import TailoringSuggestion

class TestAIValidation:
    """Test AI output validation."""
    
    def test_reject_fabricated_skills(self):
        """Ensure AI doesn't add skills not in resume."""
        resume_data = {
            "skills": {"languages": ["Python", "JavaScript"]}
        }
        
        suggestion = {
            "type": "rephrase",
            "suggested": "Experience with Python, JavaScript, and Java"
        }
        
        # Validation should fail - Java not in original resume
        with pytest.raises(ValueError, match="fabricated"):
            validate_no_fabrication(resume_data, suggestion)
    
    def test_accept_valid_rephrase(self):
        """Accept valid rephrasing without new claims."""
        original = "Built REST API with Python"
        suggested = "Developed RESTful API using Python"
        
        # Should pass - no new information added
        assert validate_rephrase(original, suggested) is True
    
    def test_reject_inflated_metrics(self):
        """Reject suggestions that inflate numbers."""
        original = "Improved performance by 20%"
        suggested = "Improved performance by 50%"
        
        # Should fail - numbers changed
        with pytest.raises(ValueError, match="inflated"):
            validate_rephrase(original, suggested)
```


**API Endpoint Testing:**
```python
# tests/test_routers/test_resumes.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    """Get auth headers for testing."""
    # Login and get token
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpass"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestResumeEndpoints:
    """Test resume API endpoints."""
    
    def test_upload_resume_success(self, auth_headers):
        """Test successful resume upload."""
        with open("tests/fixtures/sample_resume.pdf", "rb") as f:
            response = client.post(
                "/api/resumes/upload",
                files={"file": ("resume.pdf", f, "application/pdf")},
                headers=auth_headers
            )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "parsed_data" in data
    
    def test_upload_resume_invalid_format(self, auth_headers):
        """Test upload with invalid file format."""
        with open("tests/fixtures/invalid.txt", "rb") as f:
            response = client.post(
                "/api/resumes/upload",
                files={"file": ("file.exe", f, "application/exe")},
                headers=auth_headers
            )
        
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
    
    def test_get_resumes(self, auth_headers):
        """Test getting user's resumes."""
        response = client.get("/api/resumes", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "resumes" in data
        assert isinstance(data["resumes"], list)
    
    def test_delete_resume_unauthorized(self):
        """Test deleting resume without auth."""
        response = client.delete("/api/resumes/123")
        
        assert response.status_code == 401
```

### Running Tests

**Commands:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_services/test_resume_parser.py

# Run specific test
pytest tests/test_services/test_resume_parser.py::TestResumeParser::test_parse_resume_success

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

**Test Coverage Goals:**
- Critical services: 80%+ coverage
- API endpoints: 70%+ coverage
- Utilities: 60%+ coverage
- Overall: 70%+ coverage (MVP)


## Documentation Standards

### Code Documentation

**Python Docstrings:**
```python
def parse_resume(self, file_content: str, user_id: str) -> ResumeData:
    """
    Parse resume text and extract structured data.
    
    Args:
        file_content: Raw text content of the resume
        user_id: ID of the user uploading the resume
    
    Returns:
        ResumeData: Structured resume data with validated fields
    
    Raises:
        ValueError: If resume format is invalid or parsing fails
        ValidationError: If extracted data doesn't match schema
    
    Example:
        >>> service = ResumeService()
        >>> data = service.parse_resume(resume_text, "user-123")
        >>> print(data.contact.name)
        'John Doe'
    """
    # Implementation
```

**TypeScript JSDoc:**
```typescript
/**
 * Upload and parse a resume file
 * 
 * @param file - The resume file to upload (PDF or DOCX)
 * @returns Promise resolving to the parsed resume data
 * @throws {APIError} If upload fails or file format is invalid
 * 
 * @example
 * ```typescript
 * const resume = await uploadResume(file);
 * console.log(resume.parsed_data.contact.name);
 * ```
 */
export async function uploadResume(file: File): Promise<Resume> {
  // Implementation
}
```

**When to Document:**
- All public functions/methods
- Complex algorithms
- Non-obvious business logic
- API endpoints
- Utility functions

**When Not to Document:**
- Self-explanatory code
- Private helper methods (unless complex)
- Getters/setters
- Obvious variable names

### README Documentation

**Backend README.md:**
```markdown
# AI Job Application Copilot - Backend

FastAPI backend for the AI Job Application Copilot.

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- OpenAI API key

### Installation

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

- `app/models/` - Pydantic request/response models
- `app/schemas/` - SQLAlchemy database models
- `app/services/` - Business logic
- `app/repositories/` - Data access layer
- `app/routers/` - API endpoints
- `app/utils/` - Utilities

## Testing

Run tests:
```bash
pytest
```

With coverage:
```bash
pytest --cov=app
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
```

**Frontend README.md:**
```markdown
# AI Job Application Copilot - Frontend

Next.js frontend for the AI Job Application Copilot.

## Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your values
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Open http://localhost:3000

## Project Structure

- `app/` - Next.js pages and routes
- `components/` - React components
- `lib/api/` - API client functions
- `lib/types/` - TypeScript types
- `lib/hooks/` - Custom React hooks
- `lib/utils/` - Utility functions

## Building

Build for production:
```bash
npm run build
```

Start production server:
```bash
npm start
```

## Code Style

Format code:
```bash
npm run format
```

Lint code:
```bash
npm run lint
```
```


### API Documentation

**FastAPI Auto-Documentation:**
```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="AI Job Application Copilot API",
    description="API for AI-powered job application assistance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Endpoint documentation
@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=201,
    summary="Upload and parse resume",
    description="""
    Upload a resume file (PDF or DOCX) and parse it into structured data.
    
    The resume will be analyzed using AI to extract:
    - Contact information
    - Work experience
    - Education
    - Skills
    - Projects
    - Certifications
    
    The parsed data is validated and stored for future use.
    """,
    responses={
        201: {
            "description": "Resume uploaded and parsed successfully",
            "model": ResumeResponse
        },
        400: {
            "description": "Invalid file format or parsing failed",
            "model": ErrorResponse
        },
        401: {
            "description": "Unauthorized - invalid or missing token"
        }
    }
)
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (PDF or DOCX, max 5MB)"),
    current_user: User = Depends(get_current_user)
):
    """Upload and parse a resume."""
    # Implementation
```

### Inline Comments

**When to Comment:**
```python
# Good - Explain why, not what
# Use exponential backoff to avoid rate limiting
for attempt in range(max_retries):
    try:
        return await self.ai_client.call()
    except RateLimitError:
        await asyncio.sleep(2 ** attempt)

# Good - Explain complex logic
# Calculate match score: (strong_matches * 1.0 + partial_matches * 0.5) / total_requirements
match_score = (len(strong) + len(partial) * 0.5) / total

# Avoid - Obvious comments
# Increment counter
counter += 1

# Avoid - Commented-out code (delete it)
# old_function()
# return old_value
```

**Comment Style:**
```python
# Python: Use # for single-line comments
# Use """ for docstrings

# TODO: Add caching for parsed resumes
# FIXME: Handle edge case when resume has no experience
# NOTE: This assumes JD is in English
```

```typescript
// TypeScript: Use // for single-line comments
// Use /** */ for JSDoc

// TODO: Add retry logic for failed uploads
// FIXME: Handle network errors gracefully
// NOTE: This component assumes user is authenticated
```


## Code Quality Tools

### Backend (Python)

**Formatting:**
```bash
# Install Black
pip install black

# Format code
black app/

# Check without modifying
black --check app/
```

**Linting:**
```bash
# Install Flake8
pip install flake8

# Lint code
flake8 app/

# Configuration in .flake8 or setup.cfg
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E203,W503
```

**Type Checking:**
```bash
# Install mypy
pip install mypy

# Type check
mypy app/

# Configuration in mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

**Pre-commit Hooks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### Frontend (TypeScript)

**Formatting:**
```bash
# Install Prettier
npm install --save-dev prettier

# Format code
npm run format

# package.json
{
  "scripts": {
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,css,md}\""
  }
}
```

**Linting:**
```bash
# ESLint (included with Next.js)
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

**Type Checking:**
```bash
# TypeScript compiler
npm run type-check

# package.json
{
  "scripts": {
    "type-check": "tsc --noEmit"
  }
}
```

**Configuration Files:**

`.prettierrc`:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

`.eslintrc.json`:
```json
{
  "extends": ["next/core-web-vitals", "prettier"],
  "rules": {
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "prefer-const": "error",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```


## Git Workflow

### Branch Naming

**Convention:**
- `feature/` - New features: `feature/resume-tailoring`
- `fix/` - Bug fixes: `fix/upload-validation`
- `refactor/` - Code refactoring: `refactor/service-layer`
- `docs/` - Documentation: `docs/api-readme`
- `test/` - Tests: `test/resume-parser`

### Commit Messages

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `docs:` - Documentation
- `test:` - Tests
- `chore:` - Maintenance

**Examples:**
```bash
# Good
git commit -m "feat: add resume tailoring suggestions"
git commit -m "fix: validate file size before upload"
git commit -m "refactor: extract AI client to separate service"

# With body
git commit -m "feat: add cover letter generation

- Implement CoverLetterService
- Add API endpoint
- Add request/response models
- Include evidence mapping"

# Avoid
git commit -m "updates"
git commit -m "fix stuff"
git commit -m "WIP"
```

### Pull Request Guidelines

**PR Title:**
- Clear and descriptive
- Follow commit message format
- Example: `feat: Add resume tailoring suggestions`

**PR Description:**
```markdown
## Description
Brief description of changes

## Changes
- Added ResumeService
- Implemented parsing logic
- Added validation

## Testing
- [ ] Unit tests added
- [ ] Manual testing completed
- [ ] API endpoints tested

## Screenshots (if UI changes)
[Add screenshots]

## Related Issues
Closes #123
```

### Code Review Checklist

**Reviewer Checklist:**
- [ ] Code follows style guidelines
- [ ] Functions are small and focused
- [ ] Names are clear and descriptive
- [ ] Error handling is appropriate
- [ ] Input validation is present
- [ ] Tests are included
- [ ] Documentation is updated
- [ ] No sensitive data in code
- [ ] No console.logs or debug code


## Common Patterns & Best Practices

### Error Handling Patterns

**Backend:**
```python
# Good - Specific error handling
try:
    resume = await self.parse_resume(content)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    raise ValueError("Invalid resume format")
except OpenAIError as e:
    logger.error(f"AI service error: {e}")
    raise RuntimeError("AI service unavailable")
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise

# Avoid - Catching all exceptions silently
try:
    resume = await self.parse_resume(content)
except:
    pass
```

**Frontend:**
```typescript
// Good - User-friendly error handling
try {
  const resume = await uploadResume(file);
  toast.success('Resume uploaded successfully');
  router.push(`/resumes/${resume.id}`);
} catch (error) {
  if (error instanceof APIError) {
    if (error.code === 'FILE_TOO_LARGE') {
      toast.error('File is too large. Maximum size is 5MB.');
    } else if (error.code === 'INVALID_FORMAT') {
      toast.error('Invalid file format. Please upload PDF or DOCX.');
    } else {
      toast.error(error.message);
    }
  } else {
    toast.error('An unexpected error occurred. Please try again.');
  }
}

// Avoid - Generic error handling
try {
  await uploadResume(file);
} catch (error) {
  alert('Error');
}
```

### Async/Await Patterns

**Backend:**
```python
# Good - Proper async/await
async def process_application(self, resume_id: str, jd_id: str) -> Application:
    # Fetch data concurrently
    resume, jd = await asyncio.gather(
        self.resume_repo.get(resume_id),
        self.jd_repo.get(jd_id)
    )
    
    # Process sequentially
    fit_analysis = await self.analyze_fit(resume, jd)
    suggestions = await self.generate_suggestions(resume, jd, fit_analysis)
    
    return await self.create_application(resume, jd, suggestions)

# Avoid - Blocking calls in async function
async def process_application(self, resume_id: str, jd_id: str):
    resume = self.resume_repo.get(resume_id)  # Blocking!
    jd = self.jd_repo.get(jd_id)  # Blocking!
    return resume, jd
```

**Frontend:**
```typescript
// Good - Proper async handling
async function handleSubmit() {
  setIsLoading(true);
  setError(null);
  
  try {
    const result = await submitApplication(data);
    toast.success('Application submitted');
    router.push(`/applications/${result.id}`);
  } catch (err) {
    setError(err.message);
  } finally {
    setIsLoading(false);
  }
}

// Avoid - Not handling loading/error states
async function handleSubmit() {
  const result = await submitApplication(data);
  router.push(`/applications/${result.id}`);
}
```


### Validation Patterns

**Backend:**
```python
# Good - Comprehensive validation
def validate_resume_upload(file: UploadFile) -> None:
    """Validate resume file before processing."""
    # Check file exists
    if not file:
        raise ValueError("No file provided")
    
    # Check file extension
    allowed_extensions = {'.pdf', '.docx', '.txt'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise ValueError(
            f"Invalid file type '{file_ext}'. "
            f"Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Check file size
    if file.size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large ({file.size / 1024 / 1024:.1f}MB). "
            f"Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Check file is not empty
    if file.size == 0:
        raise ValueError("File is empty")

# Use Pydantic for data validation
class CreateApplicationRequest(BaseModel):
    resume_id: str = Field(..., min_length=1)
    job_description_id: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    notes: Optional[str] = Field(None, max_length=5000)
    
    @validator('resume_id', 'job_description_id')
    def validate_uuid(cls, v):
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('Invalid UUID format')
        return v
```

**Frontend:**
```typescript
// Good - Client-side validation
function validateResumeFile(file: File): string | null {
  const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  const maxSize = 5 * 1024 * 1024; // 5MB
  
  if (!allowedTypes.includes(file.type)) {
    return 'Invalid file type. Please upload PDF or DOCX.';
  }
  
  if (file.size > maxSize) {
    return `File too large (${(file.size / 1024 / 1024).toFixed(1)}MB). Maximum size is 5MB.`;
  }
  
  if (file.size === 0) {
    return 'File is empty.';
  }
  
  return null; // Valid
}

// Usage
function handleFileSelect(file: File) {
  const error = validateResumeFile(file);
  if (error) {
    toast.error(error);
    return;
  }
  
  // Proceed with upload
  uploadResume(file);
}
```

### Dependency Injection

**Backend:**
```python
# Good - Use FastAPI dependency injection
from fastapi import Depends

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_resume_repository(db: Session = Depends(get_db)) -> ResumeRepository:
    return ResumeRepository(db)

def get_resume_service(
    repository: ResumeRepository = Depends(get_resume_repository),
    ai_client: AIClient = Depends(get_ai_client),
    storage: StorageClient = Depends(get_storage_client)
) -> ResumeService:
    return ResumeService(repository, ai_client, storage)

# Use in routes
@router.post("/upload")
async def upload_resume(
    file: UploadFile,
    service: ResumeService = Depends(get_resume_service),
    current_user: User = Depends(get_current_user)
):
    return await service.upload_and_parse(file, current_user.id)
```


## Performance Best Practices

### Backend Performance

**Database Queries:**
```python
# Good - Eager loading to avoid N+1 queries
def get_applications_with_details(user_id: str) -> List[Application]:
    return db.query(Application)\
        .options(
            joinedload(Application.resume),
            joinedload(Application.job_description)
        )\
        .filter(Application.user_id == user_id)\
        .all()

# Avoid - N+1 query problem
def get_applications_with_details(user_id: str):
    applications = db.query(Application).filter(Application.user_id == user_id).all()
    for app in applications:
        app.resume  # Triggers separate query for each!
        app.job_description  # Another query!
    return applications
```

**Caching:**
```python
# Good - Cache expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def get_parsed_resume(resume_id: str) -> ResumeData:
    """Get parsed resume with caching."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    return ResumeData(**resume.parsed_data)

# Cache AI responses when appropriate
async def analyze_fit(resume_id: str, jd_id: str) -> FitAnalysis:
    cache_key = f"fit:{resume_id}:{jd_id}"
    
    # Check cache
    cached = await cache.get(cache_key)
    if cached:
        return FitAnalysis(**cached)
    
    # Generate if not cached
    analysis = await self.ai_client.analyze_fit(resume, jd)
    
    # Cache for 1 hour
    await cache.set(cache_key, analysis.dict(), expire=3600)
    
    return analysis
```

### Frontend Performance

**Lazy Loading:**
```typescript
// Good - Lazy load heavy components
import dynamic from 'next/dynamic';

const DiffViewer = dynamic(() => import('@/components/tailoring/DiffViewer'), {
  loading: () => <LoadingSpinner />,
  ssr: false
});

// Use in component
function TailoringSuggestions() {
  return (
    <div>
      <h2>Review Changes</h2>
      <DiffViewer original={original} suggested={suggested} />
    </div>
  );
}
```

**Memoization:**
```typescript
// Good - Memoize expensive computations
import { useMemo } from 'react';

function FitAnalysis({ matches }: { matches: Match[] }) {
  const matchScore = useMemo(() => {
    const strong = matches.filter(m => m.type === 'strong').length;
    const partial = matches.filter(m => m.type === 'partial').length;
    const total = matches.length;
    
    return ((strong + partial * 0.5) / total) * 100;
  }, [matches]);
  
  return <div>Match Score: {matchScore.toFixed(0)}%</div>;
}

// Good - Memoize callbacks
import { useCallback } from 'react';

function ResumeList({ resumes }: { resumes: Resume[] }) {
  const handleDelete = useCallback(async (id: string) => {
    await deleteResume(id);
  }, []);
  
  return (
    <div>
      {resumes.map(resume => (
        <ResumeCard 
          key={resume.id}
          resume={resume}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
}
```


## Security Best Practices

### Input Sanitization

**Backend:**
```python
# Good - Sanitize user input
from bleach import clean

def sanitize_text_input(text: str) -> str:
    """Remove potentially harmful content from text."""
    # Remove HTML tags
    cleaned = clean(text, tags=[], strip=True)
    
    # Trim whitespace
    cleaned = cleaned.strip()
    
    # Limit length
    max_length = 10000
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned

# Use in service
def create_job_description(self, raw_text: str, user_id: str) -> JobDescription:
    # Sanitize input
    sanitized_text = sanitize_text_input(raw_text)
    
    # Process
    parsed_data = await self.parse_jd(sanitized_text)
    return await self.repository.create(user_id, sanitized_text, parsed_data)
```

### Authentication & Authorization

**Backend:**
```python
# Good - Verify user ownership
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    repository: ResumeRepository = Depends()
) -> Resume:
    resume = await repository.get_by_id(resume_id)
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Verify ownership
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return resume

# Good - Use dependency for auth checks
def require_ownership(resource_user_id: str, current_user: User = Depends(get_current_user)):
    if resource_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
```

**Frontend:**
```typescript
// Good - Include auth token in requests
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });
  
  if (response.status === 401) {
    // Token expired, redirect to login
    router.push('/login');
    throw new Error('Unauthorized');
  }
  
  return handleResponse<T>(response);
}
```

### Secrets Management

**Never:**
```python
# BAD - Never hardcode secrets
OPENAI_API_KEY = "sk-xxxxx"
DATABASE_URL = "postgresql://user:password@localhost/db"

# BAD - Never log secrets
logger.info(f"Using API key: {api_key}")

# BAD - Never commit .env files
# Add to .gitignore:
.env
.env.local
```

**Always:**
```python
# Good - Use environment variables
from app.config import settings

openai_api_key = settings.openai_api_key
database_url = settings.database_url

# Good - Log without secrets
logger.info("Initializing OpenAI client")
logger.info(f"Connecting to database at {database_url.split('@')[1]}")
```


## MVP-Specific Guidelines

### Keep It Simple

**Avoid Over-Engineering:**
```python
# Good for MVP - Simple, direct
class ResumeService:
    def __init__(self, repository, ai_client):
        self.repository = repository
        self.ai_client = ai_client
    
    async def parse_resume(self, content: str) -> ResumeData:
        parsed = await self.ai_client.parse(content)
        return ResumeData(**parsed)

# Avoid for MVP - Over-abstracted
class ResumeService:
    def __init__(self, repository, parser_factory, validator_chain, event_bus):
        self.repository = repository
        self.parser = parser_factory.create_parser()
        self.validators = validator_chain
        self.events = event_bus
    
    async def parse_resume(self, content: str) -> ResumeData:
        parser = self.parser.get_parser_for_content(content)
        parsed = await parser.parse(content)
        validated = await self.validators.validate_all(parsed)
        await self.events.publish(ResumeParseEvent(validated))
        return validated
```

**Prioritize Features:**
```python
# Good for MVP - Core functionality
class ApplicationService:
    async def create_application(self, resume_id, jd_id, user_id):
        # Essential: Create application record
        application = await self.repository.create(resume_id, jd_id, user_id)
        return application

# Skip for MVP - Nice-to-have features
class ApplicationService:
    async def create_application(self, resume_id, jd_id, user_id):
        application = await self.repository.create(resume_id, jd_id, user_id)
        
        # Skip these for MVP:
        # await self.send_confirmation_email(user_id)
        # await self.update_analytics(user_id)
        # await self.notify_team_members(user_id)
        # await self.schedule_follow_up_reminder(application.id)
        
        return application
```

### Technical Debt Management

**Document Intentional Shortcuts:**
```python
# TODO(MVP): Add caching for parsed resumes
# Currently parsing on every request for simplicity
async def get_resume(self, resume_id: str) -> ResumeData:
    resume = await self.repository.get(resume_id)
    return ResumeData(**resume.parsed_data)

# TODO(MVP): Implement retry logic for AI calls
# Currently fails immediately on error
async def parse_resume(self, content: str) -> ResumeData:
    return await self.ai_client.parse(content)

# FIXME(Post-MVP): This is inefficient for large lists
# Consider pagination or virtual scrolling
def get_all_applications(self, user_id: str) -> List[Application]:
    return self.repository.get_all_by_user(user_id)
```

**Track Technical Debt:**
```markdown
# TECHNICAL_DEBT.md

## Known Issues

### High Priority (Post-MVP)
- [ ] Add caching layer for AI responses
- [ ] Implement proper pagination for lists
- [ ] Add retry logic for external API calls

### Medium Priority
- [ ] Optimize database queries (N+1 issues)
- [ ] Add background job processing
- [ ] Implement rate limiting

### Low Priority
- [ ] Refactor service layer for better testability
- [ ] Add more comprehensive error handling
- [ ] Improve logging structure
```


## Code Review Guidelines

### What to Look For

**Functionality:**
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Input validation is present

**Code Quality:**
- [ ] Code is readable and maintainable
- [ ] Functions are small and focused
- [ ] Names are clear and descriptive
- [ ] No unnecessary complexity
- [ ] No code duplication

**Standards Compliance:**
- [ ] Follows naming conventions
- [ ] Follows project structure
- [ ] Uses appropriate patterns
- [ ] Includes necessary documentation
- [ ] Includes tests for critical paths

**Security:**
- [ ] No hardcoded secrets
- [ ] Input is validated and sanitized
- [ ] Authentication/authorization is correct
- [ ] No sensitive data in logs

**Performance:**
- [ ] No obvious performance issues
- [ ] Database queries are efficient
- [ ] No unnecessary API calls
- [ ] Appropriate caching where needed

### Giving Feedback

**Good Feedback:**
```
❌ "This is wrong"
✅ "Consider using a more descriptive variable name here. 
   'parsed_resume_data' would be clearer than 'data'."

❌ "Bad code"
✅ "This function is doing too much. Consider extracting the 
   validation logic into a separate function for better testability."

❌ "Why did you do it this way?"
✅ "I see you're using approach X. Have you considered approach Y? 
   It might be more efficient because..."
```

**Be Constructive:**
- Explain the "why" behind suggestions
- Offer alternatives, not just criticism
- Acknowledge good code
- Ask questions instead of making demands
- Focus on the code, not the person

### Receiving Feedback

**Good Practices:**
- Don't take feedback personally
- Ask for clarification if needed
- Explain your reasoning if questioned
- Be open to learning
- Thank reviewers for their time


## Summary

This coding standards document establishes conventions and best practices for the AI Job Application Copilot project. The goal is to maintain clean, readable, and maintainable code that a solo developer can work with effectively.

### Key Principles Recap

1. **Clarity Over Cleverness** - Write code that's easy to understand
2. **Simplicity Over Abstraction** - Don't over-engineer for the MVP
3. **Consistency Over Preference** - Follow established patterns
4. **Maintainability Over Performance** - Optimize only when needed
5. **Safety Over Speed** - Validate inputs, handle errors

### Essential Standards

**Naming:**
- Python: snake_case for functions/variables, PascalCase for classes
- TypeScript: camelCase for functions/variables, PascalCase for components
- Be descriptive and meaningful

**Structure:**
- Backend: Service layer pattern (routers → services → repositories)
- Frontend: Component-based with clear separation (UI, features, API)
- Keep modules small and focused

**API Design:**
- RESTful conventions
- Consistent request/response models
- Clear error responses
- Proper status codes

**Validation:**
- Validate all inputs (files, user data, AI outputs)
- Use Pydantic for backend validation
- Use TypeScript for frontend type safety
- Never trust external data

**Testing:**
- Focus on critical paths for MVP
- Test business logic thoroughly
- Test AI validation rigorously
- 70%+ coverage goal

**Documentation:**
- Docstrings for public functions
- README files for setup
- Inline comments for complex logic
- API documentation via FastAPI

**Security:**
- Never hardcode secrets
- Validate and sanitize inputs
- Verify user ownership
- Use environment variables

### For Solo Developers

- Keep it simple - you'll thank yourself later
- Document your decisions
- Write tests for peace of mind
- Use tools (Black, Prettier, ESLint)
- Track technical debt
- Don't over-engineer for the MVP

---

**Document Version:** 1.0  
**Last Updated:** April 1, 2026  
**Maintained By:** Development Team  
**Review Frequency:** As needed or when patterns emerge
