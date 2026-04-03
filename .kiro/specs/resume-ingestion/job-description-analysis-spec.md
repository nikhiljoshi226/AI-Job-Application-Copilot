# Job Description Analysis Module Specification

## Overview
The Job Description Analysis module parses job descriptions, extracts key information, and compares it against user resume data to provide comprehensive fit analysis.

## Goals
- Accept job title, company, and JD text
- Parse the JD into structured JSON
- Extract required skills, preferred skills, responsibilities, keywords, role type, and domain clues
- Compare the JD against available resume data
- Produce fit analysis with matched skills, missing skills, and role alignment

## Backend Service Design

### API Endpoints

#### 1. Analyze Job Description
```
POST /api/v1/job-analysis/analyze
```

**Request Body:**
```json
{
  "job_title": "Senior Software Engineer",
  "company": "Tech Corp",
  "job_description": "Full job description text...",
  "resume_id": "optional-resume-id-for-comparison"
}
```

**Response:**
```json
{
  "analysis_id": "uuid",
  "status": "completed",
  "parsed_jd": { ... },
  "fit_analysis": { ... },
  "created_at": "2026-04-02T22:06:00Z"
}
```

#### 2. Get Analysis Result
```
GET /api/v1/job-analysis/{analysis_id}
```

#### 3. Compare with Multiple Resumes
```
POST /api/v1/job-analysis/compare-multiple
```

### Service Architecture

#### JD Parser Service
- **Responsibility**: Extract structured information from raw job description text
- **Input**: Raw JD text
- **Output**: Structured JSON with extracted components

#### Skills Extraction Service
- **Responsibility**: Identify and categorize skills from JD text
- **Input**: JD text sections
- **Output**: Categorized skills (technical, soft, domain-specific)

#### Resume Comparison Service
- **Responsibility**: Compare JD requirements against resume data
- **Input**: Parsed JD + resume data
- **Output**: Fit analysis with skill gaps and matches

#### AI/ML Integration
- **NLP Processing**: Use transformer models for text understanding
- **Skill Classification**: Machine learning models for skill categorization
- **Semantic Matching**: Vector similarity for skill matching

## Frontend Flow

### User Journey
1. **Input Collection**
   - Job title input field
   - Company name input field
   - Job description text area (with paste support)
   - Optional resume selection dropdown

2. **Processing State**
   - Loading indicator with progress steps
   - Real-time status updates
   - Estimated processing time

3. **Results Display**
   - Parsed JD summary
   - Skills breakdown (required vs preferred)
   - Fit analysis visualization
   - Skill gap analysis
   - Actionable recommendations

### Component Structure
```
JobAnalysis/
├── JobAnalysisForm.jsx          # Input form
├── AnalysisProgress.jsx         # Processing state
├── ParsedJDDisplay.jsx          # Structured JD view
├── SkillsBreakdown.jsx          # Skills visualization
├── FitAnalysis.jsx              # Comparison results
├── SkillGapAnalysis.jsx         # Missing skills display
└── Recommendations.jsx          # Action items
```

## Structured Output Schema

### Parsed Job Description Schema
```json
{
  "job_metadata": {
    "job_title": "Senior Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "employment_type": "full-time",
    "experience_level": "senior",
    "salary_range": "$120,000-$180,000",
    "remote_policy": "hybrid"
  },
  "skills": {
    "required": [
      {
        "skill": "Python",
        "category": "programming_language",
        "proficiency_level": "advanced",
        "context": "5+ years of Python development"
      }
    ],
    "preferred": [
      {
        "skill": "AWS",
        "category": "cloud_platform",
        "proficiency_level": "intermediate",
        "context": "Experience with AWS services preferred"
      }
    ],
    "soft_skills": [
      {
        "skill": "Communication",
        "category": "interpersonal",
        "proficiency_level": "strong",
        "context": "Excellent communication skills"
      }
    ]
  },
  "responsibilities": [
    {
      "responsibility": "Design and develop scalable applications",
      "category": "development",
      "priority": "high"
    }
  ],
  "qualifications": {
    "education": [
      {
        "degree": "Bachelor's",
        "field": "Computer Science",
        "required": true
      }
    ],
    "certifications": [
      {
        "name": "AWS Certified Developer",
        "required": false
      }
    ],
    "experience": {
      "minimum_years": 5,
      "preferred_years": 8,
      "specific_domains": ["cloud computing", "microservices"]
    }
  },
  "keywords": [
    "python", "django", "aws", "microservices", "api", "agile"
  ],
  "role_type": {
    "primary": "software_engineering",
    "secondary": ["backend", "full_stack"],
    "industry": "technology",
    "domain_clues": ["saas", "b2b", "enterprise"]
  },
  "company_insights": {
    "size": "mid-size",
    "industry": "technology",
    "culture_keywords": ["innovative", "fast-paced", "collaborative"]
  }
}
```

