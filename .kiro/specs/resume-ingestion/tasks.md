# Resume Ingestion Module - Implementation Tasks

## Task Breakdown

### Phase 1: Foundation & Database Setup

#### Task 1.1: Database Schema
- [ ] Create resumes table migration
  - [ ] Define table structure with all columns
  - [ ] Add indexes on user_id and created_at
  - [ ] Enable Row Level Security
  - [ ] Create RLS policy for user access
  - [ ] Test migration up and down
- [ ] Create Supabase Storage bucket for resumes
  - [ ] Configure bucket permissions
  - [ ] Set up folder structure (user_id/resumes/)
  - [ ] Test file upload and retrieval

#### Task 1.2: Pydantic Models
- [ ] Create ContactInfo model
  - [ ] Add field validations
  - [ ] Add email format validator
  - [ ] Add URL format validators
- [ ] Create Experience model
  - [ ] Add field validations
  - [ ] Add bullets validator (min 1, min length 10)
- [ ] Create Education model
  - [ ] Add field validations
- [ ] Create Skills model
  - [ ] Add empty string filter validator
- [ ] Create Project model
  - [ ] Add field validations
- [ ] Create Certification model
  - [ ] Add field validations
- [ ] Create ResumeData model
  - [ ] Add all section models
  - [ ] Add cross-field validator (experience or education required)
  - [ ] Add example in schema_extra
- [ ] Create Fact model for truth bank
- [ ] Create TruthBank model
- [ ] Write unit tests for all models

### Phase 2: Core Services

#### Task 2.1: DOCX Text Extractor
- [ ] Create DocxTextExtractor class
  - [ ] Implement extract() method
  - [ ] Implement _read_paragraphs() method
  - [ ] Implement _preserve_structure() method
  - [ ] Add error handling for corrupted files
- [ ] Write unit tests
  - [ ] Test with valid DOCX
  - [ ] Test structure preservation
  - [ ] Test with corrupted file
  - [ ] Test with empty file
- [ ] Create test fixtures (sample DOCX files)

#### Task 2.2: Storage Client
- [ ] Create StorageClient class
  - [ ] Implement upload_resume() method
  - [ ] Implement delete_resume() method
  - [ ] Implement _generate_file_path() method
  - [ ] Add error handling for upload failures
- [ ] Write unit tests
  - [ ] Test successful upload
  - [ ] Test file path generation
  - [ ] Test delete operation
  - [ ] Test upload failure handling
- [ ] Integration test with Supabase Storage

#### Task 2.3: AI Client for Resume Parsing
- [ ] Create or extend AIClient class
  - [ ] Implement parse_resume() method
  - [ ] Implement _build_parsing_prompt() method
  - [ ] Implement _get_parsing_function_schema() method
  - [ ] Add retry logic with exponential backoff
  - [ ] Add token usage tracking
- [ ] Define parsing prompts
  - [ ] Create system prompt with strict rules
  - [ ] Create user prompt template
  - [ ] Test prompt with sample resumes
- [ ] Define function calling schema
  - [ ] Match Pydantic models structure
  - [ ] Add all required and optional fields
  - [ ] Test schema with OpenAI API
- [ ] Write unit tests
  - [ ] Test with mocked OpenAI responses
  - [ ] Test retry logic
  - [ ] Test error handling
- [ ] Integration test with real OpenAI API

#### Task 2.4: Resume Parser
- [ ] Create ResumeParser class
  - [ ] Implement parse() method
  - [ ] Implement _build_parsing_prompt() method
  - [ ] Implement _get_parsing_function_schema() method
  - [ ] Implement _validate_parsed_data() method
  - [ ] Add comprehensive error handling
- [ ] Write unit tests
  - [ ] Test successful parsing
  - [ ] Test validation of AI output
  - [ ] Test required fields validation
  - [ ] Test email format validation
  - [ ] Test experience/education requirement
  - [ ] Test with various resume formats
- [ ] Integration tests with AI client
- [ ] Test with diverse resume samples

#### Task 2.5: Truth Bank Builder
- [ ] Create TruthBankBuilder class
  - [ ] Implement build() method
  - [ ] Implement _extract_skills() method
  - [ ] Implement _extract_technologies() method
  - [ ] Implement _extract_companies() method
  - [ ] Implement _extract_titles() method
  - [ ] Implement _extract_projects() method
  - [ ] Implement _extract_degrees() method
  - [ ] Implement _extract_certifications() method
  - [ ] Implement _extract_achievements() method
  - [ ] Implement _deduplicate_facts() method
  - [ ] Implement _link_to_source() method
- [ ] Write unit tests
  - [ ] Test skill extraction
  - [ ] Test company extraction
  - [ ] Test fact deduplication
  - [ ] Test source linking
  - [ ] Test with various parsed data
