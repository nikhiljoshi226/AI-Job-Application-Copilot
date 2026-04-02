# Resume Ingestion Module - Design Specification

## Architecture Overview

The Resume Ingestion module follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Resume Input │  │ Resume List  │  │Resume Detail │ │
│  │    Page      │  │    Page      │  │    Page      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
                          │ REST API
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Resume Router                       │   │
│  │  POST /upload-text  POST /upload-docx           │   │
│  │  GET /resumes  GET /resumes/{id}  DELETE /{id}  │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Resume Ingestion Service                 │   │
│  │  - Orchestrates parsing workflow                │   │
│  │  - Coordinates between components                │   │
│  └─────────────────────────────────────────────────┘   │
│           │              │              │                │
│           ▼              ▼              ▼                │
│  ┌──────────────┐ ┌─────────────┐ ┌─────────────┐     │
│  │   Resume     │ │  Truth Bank │ │   Storage   │     │
│  │   Parser     │ │   Builder   │ │   Client    │     │
│  └──────────────┘ └─────────────┘ └─────────────┘     │
│           │              │              │                │
│           ▼              ▼              ▼                │
│  ┌──────────────┐ ┌─────────────┐ ┌─────────────┐     │
│  │  AI Client   │ │ Validation  │ │  Supabase   │     │
│  │  (OpenAI)    │ │   Engine    │ │  Storage    │     │
│  └──────────────┘ └─────────────┘ └─────────────┘     │
│                          │                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Resume Repository                      │   │
│  │  - Database operations                           │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌──────────────────────┐
              │  PostgreSQL Database │
              │  - resumes table     │
              └──────────────────────┘
```

## Component Design

### 1. Resume Ingestion Service

**Purpose:** Orchestrates the entire resume ingestion workflow

**Responsibilities:**
- Accept resume input (text or DOCX)
- Coordinate text extraction (for DOCX)
- Coordinate parsing
- Coordinate truth bank creation
- Coordinate validation
- Coordinate storage
- Handle errors and retries

**Interface:**
```python
class ResumeIngestionService:
    def __init__(
        self,
        parser: ResumeParser,
        truth_bank_builder: TruthBankBuilder,
        storage_client: StorageClient,
        repository: ResumeRepository,
        docx_extractor: DocxTextExtractor
    ):
        self.parser = parser
        self.truth_bank_builder = truth_bank_builder
        self.storage = storage_client
        self.repository = repository
        self.docx_extractor = docx_extractor
    
    async def ingest_from_text(
        self, 
        text: str, 
        name: str, 
        user_id: str
    ) -> Resume:
        """Ingest resume from pasted text."""
        pass
    
    async def ingest_from_docx(
        self, 
        file: UploadFile, 
        name: str, 
        user_id: str
    ) -> Resume:
        """Ingest resume from DOCX file."""
        pass
    
    async def get_resume(self, resume_id: str, user_id: str) -> Resume:
        """Get resume by ID with authorization check."""
        pass
    
    async def list_resumes(self, user_id: str) -> List[Resume]:
        """List all resumes for user."""
        pass
    
    async def delete_resume(self, resume_id: str, user_id: str) -> None:
        """Delete resume and associated files."""
        pass
```

**Workflow:**
```
1. Receive input (text or DOCX)
2. If DOCX: Extract text using DocxTextExtractor
3. Validate text (length, content)
4. Parse text using ResumeParser
5. Validate parsed data against schema
6. Build truth bank using TruthBankBuilder
7. Validate truth bank
8. If DOCX: Upload file to storage
9. Save to database via repository
10. Return resume object
```



### 2. Resume Parser

**Purpose:** Parse raw resume text into structured JSON using AI

**Responsibilities:**
- Send resume text to OpenAI API
- Use function calling for structured output
- Validate AI response
- Handle parsing failures
- Retry on transient errors

**Interface:**
```python
class ResumeParser:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
    
    async def parse(self, text: str) -> ResumeData:
        """
        Parse resume text into structured data.
        
        Args:
            text: Raw resume text
            
        Returns:
            ResumeData: Validated structured resume data
            
        Raises:
            ValidationError: If parsing output doesn't match schema
            AIError: If AI service fails after retries
        """
        pass
    
    def _build_parsing_prompt(self, text: str) -> List[dict]:
        """Build messages for OpenAI API."""
        pass
    
    def _get_parsing_function_schema(self) -> dict:
        """Get JSON schema for function calling."""
        pass
    
    def _validate_parsed_data(self, data: dict) -> ResumeData:
        """Validate parsed data against Pydantic model."""
        pass
```

**AI Prompt Design:**
```python
SYSTEM_PROMPT = """You are a resume parsing assistant. Extract structured information from resumes.

CRITICAL RULES:
1. Extract ONLY information explicitly stated in the resume
2. NEVER fabricate or infer information
3. If a field is not present, use null
4. Preserve exact wording from resume in bullets
5. Extract all skills mentioned anywhere in resume
6. Categorize skills appropriately
7. Parse dates in various formats or leave as string

OUTPUT FORMAT:
Use the provided function schema to return structured JSON."""

