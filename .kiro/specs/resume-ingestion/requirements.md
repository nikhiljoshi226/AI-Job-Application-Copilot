# Resume Ingestion Module - Requirements Specification

## Overview

The Resume Ingestion module enables users to input their resume data through multiple methods (manual text paste and DOCX upload), extracts and normalizes the content, parses it into structured JSON, and creates a truth bank of verifiable facts that will be used throughout the application to prevent fabrication.

## Feature Name

`resume-ingestion`

## User Stories

### US1: Manual Resume Text Input
**As a** job seeker  
**I want to** paste my resume text directly into the application  
**So that** I can quickly get started without needing to upload a file

**Acceptance Criteria:**
- User can paste resume text into a large textarea
- System validates minimum text length (100 characters)
- System extracts and parses the pasted text
- User sees parsing progress indicator
- User can review parsed data before saving
- User can edit parsed data if needed
- System saves both raw text and parsed JSON

### US2: DOCX Resume Upload
**As a** job seeker  
**I want to** upload my resume as a DOCX file  
**So that** I can preserve my existing resume format

**Acceptance Criteria:**
- User can select or drag-drop a DOCX file
- System validates file type (DOCX only for this module)
- System validates file size (max 5MB)
- System extracts text from DOCX
- System parses extracted text
- User sees parsing progress
- User can review parsed data
- System stores original file in cloud storage
- System saves both raw text and parsed JSON

### US3: Resume Parsing into Structured JSON
**As a** system  
**I need to** parse resume text into structured JSON sections  
**So that** the data can be used for analysis and tailoring

**Acceptance Criteria:**
- System extracts contact information (name, email, phone, location, links)
- System extracts professional summary (if present)
- System extracts work experience with company, title, dates, bullets
- System extracts education with institution, degree, field, dates
- System extracts skills categorized by type
- System extracts projects with name, description, technologies, bullets
- System extracts certifications with name, issuer, date (if present)
- All extracted data follows defined JSON schema
- System validates extracted data against schema
- System handles missing sections gracefully

### US4: Truth Bank Creation
**As a** system  
**I need to** create a truth bank of verifiable facts from the resume  
**So that** I can prevent fabrication in tailoring suggestions

**Acceptance Criteria:**
- System extracts all factual claims from resume
- Truth bank includes: skills mentioned, technologies used, companies worked at, job titles held, projects completed, degrees earned, certifications obtained
- Each fact is linked to its source section in the resume
- Truth bank is stored alongside parsed JSON
- Truth bank is used for validation in all downstream features

### US5: Resume Data Review and Correction
**As a** job seeker  
**I want to** review and correct parsed resume data  
**So that** I can ensure accuracy before using it

**Acceptance Criteria:**
- User sees structured display of all parsed sections
- User can edit any field in the parsed data
- User can add missing sections
- User can delete incorrect entries
- System re-validates after edits
- System updates truth bank after edits
- User must explicitly confirm before saving

### US6: Resume Storage and Retrieval
**As a** job seeker  
**I want to** save my parsed resume and access it later  
**So that** I can use it for multiple job applications

**Acceptance Criteria:**
- System saves resume with user-provided name
- System stores raw text, parsed JSON, and truth bank
- System stores original DOCX file (if uploaded)
- User can view list of saved resumes
- User can view details of any saved resume
- User can delete saved resumes
- System prevents unauthorized access to resumes



## Functional Requirements

### FR1: Input Methods

**FR1.1: Text Paste Input**
- System shall provide a textarea for manual resume text input
- Textarea shall support at least 10,000 characters
- System shall validate minimum text length of 100 characters
- System shall display character count
- System shall preserve line breaks and formatting

**FR1.2: DOCX File Upload**
- System shall accept DOCX file uploads via file picker or drag-drop
- System shall validate file extension is .docx
- System shall validate file size does not exceed 5MB
- System shall validate file is not corrupted
- System shall extract text content from DOCX
- System shall preserve text structure (paragraphs, bullets)
- System shall store original DOCX file in cloud storage

