# Database Schema Documentation

## Overview

The AI Job Application Copilot uses a relational database schema designed to support the complete job application workflow. The schema is normalized but practical, with clear relationships between entities.

## Entity Relationship Diagram

```
Users (1) -----> (N) Resumes
Users (1) -----> (N) JobDescriptions
Users (1) -----> (N) Applications

Resumes (1) -----> (N) TailoredResumes
Resumes (1) -----> (N) SkillGapReports

JobDescriptions (1) -----> (N) FitReports
JobDescriptions (1) -----> (N) TailoredResumes
JobDescriptions (1) -----> (N) Applications
JobDescriptions (1) -----> (N) CoverLetters
JobDescriptions (1) -----> (N) OutreachDrafts
JobDescriptions (1) -----> (N) InterviewPrep

Applications (1) -----> (1) TailoredResume
Applications (1) -----> (N) CoverLetters
Applications (1) -----> (N) OutreachDrafts
Applications (1) -----> (1) InterviewPrep
```

## Table Relationships

### Core Flow
1. **User** creates **Resumes** and **JobDescriptions**
2. **JobDescription** + **Resume** → **FitReport** (analysis)
3. **JobDescription** + **Resume** → **TailoredResume** (optimized resume)
4. **Application** links **User**, **JobDescription**, **TailoredResume**
5. **Application** generates **CoverLetters**, **OutreachDrafts**, **InterviewPrep**
6. **Resume** + **JobDescription** → **SkillGapReport** (skill analysis)

## Table Details

### Users
- **Purpose**: User authentication and profile management
- **Key Fields**: email, hashed_password, full_name, is_active, is_verified
- **Relationships**: One-to-many with all user-generated content

### Resumes
- **Purpose**: Store original resume files and parsed content
- **Key Fields**: raw_text, parsed_json, file_path, file_type, is_active
- **Relationships**: Belongs to User, generates TailoredResumes and SkillGapReports

### JobDescriptions
- **Purpose**: Store job postings and parsed analysis
- **Key Fields**: raw_text, parsed_json, job_title, company, salary_range
- **Relationships**: Belongs to User, generates FitReports and content

### Applications
- **Purpose**: Track job applications through entire hiring process
- **Key Fields**: status, priority, timeline dates, outcome
- **Relationships**: Central hub linking User, JobDescription, TailoredResume, and generated content

### Content Tables
- **TailoredResumes**: Optimized resumes with suggestions and applied changes
- **CoverLetters**: Generated cover letters with metadata and quality scores
- **OutreachDrafts**: Email and LinkedIn message drafts
- **InterviewPrep**: Questions, STAR stories, and preparation guides

### Analysis Tables
- **FitReports**: Resume-JD compatibility analysis with scores and recommendations
- **SkillGapReports**: Detailed skill gap analysis with learning recommendations

## Key Design Decisions

### Normalization vs Practicality
- **Normalized**: Clear separation of concerns with proper foreign keys
- **Practical**: JSON columns for complex data (parsed content, suggestions)
- **Indexed**: Proper indexing on foreign keys and frequently queried fields

### Data Types
- **JSON**: For structured data that doesn't need separate tables
- **DateTime**: With timezone support for accurate timestamps
- **String**: Appropriate lengths for different content types
- **Float**: For scores and percentages

### Constraints
- **Foreign Keys**: Ensure data integrity
- **Unique Constraints**: User emails, etc.
- **Default Values**: Sensible defaults for status fields
- **Nullable**: Appropriate use of nullable vs required fields

## Migration Strategy

- **Alembic**: For database version control
- **Initial Migration**: Creates all tables with proper relationships
- **Future Migrations**: Incremental schema changes
- **Rollback Support**: Downgrade functions available

## Performance Considerations

### Indexes
- Primary keys automatically indexed
- Foreign keys indexed for join performance
- Frequently queried fields (email, status, dates) indexed
- Composite indexes for complex queries

### JSON Storage
- PostgreSQL JSONB for efficient JSON operations
- Indexing on JSON fields where appropriate
- Separate columns for frequently accessed JSON data

## Security Considerations

### Sensitive Data
- Passwords hashed, never stored in plain text
- Personal information in encrypted storage
- File paths stored, files in secure storage

### Access Control
- User-scoped queries through user_id filtering
- Row-level security through application logic
- Audit trails through created_at/updated_at fields
