---
inclusion: auto
---

# AI Job Application Copilot - Product Steering Document

## Project Overview

**Project Name:** AI Job Application Copilot

**Mission:** Empower students and early-career candidates with an intelligent, trustworthy assistant that supports the entire job application workflow—from resume tailoring to interview preparation—while maintaining honesty and user control.

## Target Users

- Students (undergraduate, graduate, bootcamp)
- Early-career professionals (0-3 years experience)
- Primary focus: Software, data, analytics, and technology roles
- Users who value transparency and control over automation

## Core Product Principles

### 1. Truthfulness Above All
- **Never fabricate** experience, skills, tools, projects, or achievements
- If a job requirement cannot be met with existing resume content, clearly flag it as "unsupported"
- AI suggestions must be grounded in the user's actual background
- When generating content, only rearrange, reframe, or emphasize existing qualifications

### 2. User Control & Transparency
- Always show a diff/preview before applying changes to resumes
- Require explicit user approval before final exports
- Make AI reasoning visible (e.g., "This requirement matches your Python project")
- Allow users to accept, reject, or modify suggestions individually

### 3. Structured Over Freeform
- Prefer structured outputs: tables, lists, categorized sections
- Use clear labels and categories (e.g., "Strong Match", "Partial Match", "Missing")
- Avoid walls of text; break information into scannable chunks
- Provide actionable insights, not just analysis

### 4. Simple & Trustworthy UX
- Clean, minimal interface without overwhelming options
- Clear visual hierarchy and intuitive navigation
- Professional aesthetic that builds confidence
- Fast, responsive interactions

## Core Features

### Resume Management
- Upload and store multiple resume versions
- Parse resume content (education, experience, skills, projects)
- Version history and comparison
- Support common formats (PDF, DOCX, TXT)

### Job Description Analysis
- Paste or import job descriptions
- Extract key requirements: skills, qualifications, responsibilities
- Categorize requirements by type (technical skills, soft skills, experience level, education)
- Identify keywords and phrases important for ATS

### Fit Analysis
- Compare resume content against JD requirements
- Categorize matches:
  - **Strong Match:** Direct evidence in resume
  - **Partial Match:** Related but not exact
  - **Missing:** No supporting content found
- Highlight gaps clearly and honestly
- Provide match percentage with transparent methodology

### Resume Tailoring
- Suggest reordering or rephrasing based on JD priorities
- Recommend emphasizing relevant projects/experience
- Propose keyword optimization (only using real skills)
- Show side-by-side diff before applying
- Generate tailored resume version with user approval

### Cover Letter Generation
- Generate personalized cover letters based on:
  - Selected resume version
  - Job description
  - Company research (if provided)
- Structure: intro, body (2-3 paragraphs), closing
- Maintain professional tone appropriate for target role
- Allow editing before export

### Recruiter Outreach
- Generate LinkedIn/email outreach drafts
- Personalize based on:
  - Target company and role
  - Mutual connections (if provided)
  - Specific interest points
- Keep concise (150-200 words)
- Multiple tone options: professional, enthusiastic, conversational

### Application Tracking
- Log submitted applications with metadata:
  - Company, role, date applied
  - Resume version used
  - Application status
  - Follow-up dates
- Simple dashboard view
- Status updates: Applied, Interviewing, Rejected, Offer

### Interview Preparation
- Generate interview prep materials from JD:
  - Likely technical questions based on required skills
  - Behavioral questions aligned with responsibilities
  - Company research prompts
  - STAR method examples from user's resume
- Create personalized "cheat sheet" for interview day

### Skill Gap Analysis
- Track recurring "Missing" skills across multiple applications
- Suggest portfolio projects or learning resources to fill gaps
- Prioritize gaps by frequency and role relevance
- Provide actionable next steps

## Technical Guidelines

### AI/LLM Integration
- Use structured prompts with clear constraints
- Implement guardrails against hallucination
- Validate AI outputs against source resume data
- Log AI decisions for transparency and debugging

### Data Handling
- Store user data locally or with explicit consent
- Never share resume content with third parties without permission
- Implement secure storage for sensitive information
- Allow data export and deletion

### Resume Parsing
- Extract structured data: sections, dates, bullet points
- Preserve formatting context for regeneration
- Handle various resume formats and structures
- Gracefully handle parsing errors

### Diff Generation
- Show clear before/after comparisons
- Highlight additions, deletions, modifications
- Use color coding: green (added), red (removed), yellow (modified)
- Allow granular accept/reject of changes

## Feature Development Priorities

### Phase 1: Core Workflow
1. Resume upload and parsing
2. JD analysis and fit scoring
3. Basic tailoring suggestions with diff preview
4. Tailored resume export

### Phase 2: Extended Workflow
1. Cover letter generation
2. Application tracking
3. Interview prep generation

### Phase 3: Advanced Features
1. Recruiter outreach drafts
2. Skill gap analysis and project suggestions
3. Multi-application insights and analytics

## UX Patterns