**FR1.3: Input Validation**
- System shall reject empty input
- System shall reject input shorter than 100 characters
- System shall reject files larger than 5MB
- System shall reject non-DOCX files
- System shall provide clear error messages for validation failures

### FR2: Resume Parsing

**FR2.1: Contact Information Extraction**
- System shall extract full name (required)
- System shall extract email address (required)
- System shall extract phone number (optional)
- System shall extract location/address (optional)
- System shall extract LinkedIn URL (optional)
- System shall extract GitHub URL (optional)
- System shall extract portfolio URL (optional)
- System shall validate email format
- System shall validate URL formats

**FR2.2: Professional Summary Extraction**
- System shall identify and extract professional summary section
- System shall handle various section names (Summary, Profile, About, Objective)
- System shall extract full summary text
- Summary is optional

**FR2.3: Work Experience Extraction**
- System shall extract all work experience entries
- For each entry, system shall extract:
  - Company name (required)
  - Job title (required)
  - Start date (optional, various formats)
  - End date or "Present" (optional)
  - Location (optional)
  - Bullet points/responsibilities (required, at least 1)
- System shall preserve bullet point order
- System shall handle various date formats
- System shall handle concurrent positions

**FR2.4: Education Extraction**
- System shall extract all education entries
- For each entry, system shall extract:
  - Institution name (required)
  - Degree type (required)
  - Field of study (optional)
  - Start date (optional)
  - End date or "Expected" (optional)
  - GPA (optional)
  - Achievements/honors (optional, list)
- System shall handle various degree formats (BS, B.S., Bachelor of Science)

**FR2.5: Skills Extraction**
- System shall extract all mentioned skills
- System shall categorize skills into:
  - Programming languages
  - Frameworks/libraries
  - Tools/technologies
  - Other/soft skills
- System shall handle various skill section formats
- System shall deduplicate skills
- System shall preserve skill groupings if present

**FR2.6: Projects Extraction**
- System shall extract all project entries
- For each entry, system shall extract:
  - Project name (required)
  - Description (required)
  - Technologies used (optional, list)
  - Bullet points/details (optional, list)
  - URL/link (optional)
- Projects section is optional

**FR2.7: Certifications Extraction**
- System shall extract all certification entries
- For each entry, system shall extract:
  - Certification name (required)
  - Issuing organization (optional)
  - Issue date (optional)
  - Expiration date (optional)
- Certifications section is optional

**FR2.8: Parsing Validation**
- System shall validate all extracted data against JSON schema
- System shall ensure required fields are present
- System shall validate data types
- System shall validate date formats
- System shall validate URL formats
- System shall reject parsing if critical data is missing (name, email)

### FR3: Truth Bank Creation

**FR3.1: Fact Extraction**
- System shall extract all factual claims from resume
- System shall identify:
  - All skills mentioned anywhere in resume
  - All technologies/tools mentioned
  - All companies worked at
  - All job titles held
  - All projects completed
  - All degrees earned
  - All certifications obtained
  - All quantifiable achievements (numbers, percentages)

**FR3.2: Fact Categorization**
- System shall categorize facts by type (skill, technology, company, etc.)
- System shall link each fact to its source section
- System shall link each fact to specific text in resume
- System shall mark confidence level for each fact

**FR3.3: Truth Bank Storage**
- System shall store truth bank as structured JSON
- System shall store alongside parsed resume data
- System shall update truth bank when resume is edited
- System shall make truth bank queryable for validation

### FR4: Data Storage

**FR4.1: Resume Record Creation**
- System shall create database record for each resume
- System shall generate unique ID for resume
- System shall associate resume with user account
- System shall store creation timestamp
- System shall store last updated timestamp

**FR4.2: Data Persistence**
- System shall store raw resume text
- System shall store parsed JSON data
- System shall store truth bank JSON
- System shall store original DOCX file URL (if uploaded)
- System shall store user-provided resume name
- System shall store parsing metadata (version, timestamp)

**FR4.3: File Storage**
- System shall upload DOCX files to Supabase Storage
- System shall organize files by user ID
- System shall generate secure file URLs
- System shall handle file upload failures gracefully

### FR5: User Interface