### Fit Analysis Schema
```json
{
  "overall_fit_score": 85,
  "fit_breakdown": {
    "skills_match": 90,
    "experience_match": 80,
    "education_match": 100,
    "responsibilities_alignment": 75
  },
  "matched_skills": [
    {
      "skill": "Python",
      "match_type": "exact",
      "confidence": 0.95,
      "resume_evidence": "5 years Python development at Company X"
    }
  ],
  "missing_skills": [
    {
      "skill": "AWS",
      "gap_type": "complete",
      "importance": "medium",
      "learning_resources": ["AWS Certified Developer course"]
    }
  ],
  "partial_matches": [
    {
      "skill": "Django",
      "match_type": "related",
      "confidence": 0.70,
      "resume_evidence": "Flask experience",
      "gap_analysis": "Similar framework, quick learning curve"
    }
  ],
  "role_alignment": {
    "alignment_score": 88,
    "alignment_factors": [
      {
        "factor": "Experience level",
        "alignment": "matched",
        "details": "Senior level matches 5+ years experience"
      }
    ],
    "misalignment_factors": [
      {
        "factor": "Industry experience",
        "alignment": "partial",
        "details": "Tech industry experience but not SaaS specifically"
      }
    ]
  },
  "recommendations": [
    {
      "type": "skill_development",
      "priority": "high",
      "action": "Learn AWS fundamentals",
      "estimated_time": "2-3 months",
      "resources": ["AWS tutorials", "Certification prep"]
    }
  ]
}
```

## Validation Rules

### Input Validation
- **Job Title**: Required, max 100 characters, alphanumeric + spaces
- **Company**: Required, max 100 characters, alphanumeric + spaces
- **Job Description**: Required, min 100 characters, max 10,000 characters
- **Resume ID**: Optional, must be valid UUID if provided

### Content Validation
- **JD Text Quality**: Must contain identifiable sections (responsibilities, requirements)
- **Skill Extraction**: Minimum 3 skills must be identified
- **Language**: Must be in English (detectable via language detection)

### Output Validation
- **Completeness**: All required fields must be populated
- **Consistency**: Skill categories must match predefined taxonomy
- **Scoring**: Fit scores must be between 0-100
- **Confidence**: ML confidence scores must be >= 0.5 for inclusion

## Error Cases

### HTTP Status Codes
- **400 Bad Request**: Invalid input format, validation failures
- **422 Unprocessable Entity**: Valid format but content issues
- **429 Too Many Requests**: Rate limiting exceeded
- **500 Internal Server Error**: Processing failures, ML model issues
- **503 Service Unavailable**: AI services down

### Error Response Schema
```json
{
  "error": {
    "code": "JD_PARSE_FAILED",
    "message": "Unable to parse job description",
    "details": {
      "reason": "Insufficient identifiable sections",
      "suggestion": "Ensure JD includes requirements and responsibilities sections"
    },
    "timestamp": "2026-04-02T22:06:00Z",
    "request_id": "uuid"
  }
}
```