### Information Architecture
```
Home
├── Resumes (upload, manage versions)
├── Applications
│   ├── New Application
│   │   ├── Paste JD
│   │   ├── Analyze Fit
│   │   ├── Tailor Resume
│   │   ├── Generate Cover Letter
│   │   └── Generate Outreach
│   └── Track Applications
├── Interview Prep (per application)
└── Insights (skill gaps, trends)
```

### Key User Flows

**Flow 1: Tailored Application**
1. Upload base resume → 2. Paste JD → 3. View fit analysis → 4. Review tailoring suggestions → 5. Preview diff → 6. Approve changes → 7. Export tailored resume → 8. Generate cover letter → 9. Save to tracker

**Flow 2: Interview Prep**
1. Select tracked application → 2. Generate prep materials → 3. Review questions → 4. Add personal notes → 5. Export prep sheet

**Flow 3: Skill Development**
1. View skill gap analysis → 2. Select skill to develop → 3. Review project suggestions → 4. Add to learning plan

## Content Generation Guidelines

### Resume Tailoring
- Reorder bullet points to prioritize JD-relevant items
- Rephrase using JD keywords (without changing meaning)
- Emphasize quantifiable achievements matching JD needs
- Suggest removing less relevant content if space-constrained
- Never add skills, tools, or experiences not in original resume

### Cover Letter
- Opening: Express interest and mention how you found the role
- Body: Connect 2-3 key qualifications to JD requirements with specific examples
- Closing: Express enthusiasm and call to action
- Length: 250-400 words
- Tone: Professional but personable

### Recruiter Outreach
- Subject line: Clear, specific, mentions role
- Opening: Brief intro and connection point
- Body: 1-2 sentences on relevant background
- Ask: Request for conversation or advice
- Length: 150-200 words max

### Interview Prep
- Technical questions: Based on required skills in JD
- Behavioral questions: Based on responsibilities and company values
- Provide STAR framework examples using user's actual experience
- Include 3-5 questions for the user to ask interviewer

## Quality Standards

### AI Output Quality
- Factual accuracy: 100% (no hallucinations)
- Relevance to JD: High priority
- Professional tone: Consistent
- Grammar and spelling: Error-free
- ATS compatibility: Optimized

### Performance Targets
- Resume parsing: < 3 seconds
- Fit analysis: < 5 seconds
- Tailoring suggestions: < 10 seconds
- Cover letter generation: < 15 seconds

### Accessibility
- WCAG 2.1 AA compliance target
- Keyboard navigation support
- Screen reader compatibility
- Clear focus indicators
- Sufficient color contrast

## Error Handling

### Resume Parsing Failures
- Show clear error message
- Suggest manual entry or format conversion
- Provide example of supported format

### Insufficient Resume Data
- Clearly state what's missing
- Suggest adding relevant sections
- Don't generate placeholder content

### JD Analysis Issues
- Handle poorly formatted or vague JDs gracefully
- Extract what's possible, flag ambiguities
- Allow manual requirement entry

## Privacy & Ethics

### Data Privacy
- User data stays local or in user-controlled storage
- No training on user resumes without explicit consent
- Clear privacy policy and data handling disclosure

### Ethical AI Use
- Transparency about AI involvement
- No deceptive practices
- Encourage honest self-representation
- Provide disclaimers about AI-generated content

### Bias Mitigation
- Avoid assumptions based on demographics
- Focus on skills and qualifications only
- Test for fairness across different user backgrounds

## Success Metrics

### User Engagement
- Resume uploads per user
- Applications tracked per user
- Feature adoption rates
- Return user rate

### Outcome Metrics
- User-reported interview rate
- User-reported offer rate
- Time saved per application (user survey)
- User satisfaction score

### Quality Metrics
- Fit analysis accuracy (user validation)
- Suggestion acceptance rate
- Error rate in generated content

## Future Considerations

### Potential Enhancements
- Browser extension for one-click JD capture
- LinkedIn profile import
- Company research integration
- Salary negotiation guidance
- Portfolio website generation
- Networking tracker
- Job board integrations
- Email template library
- Calendar integration for follow-ups

### Scalability
- Multi-language support
- Industry-specific templates
- Team/university licensing
- Career coach collaboration features

## Development Standards

### Code Quality
- Write clean, maintainable code
- Follow established patterns in the codebase
- Add comments for complex logic
- Keep functions focused and single-purpose

### Testing
- Test AI output validation logic
- Test resume parsing edge cases
- Test diff generation accuracy
- Manual QA for generated content quality

### Documentation
- Document AI prompt templates
- Maintain API documentation
- Keep user-facing help content updated
- Document data schemas

## Glossary

- **JD:** Job Description
- **ATS:** Applicant Tracking System
- **Fit Analysis:** Comparison of resume content against JD requirements
- **Tailoring:** Modifying resume emphasis and wording to match a specific JD
- **STAR:** Situation, Task, Action, Result (interview response framework)
- **Diff:** Side-by-side comparison showing changes

---

**Document Version:** 1.0  
**Last Updated:** April 1, 2026  
**Maintained By:** Product Team