**FR5.1: Resume Input Page**
- System shall provide tabbed interface for input methods (Text Paste, DOCX Upload)
- System shall show clear instructions for each method
- System shall display file requirements (type, size)
- System shall show real-time validation feedback
- System shall display parsing progress indicator
- System shall show estimated time remaining

**FR5.2: Parsed Data Review Page**
- System shall display all parsed sections in structured format
- System shall highlight each section clearly
- System shall show edit controls for each field
- System shall allow adding missing sections
- System shall allow deleting incorrect entries
- System shall show validation errors inline
- System shall provide "Looks Good" confirmation button
- System shall provide "Re-parse" option

**FR5.3: Resume List Page**
- System shall display all user's resumes in grid layout
- System shall show resume name, creation date for each
- System shall provide "View" action for each resume
- System shall provide "Delete" action for each resume
- System shall show empty state if no resumes
- System shall provide "Add New Resume" button

**FR5.4: Resume Detail Page**
- System shall display all parsed resume data
- System shall show each section in readable format
- System shall provide "Use for Application" button
- System shall provide "Edit" button (future)
- System shall provide "Delete" button
- System shall show original file download link (if DOCX)



## Non-Functional Requirements

### NFR1: Performance
- Resume parsing shall complete within 15 seconds for text input
- Resume parsing shall complete within 20 seconds for DOCX upload
- DOCX text extraction shall complete within 5 seconds
- File upload to storage shall complete within 10 seconds
- Database operations shall complete within 2 seconds
- UI shall remain responsive during parsing

### NFR2: Reliability
- System shall validate all AI-generated parsing output
- System shall handle parsing failures gracefully
- System shall retry failed AI calls up to 3 times
- System shall preserve user input on parsing failure
- System shall maintain data consistency between raw text and parsed JSON
- System shall prevent data loss during upload/parsing

### NFR3: Security
- System shall authenticate all API requests
- System shall authorize users to access only their own resumes
- System shall validate and sanitize all user input
- System shall scan uploaded files for malicious content
- System shall encrypt sensitive data at rest
- System shall use secure file storage with access controls
- System shall not log sensitive resume content

### NFR4: Usability
- Parsing progress shall be visible to user
- Error messages shall be clear and actionable
- Validation feedback shall be immediate
- UI shall guide user through the process
- System shall support keyboard navigation
- System shall be accessible (WCAG AA)

### NFR5: Maintainability
- Parsing logic shall be modular and testable
- AI prompts shall be versioned and configurable
- JSON schema shall be versioned
- Code shall follow project coding standards
- All functions shall have comprehensive tests
- System shall log parsing metadata for debugging

### NFR6: Scalability
- System shall handle resumes up to 10,000 characters
- System shall support concurrent parsing requests
- Database schema shall support future resume versions
- Truth bank structure shall be extensible

## Business Rules

### BR1: Data Integrity
- Raw text and parsed JSON must always be in sync
- Truth bank must be derived from parsed JSON
- Edits to parsed data must update truth bank
- Original DOCX file must be preserved unchanged

### BR2: Validation Rules
- Name and email are mandatory for all resumes
- At least one of experience or education must be present
- All dates must be parseable or null
- All URLs must be valid format or null
- Skills list must not be empty
- Experience bullets must not be empty
- Education degree must not be empty

### BR3: Truth Bank Rules
- All facts in truth bank must have source reference
- Facts must be categorized by type
- Facts must be deduplicated
- Facts must be queryable for validation
- Truth bank must be updated when resume is edited

### BR4: Parsing Rules
- System must never fabricate information
- System must extract only what is explicitly stated
- System must handle various resume formats
- System must preserve original wording in bullets
- System must handle missing sections gracefully
- System must validate extracted data before saving

## Constraints

### Technical Constraints
- Must use OpenAI API for parsing (GPT-3.5-turbo for cost efficiency)
- Must use Supabase Storage for file storage
- Must use PostgreSQL for database
- Must use python-docx for DOCX text extraction
- Must follow existing project architecture

### Business Constraints
- Must support only DOCX format initially (not PDF)
- Must support English language only initially
- Must work within OpenAI API rate limits
- Must optimize for cost (use cheaper model where possible)