### Specific Error Scenarios
1. **Empty/Invalid JD Text**: Return 422 with guidance on required content
2. **Unsupported Language**: Return 422 with language detection result
3. **Resume Not Found**: Return 404 if resume_id doesn't exist
4. **AI Service Timeout**: Return 503 with retry suggestion
5. **Content Too Large**: Return 413 with size limits

## Database Schema

### Tables

#### job_analyses
```sql
CREATE TABLE job_analyses (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    job_title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    raw_jd_text TEXT NOT NULL,
    parsed_jd JSONB NOT NULL,
    fit_analysis JSONB,
    resume_id UUID REFERENCES resumes(id),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    processing_time_ms INTEGER,
    error_details JSONB
);
```

#### extracted_skills
```sql
CREATE TABLE extracted_skills (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES job_analyses(id),
    skill_name VARCHAR(255) NOT NULL,
    skill_category VARCHAR(100) NOT NULL,
    proficiency_level VARCHAR(50),
    is_required BOOLEAN DEFAULT false,
    is_preferred BOOLEAN DEFAULT false,
    context TEXT,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### skill_matches
```sql
CREATE TABLE skill_matches (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES job_analyses(id),
    skill_name VARCHAR(255) NOT NULL,
    match_type VARCHAR(50) NOT NULL, -- 'exact', 'partial', 'related', 'missing'
    confidence_score FLOAT,
    resume_evidence TEXT,
    gap_analysis TEXT,
    importance_level VARCHAR(50), -- 'high', 'medium', 'low'
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### fit_recommendations
```sql
CREATE TABLE fit_recommendations (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES job_analyses(id),
    recommendation_type VARCHAR(100) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    action_text TEXT NOT NULL,
    estimated_time VARCHAR(100),
    resources JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Indexes
```sql
CREATE INDEX idx_job_analyses_user_id ON job_analyses(user_id);
CREATE INDEX idx_job_analyses_created_at ON job_analyses(created_at DESC);
CREATE INDEX idx_extracted_skills_analysis_id ON extracted_skills(analysis_id);
CREATE INDEX idx_extracted_skills_name ON extracted_skills(skill_name);
CREATE INDEX idx_skill_matches_analysis_id ON skill_matches(analysis_id);
CREATE INDEX idx_fit_recommendations_analysis_id ON fit_recommendations(analysis_id);
```

## Test Plan

### Unit Tests

#### JD Parser Service Tests
- **Test Valid JD Parsing**: Verify correct extraction from standard JD formats
- **Test Edge Cases**: Handle malformed JDs, missing sections
- **Test Skill Extraction**: Validate skill identification and categorization
- **Test Language Detection**: Ensure proper language identification

#### Skills Extraction Tests
- **Test Technical Skills**: Verify programming language identification
- **Test Soft Skills**: Validate interpersonal skill extraction
- **Test Skill Levels**: Ensure proficiency level detection
- **Test Context Preservation**: Verify context is captured correctly

#### Resume Comparison Tests
- **Test Exact Matches**: Validate perfect skill matching
- **Test Partial Matches**: Ensure related skill detection
- **Test Gap Analysis**: Verify missing skill identification
- **Test Scoring Algorithm**: Validate fit score calculation

### Integration Tests

#### API Endpoint Tests
- **Test Complete Flow**: End-to-end JD analysis
- **Test Error Handling**: Verify proper error responses
- **Test Rate Limiting**: Ensure rate limiting works
- **Test Authentication**: Validate user access controls

#### Database Tests
- **Test Data Persistence**: Verify analysis storage
- **Test Data Relationships**: Ensure foreign key constraints
- **Test Performance**: Validate query performance with large datasets
- **Test Data Integrity**: Ensure JSON schema validation

### Performance Tests

#### Load Testing
- **Concurrent Users**: Test with 100+ simultaneous analyses
- **Large JD Processing**: Verify handling of 10,000+ character JDs
- **Memory Usage**: Monitor memory consumption during processing
- **Response Times**: Ensure <5 second response time for typical JDs

#### Stress Testing
- **AI Service Failures**: Test graceful degradation
- **Database Connection Limits**: Verify connection pooling
- **Memory Pressure**: Test under low memory conditions
- **Network Latency**: Ensure resilience to slow AI responses

### User Acceptance Tests

#### Usability Tests
- **Input Form Validation**: Test user input guidance
- **Result Comprehensibility**: Ensure clear presentation
- **Actionable Insights**: Verify recommendations are useful
- **Mobile Responsiveness**: Test on mobile devices

#### Accuracy Tests
- **Human Validation**: Compare AI extraction with human analysis
- **Industry Diversity**: Test across different industries
- **Role Variety**: Validate for different job types
- **Resume Diversity**: Test with various resume formats

### Test Data Sets

#### Positive Test Cases
- Well-structured tech JDs
- Standard corporate JDs
- Startup job postings
- Remote job descriptions

#### Negative Test Cases
- Minimal JD content
- Non-English JDs
- Poorly formatted JDs
- Extremely long JDs

#### Edge Cases
- JDs with emojis/special characters
- JDs with tables/lists
- JDs with salary information
- JDs with unusual requirements

## Implementation Timeline

### Phase 1: Core Infrastructure (2 weeks)
- Database schema implementation
- Basic API endpoints
- JD parsing service foundation
- Unit test framework setup

### Phase 2: AI Integration (3 weeks)
- ML model integration
- Skills extraction algorithms
- Resume comparison logic
- Initial accuracy testing

### Phase 3: Frontend Development (2 weeks)
- Input form components
- Results display components
- Progress indicators
- Basic styling

### Phase 4: Integration & Testing (2 weeks)
- End-to-end testing
- Performance optimization
- Error handling refinement
- User acceptance testing

### Phase 5: Deployment & Monitoring (1 week)
- Production deployment
- Monitoring setup
- Documentation completion
- User training materials

## Success Metrics

### Technical Metrics
- **Processing Speed**: <5 seconds for typical JD
- **Accuracy Rate**: >90% skill extraction accuracy
- **Uptime**: >99.5% service availability
- **Error Rate**: <1% processing failures

### User Metrics
- **Completion Rate**: >80% of analyses completed successfully
- **User Satisfaction**: >4.5/5 rating on usefulness
- **Adoption Rate**: >60% of active users use feature
- **Action Rate**: >40% of users follow recommendations

## Security Considerations

### Data Protection
- **PII Redaction**: Automatically remove personal information
- **Data Encryption**: Encrypt sensitive JD data at rest
- **Access Controls**: Role-based access to analysis data
- **Data Retention**: Configurable data retention policies

### API Security
- **Rate Limiting**: Prevent abuse with rate limits
- **Input Sanitization**: Prevent injection attacks
- **Authentication**: Secure user authentication
- **Audit Logging**: Track all analysis requests

## Monitoring & Observability

### Metrics to Track
- **Processing Time**: Average analysis duration
- **Error Rates**: Types and frequency of errors
- **Usage Patterns**: Peak usage times and volumes
- **Model Performance**: AI model accuracy over time

### Alerting
- **High Error Rates**: Alert when error rate >5%
- **Slow Processing**: Alert when processing time >10 seconds
- **Service Downtime**: Immediate alert for service failures
- **Resource Usage**: Alert on high memory/CPU usage

## Future Enhancements

### Advanced Features
- **Batch Analysis**: Process multiple JDs simultaneously
- **Trend Analysis**: Identify skill trends across JDs
- **Salary Prediction**: Estimate salary based on requirements
- **Career Path Mapping**: Suggest career progression based on JD analysis

### AI Improvements
- **Custom Models**: Train models on specific industries
- **Multilingual Support**: Expand to non-English JDs
- **Real-time Updates**: Continuous model improvement
- **Explainable AI**: Provide reasoning for skill matches

### Integration Opportunities
- **ATS Integration**: Connect with applicant tracking systems
- **LinkedIn Integration**: Import JDs directly from LinkedIn
- **Resume Builders**: Auto-update resumes based on JD analysis
- **Interview Prep**: Generate interview questions based on JD