- [ ] Integration test with parsed resume data

#### Task 2.6: Resume Repository
- [ ] Create ResumeRepository class
  - [ ] Implement create() method
  - [ ] Implement get_by_id() method
  - [ ] Implement get_by_user() method
  - [ ] Implement delete() method
  - [ ] Implement update() method (for future)
  - [ ] Add proper error handling
- [ ] Write unit tests
  - [ ] Test create operation
  - [ ] Test get operations
  - [ ] Test delete operation
  - [ ] Test with non-existent IDs
- [ ] Integration tests with database

#### Task 2.7: Resume Ingestion Service
- [ ] Create ResumeIngestionService class
  - [ ] Implement ingest_from_text() method
  - [ ] Implement ingest_from_docx() method
  - [ ] Implement get_resume() method with auth check
  - [ ] Implement list_resumes() method
  - [ ] Implement delete_resume() method with file cleanup
  - [ ] Add comprehensive error handling
  - [ ] Add logging for debugging
- [ ] Write unit tests
  - [ ] Test text ingestion workflow
  - [ ] Test DOCX ingestion workflow
  - [ ] Test authorization checks
  - [ ] Test error scenarios
  - [ ] Test file cleanup on delete
- [ ] Integration tests with all dependencies

### Phase 3: API Endpoints

#### Task 3.1: Input Validation Functions
- [ ] Create validate_text_input() function
  - [ ] Check not empty
  - [ ] Check minimum length (100 chars)
  - [ ] Check maximum length (10000 chars)
- [ ] Create validate_docx_file() function
  - [ ] Check file extension
  - [ ] Check MIME type
  - [ ] Check file size (max 5MB)
  - [ ] Check not empty
- [ ] Create validate_resume_name() function
  - [ ] Check not empty
  - [ ] Check maximum length (255 chars)
- [ ] Write unit tests for all validation functions

#### Task 3.2: Resume Router
- [ ] Create resume router file
- [ ] Implement POST /api/resumes/upload-text
  - [ ] Add request model
  - [ ] Add response model
  - [ ] Add authentication dependency
  - [ ] Add input validation
  - [ ] Call ingestion service
  - [ ] Handle errors with proper status codes
  - [ ] Add API documentation
- [ ] Implement POST /api/resumes/upload-docx
  - [ ] Add multipart form handling
  - [ ] Add authentication dependency
  - [ ] Add file validation
  - [ ] Call ingestion service
  - [ ] Handle errors
  - [ ] Add API documentation
- [ ] Implement GET /api/resumes
  - [ ] Add authentication dependency
  - [ ] Call ingestion service
  - [ ] Return list response
  - [ ] Add API documentation
- [ ] Implement GET /api/resumes/{id}
  - [ ] Add authentication dependency
  - [ ] Add authorization check
  - [ ] Call ingestion service
  - [ ] Handle not found
  - [ ] Add API documentation
- [ ] Implement DELETE /api/resumes/{id}
  - [ ] Add authentication dependency
  - [ ] Add authorization check
  - [ ] Call ingestion service
  - [ ] Return 204 on success
  - [ ] Add API documentation
- [ ] Register router in main app

#### Task 3.3: API Integration Tests
- [ ] Test POST /api/resumes/upload-text
  - [ ] Test successful upload
  - [ ] Test with invalid input
  - [ ] Test without authentication
  - [ ] Test parsing failure
- [ ] Test POST /api/resumes/upload-docx
  - [ ] Test successful upload
  - [ ] Test with invalid file
  - [ ] Test with too large file
  - [ ] Test without authentication
- [ ] Test GET /api/resumes
  - [ ] Test returns user's resumes only
  - [ ] Test without authentication
  - [ ] Test empty list
- [ ] Test GET /api/resumes/{id}
  - [ ] Test successful retrieval
  - [ ] Test not found
  - [ ] Test unauthorized access
- [ ] Test DELETE /api/resumes/{id}
  - [ ] Test successful deletion
  - [ ] Test file cleanup
  - [ ] Test not found
  - [ ] Test unauthorized access

### Phase 4: Frontend Implementation

#### Task 4.1: TypeScript Types
- [ ] Create Resume interface
- [ ] Create ResumeData interface
- [ ] Create ContactInfo interface
- [ ] Create Experience interface
- [ ] Create Education interface
- [ ] Create Skills interface
- [ ] Create Project interface
- [ ] Create Certification interface
- [ ] Create TruthBank interface
- [ ] Create Fact interface
- [ ] Create API request/response types

#### Task 4.2: API Client Functions
- [ ] Create uploadResumeText() function
  - [ ] Handle request/response
  - [ ] Handle errors
  - [ ] Add TypeScript types