### User Constraints
- Users must have valid authentication
- Users must accept terms of service
- Users must provide accurate information

## Success Criteria

### Parsing Accuracy
- Contact information extraction accuracy > 95%
- Work experience extraction accuracy > 90%
- Education extraction accuracy > 90%
- Skills extraction accuracy > 85%
- Overall parsing success rate > 90%

### User Experience
- Users can complete resume input in < 3 minutes
- Users report satisfaction with parsed data accuracy
- Users can easily correct parsing errors
- Clear error messages for all failure cases

### System Performance
- 95% of parsing requests complete within SLA
- Zero data loss incidents
- Zero unauthorized access incidents
- System handles 100 concurrent users

### Code Quality
- Test coverage > 80% for parsing logic
- All validation rules have tests
- All API endpoints have integration tests
- Code passes all linting checks

## Dependencies

### External Dependencies
- OpenAI API (GPT-3.5-turbo)
- Supabase Storage
- Supabase Auth
- PostgreSQL database

### Internal Dependencies
- Authentication system (must be implemented first)
- Database schema (must be created)
- File storage configuration (must be set up)

### Library Dependencies
- python-docx (DOCX text extraction)
- pydantic (data validation)
- openai (AI client)
- supabase-py (storage client)

## Risks and Mitigations

### Risk 1: AI Parsing Inaccuracy
**Impact:** High - Incorrect data affects all downstream features  
**Probability:** Medium  
**Mitigation:**
- Use structured output with function calling
- Validate all AI output against schema
- Allow user to review and correct
- Implement comprehensive validation rules
- Test with diverse resume samples

### Risk 2: DOCX Extraction Failures
**Impact:** Medium - Users cannot upload DOCX files  
**Probability:** Low  
**Mitigation:**
- Use reliable python-docx library
- Handle corrupted files gracefully
- Provide clear error messages
- Offer text paste as alternative
- Test with various DOCX formats

### Risk 3: Performance Issues
**Impact:** Medium - Poor user experience  
**Probability:** Low  
**Mitigation:**
- Use GPT-3.5-turbo for faster parsing
- Implement progress indicators
- Optimize database queries
- Cache parsed results
- Monitor performance metrics

### Risk 4: Data Privacy Concerns
**Impact:** High - Legal and trust issues  
**Probability:** Low  
**Mitigation:**
- Implement strict access controls
- Encrypt data at rest
- Follow data protection regulations
- Clear privacy policy
- Audit access logs

### Risk 5: Truth Bank Incompleteness
**Impact:** Medium - Fabrication detection may fail  
**Probability:** Medium  
**Mitigation:**
- Comprehensive fact extraction logic
- Multiple extraction passes
- Validation against source text
- User review of extracted facts
- Continuous improvement based on feedback

## Open Questions

1. Should we support PDF upload in addition to DOCX?
   - **Decision:** No, DOCX only for MVP. PDF in post-MVP.

2. Should we support resume editing after initial parsing?
   - **Decision:** Yes, but as a future enhancement. MVP allows review and correction during initial parsing only.

3. How should we handle resumes in languages other than English?
   - **Decision:** English only for MVP. Multi-language support post-MVP.

4. Should we support multiple resume versions per user?
   - **Decision:** Yes, users can upload multiple resumes with different names.

5. How long should we retain uploaded DOCX files?
   - **Decision:** Retain indefinitely until user deletes resume or account.

6. Should we support resume templates or formatting?
   - **Decision:** No, focus on content extraction only. Formatting is for generation phase.

## Glossary

- **Resume Ingestion:** The process of accepting, extracting, parsing, and storing resume data
- **Truth Bank:** A structured collection of verifiable facts extracted from the resume
- **Parsed JSON:** Structured representation of resume data following defined schema
- **Raw Text:** Original text content from resume (pasted or extracted from DOCX)
- **Fact:** A verifiable claim from the resume (skill, experience, education, etc.)
- **Source Reference:** Link from a fact to its location in the original resume
- **Validation:** Process of checking data against rules and schema
- **Normalization:** Process of standardizing data format and structure