USER_PROMPT_TEMPLATE = """Parse the following resume into structured JSON:

{resume_text}

Extract:
- Contact information (name, email, phone, location, links)
- Professional summary (if present)
- Work experience (company, title, dates, location, bullets)
- Education (institution, degree, field, dates, GPA, achievements)
- Skills (categorized by type)
- Projects (name, description, technologies, bullets, URL)
- Certifications (name, issuer, date)

Remember: Extract only what is explicitly stated. Do not fabricate."""
```

**Function Schema:**
```json
{
  "name": "parse_resume",
  "description": "Extract structured data from resume text",
  "parameters": {
    "type": "object",
    "required": ["contact", "experience", "education", "skills"],
    "properties": {
      "contact": {
        "type": "object",
        "required": ["name", "email"],
        "properties": {
          "name": {"type": "string"},
          "email": {"type": "string"},
          "phone": {"type": ["string", "null"]},
          "location": {"type": ["string", "null"]},
          "linkedin": {"type": ["string", "null"]},
          "github": {"type": ["string", "null"]},
          "portfolio": {"type": ["string", "null"]}
        }
      },
      "summary": {"type": ["string", "null"]},
      "experience": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["company", "title", "bullets"],
          "properties": {
            "company": {"type": "string"},
            "title": {"type": "string"},
            "start_date": {"type": ["string", "null"]},
            "end_date": {"type": ["string", "null"]},
            "location": {"type": ["string", "null"]},
            "bullets": {
              "type": "array",
              "items": {"type": "string"},
              "minItems": 1
            }
          }
        }
      },
      "education": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["institution", "degree"],
          "properties": {
            "institution": {"type": "string"},
            "degree": {"type": "string"},
            "field": {"type": ["string", "null"]},
            "start_date": {"type": ["string", "null"]},
            "end_date": {"type": ["string", "null"]},
            "gpa": {"type": ["string", "null"]},
            "achievements": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        }
      },
      "skills": {
        "type": "object",
        "properties": {
          "languages": {"type": "array", "items": {"type": "string"}},
          "frameworks": {"type": "array", "items": {"type": "string"}},
          "tools": {"type": "array", "items": {"type": "string"}},
          "other": {"type": "array", "items": {"type": "string"}}
        }
      },
      "projects": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["name", "description"],
          "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "technologies": {"type": "array", "items": {"type": "string"}},
            "bullets": {"type": "array", "items": {"type": "string"}},
            "url": {"type": ["string", "null"]}
          }
        }
      },
      "certifications": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["name"],
          "properties": {
            "name": {"type": "string"},
            "issuer": {"type": ["string", "null"]},
            "date": {"type": ["string", "null"]}
          }
        }
      }
    }
  }
}
```

### 3. Truth Bank Builder

**Purpose:** Extract verifiable facts from parsed resume data

**Responsibilities:**
- Extract all factual claims
- Categorize facts by type
- Link facts to source sections
- Deduplicate facts
- Build queryable structure

**Interface:**
```python
class TruthBankBuilder:
    def build(self, parsed_data: ResumeData, raw_text: str) -> TruthBank:
        """
        Build truth bank from parsed resume data.
        
        Args:
            parsed_data: Validated parsed resume data
            raw_text: Original resume text for source linking
            
        Returns:
            TruthBank: Structured collection of verifiable facts
        """
        pass
    
    def _extract_skills(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract all skills as facts."""
        pass
    
    def _extract_technologies(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract all technologies/tools as facts."""
        pass
    
    def _extract_companies(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract all companies worked at."""
        pass
    
    def _extract_titles(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract all job titles held."""
        pass
    
    def _extract_projects(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract all projects completed."""
        pass
    
    def _extract_degrees(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract all degrees earned."""
        pass
    
    def _extract_certifications(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract all certifications obtained."""
        pass
    
    def _extract_achievements(self, parsed_data: ResumeData) -> List[Fact]:
        """Extract quantifiable achievements."""
        pass
    
    def _deduplicate_facts(self, facts: List[Fact]) -> List[Fact]:
        """Remove duplicate facts."""
        pass
    
    def _link_to_source(self, fact: Fact, raw_text: str) -> Fact:
        """Link fact to its location in original text."""
        pass
```

**Truth Bank Structure:**
```python
class Fact(BaseModel):
    """A verifiable fact from the resume."""
    id: str  # Unique identifier
    type: str  # skill, technology, company, title, project, degree, certification, achievement
    value: str  # The fact itself
    category: Optional[str]  # Sub-category if applicable
    source_section: str  # experience, education, skills, projects, certifications
    source_text: Optional[str]  # Exact text from resume
    confidence: str  # high, medium, low
    metadata: dict  # Additional context

class TruthBank(BaseModel):
    """Collection of verifiable facts from resume."""
    facts: List[Fact]
    skills: List[str]  # Quick access to all skills
    technologies: List[str]  # Quick access to all technologies
    companies: List[str]  # Quick access to all companies
    titles: List[str]  # Quick access to all titles
    projects: List[str]  # Quick access to all projects
    degrees: List[str]  # Quick access to all degrees
    certifications: List[str]  # Quick access to all certifications
    created_at: datetime
    version: str  # Truth bank schema version
```

**Example Truth Bank:**
```json
{
  "facts": [
    {
      "id": "fact_001",
      "type": "skill",
      "value": "Python",
      "category": "programming_language",
      "source_section": "skills",
      "source_text": "Python",
      "confidence": "high",
      "metadata": {}
    },
    {
      "id": "fact_002",
      "type": "technology",
      "value": "FastAPI",
      "category": "framework",
      "source_section": "experience",
      "source_text": "Built REST API with FastAPI",
      "confidence": "high",
      "metadata": {"context": "work_experience"}
    },
    {
      "id": "fact_003",
      "type": "company",
      "value": "Tech Corp",
      "category": null,
      "source_section": "experience",
      "source_text": "Software Engineer at Tech Corp",
      "confidence": "high",
      "metadata": {"duration": "2 years"}
    }
  ],
  "skills": ["Python", "JavaScript", "React"],
  "technologies": ["FastAPI", "PostgreSQL", "Docker"],
  "companies": ["Tech Corp", "Startup Inc"],
  "titles": ["Software Engineer", "Junior Developer"],
  "projects": ["E-commerce Platform", "Data Pipeline"],
  "degrees": ["Bachelor of Science in Computer Science"],
  "certifications": ["AWS Certified Developer"],
  "created_at": "2026-04-01T10:00:00Z",
  "version": "1.0"
}
```



### 4. DOCX Text Extractor

**Purpose:** Extract text content from DOCX files

**Responsibilities:**
- Read DOCX file
- Extract text preserving structure
- Handle corrupted files
- Preserve paragraphs and bullets

**Interface:**
```python
class DocxTextExtractor:
    def extract(self, file: UploadFile) -> str:
        """
        Extract text from DOCX file.
        
        Args:
            file: Uploaded DOCX file
            
        Returns:
            str: Extracted text with preserved structure
            
        Raises:
            ValueError: If file is corrupted or not valid DOCX
        """
        pass
    
    def _read_paragraphs(self, doc: Document) -> List[str]:
        """Read all paragraphs from document."""
        pass
    
    def _preserve_structure(self, paragraphs: List[str]) -> str:
        """Preserve paragraph breaks and bullets."""
        pass
```

**Implementation:**
```python
from docx import Document
from io import BytesIO

class DocxTextExtractor:
    def extract(self, file: UploadFile) -> str:
        try:
            # Read file content
            content = file.file.read()
            
            # Parse DOCX
            doc = Document(BytesIO(content))
            
            # Extract paragraphs
            paragraphs = self._read_paragraphs(doc)
            
            # Preserve structure
            text = self._preserve_structure(paragraphs)
            
            return text
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
    
    def _read_paragraphs(self, doc: Document) -> List[str]:
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)
        return paragraphs
    
    def _preserve_structure(self, paragraphs: List[str]) -> str:
        # Join with double newline to preserve paragraph breaks
        return "\n\n".join(paragraphs)
```

### 5. Storage Client

**Purpose:** Handle file uploads to Supabase Storage

**Responsibilities:**
- Upload DOCX files
- Generate file URLs
- Delete files
- Handle upload failures

**Interface:**
```python
class StorageClient:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.bucket = "resumes"
    
    async def upload_resume(
        self, 
        file: UploadFile, 
        user_id: str, 
        resume_id: str
    ) -> str:
        """
        Upload resume file to storage.
        
        Args:
            file: DOCX file to upload
            user_id: User ID for folder organization
            resume_id: Resume ID for filename
            
        Returns:
            str: Public URL of uploaded file
            
        Raises:
            StorageError: If upload fails
        """
        pass
    
    async def delete_resume(self, file_url: str) -> None:
        """Delete resume file from storage."""
        pass
    
    def _generate_file_path(self, user_id: str, resume_id: str) -> str:
        """Generate storage path: {user_id}/resumes/{resume_id}.docx"""
        pass
```

### 6. Resume Repository

**Purpose:** Handle database operations for resumes

**Responsibilities:**
- Create resume records
- Retrieve resumes
- Update resumes
- Delete resumes
- Query resumes by user

**Interface:**
```python
class ResumeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    async def create(
        self,
        user_id: str,
        name: str,
        raw_text: str,
        parsed_data: dict,
        truth_bank: dict,
        file_url: Optional[str] = None
    ) -> Resume:
        """Create new resume record."""
        pass
    
    async def get_by_id(self, resume_id: str) -> Optional[Resume]:
        """Get resume by ID."""
        pass
    
    async def get_by_user(self, user_id: str) -> List[Resume]:
        """Get all resumes for user."""
        pass
    
    async def delete(self, resume_id: str) -> None:
        """Delete resume record."""
        pass
    
    async def update(
        self,
        resume_id: str,
        parsed_data: dict,
        truth_bank: dict
    ) -> Resume:
        """Update resume data (for future editing feature)."""
        pass
```

## Data Models

### Database Schema

**resumes table:**
```sql
CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    raw_text TEXT NOT NULL,
    parsed_data JSONB NOT NULL,
    truth_bank JSONB NOT NULL,
    original_file_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_created_at ON resumes(created_at DESC);

-- Enable Row Level Security
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their own resumes
CREATE POLICY resumes_user_policy ON resumes
    FOR ALL
    USING (auth.uid() = user_id);
```

### Pydantic Models

**Contact Information:**
```python
class ContactInfo(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None
```

**Experience:**
```python
class Experience(BaseModel):
    company: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    start_date: Optional[str] = Field(None, max_length=50)
    end_date: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    bullets: List[str] = Field(..., min_items=1)
    
    @validator('bullets')
    def validate_bullets(cls, v):
        if not v:
            raise ValueError('At least one bullet point required')
        if any(len(b.strip()) < 10 for b in v):
            raise ValueError('Bullet points must be at least 10 characters')
        return v
```

**Education:**
```python
class Education(BaseModel):
    institution: str = Field(..., min_length=1, max_length=255)
    degree: str = Field(..., min_length=1, max_length=255)
    field: Optional[str] = Field(None, max_length=255)
    start_date: Optional[str] = Field(None, max_length=50)
    end_date: Optional[str] = Field(None, max_length=50)
    gpa: Optional[str] = Field(None, max_length=20)
    achievements: List[str] = []
```

**Skills:**
```python
class Skills(BaseModel):
    languages: List[str] = []
    frameworks: List[str] = []
    tools: List[str] = []
    other: List[str] = []
    
    @validator('languages', 'frameworks', 'tools', 'other')
    def validate_not_empty_strings(cls, v):
        return [s.strip() for s in v if s.strip()]
```

**Project:**
```python
class Project(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    technologies: List[str] = []
    bullets: List[str] = []
    url: Optional[HttpUrl] = None
```

**Certification:**
```python
class Certification(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    issuer: Optional[str] = Field(None, max_length=255)
    date: Optional[str] = Field(None, max_length=50)
```

**Resume Data:**
```python
class ResumeData(BaseModel):
    contact: ContactInfo
    summary: Optional[str] = Field(None, max_length=2000)
    experience: List[Experience] = []
    education: List[Education] = []
    skills: Skills
    projects: List[Project] = []
    certifications: List[Certification] = []
    
    @validator('experience', 'education')
    def validate_has_experience_or_education(cls, v, values):
        # At least one of experience or education must be present
        if 'experience' in values and not values['experience'] and not v:
            raise ValueError('Must have at least one experience or education entry')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "contact": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1-555-0100",
                    "location": "San Francisco, CA",
                    "linkedin": "https://linkedin.com/in/johndoe",
                    "github": "https://github.com/johndoe"
                },
                "summary": "Software engineer with 3 years of experience...",
                "experience": [
                    {
                        "company": "Tech Corp",
                        "title": "Software Engineer",
                        "start_date": "Jan 2021",
                        "end_date": "Present",
                        "location": "San Francisco, CA",
                        "bullets": [
                            "Built REST API with FastAPI",
                            "Improved performance by 40%"
                        ]
                    }
                ],
                "education": [
                    {
                        "institution": "University of California",
                        "degree": "Bachelor of Science",
                        "field": "Computer Science",
                        "end_date": "2020",
                        "gpa": "3.8"
                    }
                ],
                "skills": {
                    "languages": ["Python", "JavaScript"],
                    "frameworks": ["FastAPI", "React"],
                    "tools": ["Docker", "PostgreSQL"]
                }
            }
        }
```

**Resume (Database Model):**
```python
class Resume(BaseModel):
    id: str
    user_id: str
    name: str
    raw_text: str
    parsed_data: ResumeData
    truth_bank: TruthBank
    original_file_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```



## API Endpoints

### POST /api/resumes/upload-text

**Description:** Upload resume from pasted text

**Request:**
```typescript
{
  "text": "string (min 100 chars, max 10000 chars)",
  "name": "string (min 1 char, max 255 chars)"
}
```

**Response (201 Created):**
```typescript
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "raw_text": "string",
  "parsed_data": ResumeData,
  "truth_bank": TruthBank,
  "original_file_url": null,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**Errors:**
- 400: Invalid input (text too short, name missing)
- 401: Unauthorized
- 422: Parsing failed
- 500: Internal server error

### POST /api/resumes/upload-docx

**Description:** Upload resume from DOCX file

**Request:** multipart/form-data
- file: DOCX file (max 5MB)
- name: string (resume name)

**Response (201 Created):**
```typescript
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "raw_text": "string (extracted)",
  "parsed_data": ResumeData,
  "truth_bank": TruthBank,
  "original_file_url": "string (storage URL)",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**Errors:**
- 400: Invalid file (wrong type, too large, corrupted)
- 401: Unauthorized
- 422: Parsing failed
- 500: Internal server error

### GET /api/resumes

**Description:** List all resumes for authenticated user

**Response (200 OK):**
```typescript
{
  "resumes": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "name": "string",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  ],
  "total": number
}
```

**Errors:**
- 401: Unauthorized

### GET /api/resumes/{id}

**Description:** Get resume by ID

**Response (200 OK):**
```typescript
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "string",
  "raw_text": "string",
  "parsed_data": ResumeData,
  "truth_bank": TruthBank,
  "original_file_url": "string | null",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**Errors:**
- 401: Unauthorized
- 403: Forbidden (not user's resume)
- 404: Not found

### DELETE /api/resumes/{id}

**Description:** Delete resume and associated files

**Response (204 No Content)**

**Errors:**
- 401: Unauthorized
- 403: Forbidden (not user's resume)
- 404: Not found

## Validation Rules

### Input Validation

**Text Input:**
```python
def validate_text_input(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("Resume text cannot be empty")
    
    if len(text.strip()) < 100:
        raise ValueError("Resume text must be at least 100 characters")
    
    if len(text) > 10000:
        raise ValueError("Resume text cannot exceed 10,000 characters")
```

**DOCX File:**
```python
def validate_docx_file(file: UploadFile) -> None:
    # Check file extension
    if not file.filename.lower().endswith('.docx'):
        raise ValueError("File must be a DOCX document")
    
    # Check MIME type
    if file.content_type not in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        raise ValueError("Invalid file type. Must be DOCX")
    
    # Check file size
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise ValueError("File size cannot exceed 5MB")
    
    # Check file is not empty
    if file.size == 0:
        raise ValueError("File is empty")
```

**Resume Name:**
```python
def validate_resume_name(name: str) -> None:
    if not name or not name.strip():
        raise ValueError("Resume name cannot be empty")
    
    if len(name.strip()) > 255:
        raise ValueError("Resume name cannot exceed 255 characters")
```

### Parsing Validation

**Contact Information:**
```python
def validate_contact(contact: dict) -> None:
    if not contact.get('name'):
        raise ValueError("Name is required")
    
    if not contact.get('email'):
        raise ValueError("Email is required")
    
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, contact['email']):
        raise ValueError("Invalid email format")
    
    # Validate URLs if present
    for url_field in ['linkedin', 'github', 'portfolio']:
        if contact.get(url_field):
            if not contact[url_field].startswith(('http://', 'https://')):
                raise ValueError(f"Invalid {url_field} URL format")
```

**Experience:**
```python
def validate_experience(experience: List[dict]) -> None:
    for exp in experience:
        if not exp.get('company'):
            raise ValueError("Company name is required for experience")
        
        if not exp.get('title'):
            raise ValueError("Job title is required for experience")
        
        if not exp.get('bullets') or len(exp['bullets']) == 0:
            raise ValueError("At least one bullet point required for experience")
        
        for bullet in exp['bullets']:
            if len(bullet.strip()) < 10:
                raise ValueError("Bullet points must be at least 10 characters")
```

**Education:**
```python
def validate_education(education: List[dict]) -> None:
    for edu in education:
        if not edu.get('institution'):
            raise ValueError("Institution name is required for education")
        
        if not edu.get('degree'):
            raise ValueError("Degree is required for education")
```

**Skills:**
```python
def validate_skills(skills: dict) -> None:
    # At least one skill category must have values
    has_skills = any([
        skills.get('languages'),
        skills.get('frameworks'),
        skills.get('tools'),
        skills.get('other')
    ])
    
    if not has_skills:
        raise ValueError("At least one skill must be present")
    
    # Remove empty strings
    for category in ['languages', 'frameworks', 'tools', 'other']:
        if skills.get(category):
            skills[category] = [s.strip() for s in skills[category] if s.strip()]
```

**Overall Resume:**
```python
def validate_resume_data(data: dict) -> None:
    # Must have contact info
    if not data.get('contact'):
        raise ValueError("Contact information is required")
    
    validate_contact(data['contact'])
    
    # Must have at least experience or education
    has_experience = data.get('experience') and len(data['experience']) > 0
    has_education = data.get('education') and len(data['education']) > 0
    
    if not has_experience and not has_education:
        raise ValueError("Resume must have at least one experience or education entry")
    
    # Validate sections if present
    if has_experience:
        validate_experience(data['experience'])
    
    if has_education:
        validate_education(data['education'])
    
    # Skills are required
    if not data.get('skills'):
        raise ValueError("Skills section is required")
    
    validate_skills(data['skills'])
```

### Truth Bank Validation

```python
def validate_truth_bank(truth_bank: dict, parsed_data: dict) -> None:
    """Ensure truth bank facts are derived from parsed data."""
    
    # Check all skills in truth bank exist in parsed data
    parsed_skills = set()
    for category in parsed_data['skills'].values():
        parsed_skills.update(category)
    
    for skill in truth_bank.get('skills', []):
        if skill not in parsed_skills:
            raise ValueError(f"Truth bank skill '{skill}' not found in parsed data")
    
    # Check all companies in truth bank exist in experience
    parsed_companies = {exp['company'] for exp in parsed_data.get('experience', [])}
    for company in truth_bank.get('companies', []):
        if company not in parsed_companies:
            raise ValueError(f"Truth bank company '{company}' not found in parsed data")
    
    # Similar checks for other fact types...
```

## Frontend Design

### Pages

**1. Resume Input Page (`/resumes/new`)**

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Add New Resume                                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ [Paste Text] [Upload DOCX]                          │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Resume Name                                          │ │
│ │ [Input field]                                        │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Paste Text Tab:                                      │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │                                                   │ │ │
│ │ │  [Large textarea for resume text]                │ │ │
│ │ │                                                   │ │ │
│ │ │  Character count: 0 / 10,000                     │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ │                                                      │ │
│ │ [Parse Resume]                                       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ OR                                                       │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Upload DOCX Tab:                                     │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │                                                   │ │ │
│ │ │  Drop DOCX file here or click to browse          │ │ │
│ │ │                                                   │ │ │
│ │ │  Supported: .docx (max 5MB)                      │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ │                                                      │ │
│ │ [Upload and Parse]                                   │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Components:**
- TabSelector (Paste Text / Upload DOCX)
- TextInput (resume name)
- Textarea (for text paste)
- FileDropZone (for DOCX upload)
- Button (Parse/Upload)
- CharacterCount
- ValidationMessage

**State:**
```typescript
interface ResumeInputState {
  activeTab: 'text' | 'docx';
  resumeName: string;
  resumeText: string;
  selectedFile: File | null;
  isUploading: boolean;
  isParsing: boolean;
  error: string | null;
}
```

**2. Parsing Progress Page**

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Parsing Your Resume                                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│              [Spinner Animation]                         │
│                                                          │
│         Analyzing your resume...                         │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ✓ Text extracted                                     │ │
│ │ ⏳ Parsing sections...                               │ │
│ │ ⏳ Building truth bank...                            │ │
│ │ ⏳ Validating data...                                │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│         This may take 10-15 seconds                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Components:**
- LoadingSpinner
- ProgressSteps
- StatusMessage

**3. Parsed Data Review Page**

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Review Parsed Resume                    [Edit] [Delete] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Contact Information                                  │ │
│ │ Name: John Doe                                       │ │
│ │ Email: john@example.com                              │ │
│ │ Phone: +1-555-0100                                   │ │
│ │ Location: San Francisco, CA                          │ │
│ │ LinkedIn: linkedin.com/in/johndoe                    │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Professional Summary                                 │ │
│ │ Software engineer with 3 years of experience...      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Work Experience (2 entries)                          │ │
│ │                                                      │ │
│ │ Software Engineer at Tech Corp                       │ │
│ │ Jan 2021 - Present | San Francisco, CA               │ │
│ │ • Built REST API with FastAPI                        │ │
│ │ • Improved performance by 40%                        │ │
│ │                                                      │ │
│ │ Junior Developer at Startup Inc                      │ │
│ │ Jun 2020 - Dec 2020 | Remote                         │ │
│ │ • Developed frontend with React                      │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Education (1 entry)                                  │ │
│ │ Bachelor of Science in Computer Science              │ │
│ │ University of California | 2020 | GPA: 3.8           │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Skills                                               │ │
│ │ Languages: Python, JavaScript, TypeScript            │ │
│ │ Frameworks: FastAPI, React, Next.js                  │ │
│ │ Tools: Docker, PostgreSQL, Git                       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                          │
│ [Looks Good - Save Resume] [Re-parse]                    │
└─────────────────────────────────────────────────────────┘
```

**Components:**
- SectionCard (for each resume section)
- ContactDisplay
- ExperienceDisplay
- EducationDisplay
- SkillsDisplay
- ProjectsDisplay (if present)
- CertificationsDisplay (if present)
- Button (Save, Re-parse)

**State:**
```typescript
interface ParsedResumeState {
  resume: Resume;
  isSaving: boolean;
  error: string | null;
}
```

**4. Resume List Page (`/resumes`)**

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ My Resumes                              [+ Add New]      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│ │ Software     │  │ Data Science │  │ Product      │  │
│ │ Engineer     │  │ Resume       │  │ Manager      │  │
│ │ Resume       │  │              │  │ Resume       │  │
│ │              │  │ Created:     │  │              │  │
│ │ Created:     │  │ Mar 15, 2026 │  │ Created:     │  │
│ │ Apr 1, 2026  │  │              │  │ Feb 20, 2026 │  │
│ │              │  │ [View]       │  │              │  │
│ │ [View]       │  │ [Delete]     │  │ [View]       │  │
│ │ [Delete]     │  │              │  │ [Delete]     │  │
│ └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Components:**
- ResumeCard (grid layout)
- Button (Add New, View, Delete)
- EmptyState (if no resumes)

**State:**
```typescript
interface ResumeListState {
  resumes: Resume[];
  isLoading: boolean;
  error: string | null;
}
```

**5. Resume Detail Page (`/resumes/[id]`)**

Similar to Parsed Data Review Page, but read-only with actions:
- Use for Application
- Download Original (if DOCX)
- Delete



## Test Strategy

### Unit Tests

**Resume Parser Tests:**
```python
# tests/test_services/test_resume_parser.py

def test_parse_resume_success(mock_ai_client, sample_resume_text):
    """Test successful resume parsing."""
    parser = ResumeParser(mock_ai_client)
    result = parser.parse(sample_resume_text)
    
    assert isinstance(result, ResumeData)
    assert result.contact.name == "John Doe"
    assert result.contact.email == "john@example.com"
    assert len(result.experience) > 0

def test_parse_resume_validates_schema(mock_ai_client):
    """Test that invalid AI output is rejected."""
    mock_ai_client.parse_resume.return_value = {
        "contact": {}  # Missing required fields
    }
    
    parser = ResumeParser(mock_ai_client)
    
    with pytest.raises(ValidationError):
        parser.parse("resume text")

def test_parse_resume_requires_name_and_email(mock_ai_client):
    """Test that name and email are required."""
    mock_ai_client.parse_resume.return_value = {
        "contact": {"name": "John Doe"},  # Missing email
        "experience": [],
        "education": [],
        "skills": {}
    }
    
    parser = ResumeParser(mock_ai_client)
    
    with pytest.raises(ValidationError, match="email"):
        parser.parse("resume text")

def test_parse_resume_requires_experience_or_education(mock_ai_client):
    """Test that at least one of experience or education is required."""
    mock_ai_client.parse_resume.return_value = {
        "contact": {"name": "John Doe", "email": "john@example.com"},
        "experience": [],
        "education": [],
        "skills": {"languages": ["Python"]}
    }
    
    parser = ResumeParser(mock_ai_client)
    
    with pytest.raises(ValidationError, match="experience or education"):
        parser.parse("resume text")

def test_parse_resume_validates_email_format(mock_ai_client):
    """Test that email format is validated."""
    mock_ai_client.parse_resume.return_value = {
        "contact": {"name": "John Doe", "email": "invalid-email"},
        "experience": [{"company": "Tech Corp", "title": "Engineer", "bullets": ["test"]}],
        "skills": {"languages": ["Python"]}
    }
    
    parser = ResumeParser(mock_ai_client)
    
    with pytest.raises(ValidationError, match="email"):
        parser.parse("resume text")
```

**Truth Bank Builder Tests:**
```python
# tests/test_services/test_truth_bank_builder.py

def test_build_truth_bank_extracts_skills(sample_parsed_data):
    """Test that all skills are extracted."""
    builder = TruthBankBuilder()
    truth_bank = builder.build(sample_parsed_data, "raw text")
    
    assert "Python" in truth_bank.skills
    assert "JavaScript" in truth_bank.skills
    assert len(truth_bank.skills) == len(set(truth_bank.skills))  # No duplicates

def test_build_truth_bank_extracts_companies(sample_parsed_data):
    """Test that all companies are extracted."""
    builder = TruthBankBuilder()
    truth_bank = builder.build(sample_parsed_data, "raw text")
    
    assert "Tech Corp" in truth_bank.companies
    assert len(truth_bank.companies) > 0

def test_build_truth_bank_links_facts_to_source(sample_parsed_data):
    """Test that facts are linked to source sections."""
    builder = TruthBankBuilder()
    truth_bank = builder.build(sample_parsed_data, "raw text")
    
    skill_facts = [f for f in truth_bank.facts if f.type == "skill"]
    for fact in skill_facts:
        assert fact.source_section in ["skills", "experience", "projects"]
        assert fact.source_text is not None

def test_build_truth_bank_deduplicates_facts(sample_parsed_data):
    """Test that duplicate facts are removed."""
    # Add duplicate skill in different sections
    sample_parsed_data.skills.languages.append("Python")  # Already in skills
    
    builder = TruthBankBuilder()
    truth_bank = builder.build(sample_parsed_data, "raw text")
    
    python_facts = [f for f in truth_bank.facts if f.value == "Python"]
    assert len(python_facts) == 1  # Only one fact for Python
```

**DOCX Extractor Tests:**
```python
# tests/test_utils/test_docx_extractor.py

def test_extract_text_from_valid_docx(sample_docx_file):
    """Test text extraction from valid DOCX."""
    extractor = DocxTextExtractor()
    text = extractor.extract(sample_docx_file)
    
    assert len(text) > 0
    assert "John Doe" in text

def test_extract_text_preserves_structure(sample_docx_file):
    """Test that paragraph structure is preserved."""
    extractor = DocxTextExtractor()
    text = extractor.extract(sample_docx_file)
    
    # Should have paragraph breaks
    assert "\n\n" in text

def test_extract_text_handles_corrupted_file(corrupted_docx_file):
    """Test handling of corrupted DOCX files."""
    extractor = DocxTextExtractor()
    
    with pytest.raises(ValueError, match="Failed to extract"):
        extractor.extract(corrupted_docx_file)
```

**Validation Tests:**
```python
# tests/test_validation/test_input_validation.py

def test_validate_text_input_rejects_empty():
    """Test that empty text is rejected."""
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_text_input("")

def test_validate_text_input_rejects_too_short():
    """Test that text shorter than 100 chars is rejected."""
    with pytest.raises(ValueError, match="at least 100 characters"):
        validate_text_input("Short text")

def test_validate_text_input_rejects_too_long():
    """Test that text longer than 10000 chars is rejected."""
    long_text = "a" * 10001
    with pytest.raises(ValueError, match="cannot exceed 10,000"):
        validate_text_input(long_text)

def test_validate_docx_file_rejects_wrong_extension():
    """Test that non-DOCX files are rejected."""
    file = UploadFile(filename="resume.pdf")
    
    with pytest.raises(ValueError, match="must be a DOCX"):
        validate_docx_file(file)

def test_validate_docx_file_rejects_too_large():
    """Test that files larger than 5MB are rejected."""
    file = UploadFile(filename="resume.docx", size=6 * 1024 * 1024)
    
    with pytest.raises(ValueError, match="cannot exceed 5MB"):
        validate_docx_file(file)
```

### Integration Tests

**API Endpoint Tests:**
```python
# tests/test_routers/test_resume_ingestion.py

def test_upload_text_success(client, auth_headers):
    """Test successful text upload."""
    response = client.post(
        "/api/resumes/upload-text",
        json={
            "text": sample_resume_text,
            "name": "Software Engineer Resume"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Software Engineer Resume"
    assert "parsed_data" in data
    assert "truth_bank" in data

def test_upload_text_validates_input(client, auth_headers):
    """Test that invalid input is rejected."""
    response = client.post(
        "/api/resumes/upload-text",
        json={
            "text": "Too short",
            "name": "Resume"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert "at least 100 characters" in response.json()["detail"]

def test_upload_docx_success(client, auth_headers, sample_docx):
    """Test successful DOCX upload."""
    response = client.post(
        "/api/resumes/upload-docx",
        files={"file": ("resume.docx", sample_docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        data={"name": "My Resume"},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["original_file_url"] is not None

def test_get_resumes_returns_user_resumes_only(client, auth_headers, other_user_resume):
    """Test that users only see their own resumes."""
    response = client.get("/api/resumes", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should not include other user's resume
    resume_ids = [r["id"] for r in data["resumes"]]
    assert other_user_resume.id not in resume_ids

def test_delete_resume_removes_file(client, auth_headers, resume_with_file):
    """Test that deleting resume also deletes file."""
    response = client.delete(
        f"/api/resumes/{resume_with_file.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 204
    
    # Verify file is deleted from storage
    assert not storage_client.file_exists(resume_with_file.original_file_url)
```

### End-to-End Tests

**Full Workflow Tests:**
```python
# tests/test_e2e/test_resume_ingestion_flow.py

def test_complete_text_upload_flow(client, auth_headers):
    """Test complete flow from text upload to retrieval."""
    # 1. Upload resume text
    upload_response = client.post(
        "/api/resumes/upload-text",
        json={
            "text": sample_resume_text,
            "name": "Test Resume"
        },
        headers=auth_headers
    )
    assert upload_response.status_code == 201
    resume_id = upload_response.json()["id"]
    
    # 2. Retrieve resume
    get_response = client.get(
        f"/api/resumes/{resume_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 200
    resume = get_response.json()
    
    # 3. Verify parsed data
    assert resume["parsed_data"]["contact"]["name"] == "John Doe"
    assert len(resume["parsed_data"]["experience"]) > 0
    
    # 4. Verify truth bank
    assert len(resume["truth_bank"]["skills"]) > 0
    assert len(resume["truth_bank"]["companies"]) > 0
    
    # 5. Delete resume
    delete_response = client.delete(
        f"/api/resumes/{resume_id}",
        headers=auth_headers
    )
    assert delete_response.status_code == 204
    
    # 6. Verify deleted
    get_after_delete = client.get(
        f"/api/resumes/{resume_id}",
        headers=auth_headers
    )
    assert get_after_delete.status_code == 404
```

### Test Coverage Goals

- Resume Parser: 90%+
- Truth Bank Builder: 85%+
- DOCX Extractor: 80%+
- Validation functions: 95%+
- API endpoints: 85%+
- Overall: 85%+

### Test Data

**Sample Resume Text:**
```
John Doe
john.doe@email.com | +1-555-0100 | San Francisco, CA
linkedin.com/in/johndoe | github.com/johndoe

PROFESSIONAL SUMMARY
Software engineer with 3 years of experience building scalable web applications.

WORK EXPERIENCE

Software Engineer | Tech Corp | Jan 2021 - Present | San Francisco, CA
• Built REST API with FastAPI serving 1M+ requests/day
• Improved application performance by 40% through optimization
• Mentored 2 junior developers

Junior Developer | Startup Inc | Jun 2020 - Dec 2020 | Remote
• Developed frontend features using React and TypeScript
• Implemented responsive design for mobile users

EDUCATION

Bachelor of Science in Computer Science | University of California | 2020
GPA: 3.8/4.0
Dean's List (4 semesters)

SKILLS

Languages: Python, JavaScript, TypeScript, SQL
Frameworks: FastAPI, React, Next.js, Django
Tools: Docker, PostgreSQL, Git, AWS

PROJECTS

E-commerce Platform
• Built full-stack e-commerce site with React and FastAPI
• Integrated Stripe payment processing
• Technologies: React, FastAPI, PostgreSQL, Docker

CERTIFICATIONS

AWS Certified Developer - Associate | Amazon Web Services | 2022
```