- [ ] Create uploadResumeDocx() function
  - [ ] Handle multipart form data
  - [ ] Handle errors
  - [ ] Add TypeScript types
- [ ] Create getResumes() function
- [ ] Create getResume() function
- [ ] Create deleteResume() function
- [ ] Add error handling wrapper
- [ ] Add authentication token handling

#### Task 4.3: Custom Hooks
- [ ] Create useResumes() hook
  - [ ] Implement state management
  - [ ] Implement loadResumes()
  - [ ] Implement uploadText()
  - [ ] Implement uploadDocx()
  - [ ] Implement deleteResume()
  - [ ] Add loading and error states
- [ ] Write tests for hook (optional for MVP)

#### Task 4.4: UI Components
- [ ] Create TabSelector component
  - [ ] Support Paste Text / Upload DOCX tabs
  - [ ] Add active state styling
- [ ] Create FileDropZone component
  - [ ] Support drag and drop
  - [ ] Support file picker
  - [ ] Show file requirements
  - [ ] Show selected file info
  - [ ] Add validation feedback
- [ ] Create CharacterCount component
  - [ ] Show current / max characters
  - [ ] Color code based on limits
- [ ] Create LoadingSpinner component
- [ ] Create ProgressSteps component
  - [ ] Show parsing steps
  - [ ] Show completion status
- [ ] Create ResumeCard component
  - [ ] Show resume name and date
  - [ ] Add View and Delete actions
  - [ ] Add hover effects
- [ ] Create ContactDisplay component
- [ ] Create ExperienceDisplay component
- [ ] Create EducationDisplay component
- [ ] Create SkillsDisplay component
- [ ] Create ProjectsDisplay component
- [ ] Create CertificationsDisplay component
- [ ] Create SectionCard component (wrapper)

#### Task 4.5: Resume Input Page
- [ ] Create /resumes/new page
- [ ] Add page layout and header
- [ ] Add TabSelector for input methods
- [ ] Add resume name input field
- [ ] Implement Paste Text tab
  - [ ] Add large textarea
  - [ ] Add character count
  - [ ] Add validation
  - [ ] Add Parse button
- [ ] Implement Upload DOCX tab
  - [ ] Add FileDropZone
  - [ ] Add file validation
  - [ ] Add Upload button
- [ ] Implement parsing progress view
  - [ ] Show loading spinner
  - [ ] Show progress steps
  - [ ] Show status messages
- [ ] Handle parsing success
  - [ ] Navigate to review page
- [ ] Handle parsing errors
  - [ ] Show error message
  - [ ] Allow retry
- [ ] Add responsive design
- [ ] Add accessibility features

#### Task 4.6: Parsed Data Review Page
- [ ] Create /resumes/review page (or modal)
- [ ] Add page layout and header
- [ ] Display all parsed sections
  - [ ] Contact information
  - [ ] Professional summary
  - [ ] Work experience
  - [ ] Education
  - [ ] Skills
  - [ ] Projects (if present)
  - [ ] Certifications (if present)
- [ ] Add "Looks Good" button
  - [ ] Save resume on click
  - [ ] Show success message
  - [ ] Navigate to resume list or detail
- [ ] Add "Re-parse" button
  - [ ] Return to input page
  - [ ] Preserve input
- [ ] Add responsive design
- [ ] Add accessibility features

#### Task 4.7: Resume List Page
- [ ] Create /resumes page
- [ ] Add page layout and header
- [ ] Add "Add New Resume" button
- [ ] Fetch and display resumes
  - [ ] Show loading state
  - [ ] Show error state
  - [ ] Show empty state
  - [ ] Display resume cards in grid
- [ ] Implement View action
  - [ ] Navigate to detail page
- [ ] Implement Delete action
  - [ ] Show confirmation modal
  - [ ] Delete resume
  - [ ] Update list
  - [ ] Show success message
- [ ] Add responsive design
- [ ] Add accessibility features

#### Task 4.8: Resume Detail Page
- [ ] Create /resumes/[id] page
- [ ] Add page layout and header
- [ ] Fetch and display resume data
  - [ ] Show loading state
  - [ ] Show error state
  - [ ] Display all sections
- [ ] Add "Use for Application" button
  - [ ] Navigate to new application flow
  - [ ] Pass resume ID
- [ ] Add "Download Original" button (if DOCX)
  - [ ] Download file from storage URL
- [ ] Add "Delete" button
  - [ ] Show confirmation modal
  - [ ] Delete resume
  - [ ] Navigate to list page
- [ ] Add responsive design
- [ ] Add accessibility features

### Phase 5: Testing & Polish

#### Task 5.1: End-to-End Testing
- [ ] Test complete text upload flow
  - [ ] Input → Parse → Review → Save → View
- [ ] Test complete DOCX upload flow
  - [ ] Upload → Parse → Review → Save → View
- [ ] Test error scenarios
  - [ ] Invalid input
  - [ ] Parsing failures
  - [ ] Network errors
- [ ] Test on different browsers
  - [ ] Chrome
  - [ ] Firefox
  - [ ] Safari
- [ ] Test on different devices
  - [ ] Desktop
  - [ ] Tablet
  - [ ] Mobile

#### Task 5.2: Performance Testing
- [ ] Test parsing performance
  - [ ] Measure time for various resume sizes
  - [ ] Ensure < 15 seconds for text
  - [ ] Ensure < 20 seconds for DOCX
- [ ] Test file upload performance
  - [ ] Measure time for various file sizes
  - [ ] Ensure < 10 seconds for 5MB file
- [ ] Test database query performance
  - [ ] Measure query times
  - [ ] Ensure < 2 seconds
- [ ] Optimize if needed

#### Task 5.3: Error Handling & UX Polish
- [ ] Add comprehensive error messages
  - [ ] Clear and actionable
  - [ ] User-friendly language
- [ ] Add loading states everywhere
  - [ ] Spinners
  - [ ] Progress indicators
  - [ ] Skeleton screens
- [ ] Add success feedback
  - [ ] Toast notifications
  - [ ] Success messages
- [ ] Add empty states
  - [ ] No resumes yet
  - [ ] Helpful CTAs
- [ ] Add confirmation modals
  - [ ] Delete confirmation
  - [ ] Destructive actions
- [ ] Test keyboard navigation
- [ ] Test screen reader compatibility
- [ ] Fix any accessibility issues

#### Task 5.4: Documentation
- [ ] Document API endpoints
  - [ ] Request/response formats
  - [ ] Error codes
  - [ ] Examples
- [ ] Document data models
  - [ ] Schema definitions
  - [ ] Validation rules
- [ ] Update README
  - [ ] Setup instructions
  - [ ] Environment variables
  - [ ] Running tests
- [ ] Add inline code comments
  - [ ] Complex logic
  - [ ] Business rules
- [ ] Create user guide (optional)
  - [ ] How to upload resume
  - [ ] How to review parsed data

#### Task 5.5: Code Review & Cleanup
- [ ] Review all code for quality
  - [ ] Follow coding standards
  - [ ] Remove debug code
  - [ ] Remove commented code
- [ ] Run linters
  - [ ] Black (Python)
  - [ ] Flake8 (Python)
  - [ ] ESLint (TypeScript)
  - [ ] Prettier (TypeScript)
- [ ] Fix all linting issues
- [ ] Ensure test coverage > 85%
- [ ] Review and improve error handling
- [ ] Review and improve logging

### Phase 6: Deployment

#### Task 6.1: Deployment Preparation
- [ ] Set up production database
  - [ ] Run migrations
  - [ ] Verify schema
- [ ] Set up production storage bucket
  - [ ] Configure permissions
  - [ ] Test file upload
- [ ] Configure production environment variables
  - [ ] Database URL
  - [ ] Supabase credentials
  - [ ] OpenAI API key
  - [ ] Storage bucket name
- [ ] Test with production-like data

#### Task 6.2: Deploy Backend
- [ ] Deploy to Railway/Render
- [ ] Verify API endpoints work
- [ ] Test authentication
- [ ] Test file upload
- [ ] Monitor for errors

#### Task 6.3: Deploy Frontend
- [ ] Deploy to Vercel
- [ ] Verify pages load
- [ ] Test API integration
- [ ] Test file upload
- [ ] Monitor for errors

#### Task 6.4: Post-Deployment Testing
- [ ] Test complete flow in production
- [ ] Test with real resume data
- [ ] Monitor performance
- [ ] Monitor error rates
- [ ] Fix any issues

## Estimated Timeline

- **Phase 1:** Foundation & Database Setup - 2 days
- **Phase 2:** Core Services - 5 days
- **Phase 3:** API Endpoints - 3 days
- **Phase 4:** Frontend Implementation - 5 days
- **Phase 5:** Testing & Polish - 3 days
- **Phase 6:** Deployment - 2 days

**Total:** ~20 days (4 weeks) for solo developer

## Dependencies

- Authentication system must be implemented first
- Database must be set up
- Supabase Storage must be configured
- OpenAI API access must be available

## Success Criteria

- [ ] Users can paste resume text and get parsed data
- [ ] Users can upload DOCX and get parsed data
- [ ] Parsing accuracy > 90%
- [ ] Truth bank contains all verifiable facts
- [ ] Users can review and save parsed data
- [ ] Users can view list of saved resumes
- [ ] Users can delete resumes
- [ ] All tests pass with > 85% coverage
- [ ] API documentation is complete
- [ ] Code follows project standards
- [ ] Deployed and functional in production

