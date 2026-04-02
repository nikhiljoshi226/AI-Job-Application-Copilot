---
inclusion: auto
---

# AI Job Application Copilot - AI Guardrails & Safety Document

## Purpose

This document defines strict guardrails, validation rules, and safety measures for all AI-powered features in the AI Job Application Copilot. These rules ensure truthfulness, user control, and reliability across resume tailoring, job analysis, content generation, and career guidance features.

## Core AI Safety Principles

### 1. Absolute Truthfulness
AI must never fabricate, invent, or hallucinate any of the following:
- Work experience or job titles
- Projects or portfolio items
- Years of experience or employment dates
- Technical skills or programming languages
- Soft skills or competencies
- Certifications or credentials
- Educational degrees or institutions
- Achievements or awards
- Tools or technologies used
- Quantitative metrics (unless rephrasing existing ones)

### 2. Source Data Constraints
AI outputs must be grounded exclusively in:
- User's uploaded and parsed resume data
- User's explicitly provided profile information
- User's approved edits and additions
- Job description content (for analysis only)

AI must NOT use:
- General knowledge about what "typical" candidates have
- Assumptions about user's background
- Inferred skills not explicitly stated
- Projected or estimated experience


### 3. Transparency & Traceability
Every AI-generated suggestion must include:
- Clear reasoning for the suggestion
- Evidence mapping to source resume data
- Confidence level when applicable
- Explicit flags for missing requirements

### 4. User Control
- All changes require explicit user approval
- Users can accept, reject, or modify suggestions individually
- Show before/after previews for all modifications
- Allow users to revert changes
- Never auto-apply AI suggestions

### 5. Structured Outputs
- Use JSON schemas for all AI responses
- Validate outputs against predefined schemas
- Reject malformed or incomplete responses
- Log validation failures for monitoring

### 6. Professional Standards
- Maintain professional, concise language
- Avoid hyperbole or exaggeration
- No keyword stuffing or manipulation
- Optimize for ATS while preserving readability
- Keep tone appropriate for target industry

## Feature-Specific Guardrails

### Resume Parsing

**Allowed Operations:**
- Extract text from uploaded documents
- Identify resume sections (contact, experience, education, skills)
- Parse dates, job titles, company names
- Extract bullet points and descriptions
- Categorize skills by type

**Prohibited Operations:**
- Adding skills not present in resume
- Inferring experience not explicitly stated
- Assuming education level or GPA
- Inventing project details
- Extrapolating years of experience

**Validation Rules:**
- All extracted data must have source text reference
- Dates must be in valid format or null
- Contact information must be validated (email format, etc.)
- Skills must be explicitly mentioned in resume


### Job Description Analysis

**Allowed Operations:**
- Extract required skills and qualifications
- Identify responsibilities and duties
- Categorize requirements by type (technical, soft skills, education)
- Extract keywords for ATS optimization
- Identify nice-to-have vs. required qualifications
- Parse experience level requirements

**Prohibited Operations:**
- Making assumptions about unlisted requirements
- Adding requirements not in the JD
- Interpreting vague requirements too broadly
- Assuming company culture or values not stated

**Validation Rules:**
- All requirements must have source text from JD
- Categorization must be consistent (technical/soft/education/experience)
- Required vs. nice-to-have distinction must be clear
- Years of experience must be numeric or null
- Skills must be specific, not generic categories

### Fit Analysis

**Allowed Operations:**
- Match resume content to JD requirements
- Categorize matches as: Strong, Partial, Missing
- Provide evidence from resume for each match
- Calculate match percentage based on coverage
- Identify keyword gaps

**Prohibited Operations:**
- Claiming matches without resume evidence
- Marking requirements as "Strong Match" with weak evidence
- Inventing connections between resume and JD
- Overstating partial matches
- Hiding or downplaying missing requirements

**Validation Rules:**
- Every "Strong Match" must have direct evidence
- Every "Partial Match" must explain the gap
- Every "Missing" requirement must be clearly flagged
- Evidence must reference specific resume sections
- Match score must be calculated transparently

**Evidence Quality Standards:**
- Strong Match: Direct mention of skill/requirement in resume
- Partial Match: Related but not exact (e.g., similar technology)
- Missing: No supporting evidence in resume


### Resume Tailoring

**Allowed Operations:**
- Reorder bullet points to emphasize relevant experience
- Rephrase existing content using JD keywords (without changing meaning)
- Suggest emphasizing certain projects or experiences
- Recommend de-emphasizing less relevant content
- Adjust formatting for ATS optimization
- Reframe achievements to align with JD language

**Prohibited Operations:**
- Adding new skills not in original resume
- Inventing projects or experiences
- Changing dates or durations
- Adding technologies or tools not mentioned
- Fabricating metrics or achievements
- Claiming certifications user doesn't have
- Inflating job titles or responsibilities

**Validation Rules:**
- Every suggestion must map to existing resume content
- Rephrased content must preserve original meaning
- No new factual claims can be introduced
- Suggestions must include reasoning
- Changes must be reversible
- Original resume data must be preserved

**Suggestion Types & Constraints:**

1. **Reorder Suggestions**
   - Must reference existing items only
   - Must provide clear reasoning (relevance to JD)
   - Must maintain chronological integrity within sections

2. **Rephrase Suggestions**
   - Must preserve factual accuracy
   - Can incorporate JD keywords if truthful
   - Must maintain professional tone
   - Cannot exaggerate or inflate

3. **Emphasize Suggestions**
   - Must identify existing content to highlight
   - Must explain relevance to JD
   - Cannot add new information


### Cover Letter Generation

**Allowed Operations:**
- Reference specific experiences from resume
- Connect resume content to JD requirements
- Express genuine interest in role
- Highlight relevant achievements from resume
- Use professional, personalized tone
- Structure: intro, body (2-3 paragraphs), closing

**Prohibited Operations:**
- Inventing experiences or projects
- Claiming skills not in resume
- Fabricating connections to company
- Making up reasons for interest
- Exaggerating qualifications
- Using generic templates without personalization
- Claiming knowledge of company not provided by user

**Validation Rules:**
- Every claim must reference resume data
- Length: 250-400 words
- Must include specific examples (not generic)
- Tone must be professional and authentic
- No clichés or overused phrases
- Must be tailored to specific JD

**Content Requirements:**
- Opening: Role title, how user found position
- Body: 2-3 specific examples from resume matching JD
- Closing: Call to action, expression of interest
- All examples must be verifiable in resume

**Quality Checks:**
- No placeholder text (e.g., "[Your Name]", "[Company]")
- No generic statements without specifics
- No exaggerated language ("perfect fit", "dream job")
- Proper grammar and spelling
- Professional formatting


### Recruiter Outreach

**Allowed Operations:**
- Draft concise, professional outreach messages
- Reference specific role and company
- Highlight 1-2 relevant qualifications from resume
- Request conversation or advice
- Personalize based on user-provided context

**Prohibited Operations:**
- Inventing mutual connections
- Fabricating reasons for reaching out
- Claiming familiarity with company not provided
- Exaggerating qualifications
- Using manipulative language
- Making false claims about referrals

**Validation Rules:**
- Length: 150-200 words maximum
- Must reference specific role
- Must include clear call to action
- All qualifications must be from resume
- Tone must be professional and respectful
- No aggressive or pushy language

**Template Structure:**
- Subject line: Clear, specific, mentions role
- Opening: Brief intro, connection point (if any)
- Body: 1-2 sentences on relevant background from resume
- Ask: Specific request (conversation, advice, consideration)
- Closing: Professional sign-off

**Tone Guidelines:**
- Professional but personable
- Confident but not arrogant
- Specific but concise
- Respectful of recipient's time


### Interview Preparation

**Allowed Operations:**
- Generate likely technical questions based on JD requirements
- Generate behavioral questions based on JD responsibilities
- Suggest STAR method examples using actual resume content
- Provide company research prompts
- Create personalized prep checklist
- Suggest questions for user to ask interviewer

**Prohibited Operations:**
- Inventing experiences for STAR examples
- Suggesting user claim skills they don't have
- Fabricating company information
- Creating fake scenarios
- Recommending dishonest interview strategies
- Suggesting memorized answers that aren't truthful

**Validation Rules:**
- Technical questions must align with JD requirements
- Behavioral questions must relate to JD responsibilities
- STAR examples must use actual resume content
- Suggested answers must be truthful frameworks, not scripts
- Company research must be based on provided info or general guidance

**Content Structure:**
- Technical questions: 5-10 based on required skills
- Behavioral questions: 5-8 based on responsibilities
- STAR examples: 3-5 using real resume experiences
- Questions to ask: 5-7 thoughtful, role-specific questions
- Prep checklist: Practical, actionable items

**STAR Example Guidelines:**
- Situation: Must reference real context from resume
- Task: Must be actual responsibility user had
- Action: Must be actions user actually took
- Result: Must be real outcomes (or framework for user to fill)


### Skill Gap Analysis

**Allowed Operations:**
- Identify skills frequently missing across applications
- Categorize gaps by skill type and frequency
- Suggest learning resources for missing skills
- Recommend portfolio projects to demonstrate skills
- Prioritize gaps by relevance to target roles

**Prohibited Operations:**
- Suggesting user claim skills before learning them
- Recommending dishonest resume updates
- Overstating urgency of skill gaps
- Suggesting shortcuts that compromise learning
- Making assumptions about user's learning capacity

**Validation Rules:**
- Gaps must be based on actual JD analysis data
- Frequency counts must be accurate
- Project suggestions must be realistic and achievable
- Learning resources should be reputable
- Prioritization must be transparent

**Output Structure:**
- Gap identification: Skill name, frequency, role types
- Impact assessment: How critical is this gap?
- Learning path: Resources, timeline, difficulty
- Project ideas: Specific, achievable portfolio projects
- Priority ranking: Based on frequency and role relevance

**Project Suggestion Guidelines:**
- Must be achievable for target skill level
- Should demonstrate the missing skill clearly
- Include specific deliverables
- Provide realistic time estimates
- Suggest technologies/tools to use


## Validation Schemas

### Resume Parser Output Schema

```json
{
  "type": "object",
  "required": ["contact", "experience", "skills"],
  "properties": {
    "contact": {
      "type": "object",
      "required": ["name", "email"],
      "properties": {
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "phone": {"type": ["string", "null"]},
        "location": {"type": ["string", "null"]},
        "linkedin": {"type": ["string", "null"], "format": "uri"},
        "github": {"type": ["string", "null"], "format": "uri"},
        "portfolio": {"type": ["string", "null"], "format": "uri"}
      }
    },
    "summary": {"type": ["string", "null"]},
    "experience": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["company", "title", "bullets"],
        "properties": {
          "company": {"type": "string", "minLength": 1},
          "title": {"type": "string", "minLength": 1},
          "start_date": {"type": ["string", "null"]},
          "end_date": {"type": ["string", "null"]},
          "location": {"type": ["string", "null"]},
          "bullets": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
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
          "institution": {"type": "string", "minLength": 1},
          "degree": {"type": "string", "minLength": 1},
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
    "projects": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "description"],
        "properties": {
          "name": {"type": "string", "minLength": 1},
          "description": {"type": "string", "minLength": 1},
          "technologies": {
            "type": "array",
            "items": {"type": "string"}
          },
          "bullets": {
            "type": "array",
            "items": {"type": "string"}
          },
          "url": {"type": ["string", "null"], "format": "uri"}
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
    "certifications": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name"],
        "properties": {
          "name": {"type": "string", "minLength": 1},
          "issuer": {"type": ["string", "null"]},
          "date": {"type": ["string", "null"]}
        }
      }
    }
  }
}
```

**Validation Rules:**
- Contact name and email are mandatory
- Experience must have at least company, title, and bullets
- All arrays must not contain empty strings
- URLs must be valid format or null
- Dates should be parseable or null
- No fabricated data allowed


### Job Description Parser Output Schema

```json
{
  "type": "object",
  "required": ["company", "title", "requirements"],
  "properties": {
    "company": {"type": "string", "minLength": 1},
    "title": {"type": "string", "minLength": 1},
    "location": {"type": ["string", "null"]},
    "job_type": {"type": ["string", "null"]},
    "salary_range": {"type": ["string", "null"]},
    "requirements": {
      "type": "object",
      "required": ["technical_skills"],
      "properties": {
        "technical_skills": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["skill", "required"],
            "properties": {
              "skill": {"type": "string", "minLength": 1},
              "required": {"type": "boolean"},
              "years": {"type": ["number", "null"], "minimum": 0}
            }
          }
        },
        "soft_skills": {
          "type": "array",
          "items": {"type": "string", "minLength": 1}
        },
        "education": {
          "type": "array",
          "items": {"type": "string", "minLength": 1}
        },
        "experience_years": {"type": ["number", "null"], "minimum": 0},
        "certifications": {
          "type": "array",
          "items": {"type": "string", "minLength": 1}
        }
      }
    },
    "responsibilities": {
      "type": "array",
      "items": {"type": "string", "minLength": 1}
    },
    "nice_to_have": {
      "type": "array",
      "items": {"type": "string", "minLength": 1}
    },
    "keywords": {
      "type": "array",
      "items": {"type": "string", "minLength": 1}
    }
  }
}
```

**Validation Rules:**
- Company and title are mandatory
- Technical skills must specify if required or nice-to-have
- Years of experience must be non-negative or null
- All extracted content must have source in JD text
- No assumptions about unlisted requirements
- Keywords must be actually present in JD


### Tailoring Suggestions Output Schema

```json
{
  "type": "object",
  "required": ["suggestions"],
  "properties": {
    "suggestions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "section", "reason", "evidence"],
        "properties": {
          "type": {
            "type": "string",
            "enum": ["reorder", "rephrase", "emphasize", "deemphasize"]
          },
          "section": {
            "type": "string",
            "enum": ["experience", "projects", "skills", "education", "summary"]
          },
          "item_id": {"type": "string"},
          "bullet_index": {"type": ["number", "null"]},
          "original": {"type": ["string", "null"]},
          "suggested": {"type": ["string", "null"]},
          "reason": {"type": "string", "minLength": 10},
          "evidence": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
            "minItems": 1
          },
          "jd_alignment": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    }
  }
}
```

**Validation Rules:**
- Every suggestion must have a clear reason
- Every suggestion must have evidence from resume
- Rephrase suggestions must include both original and suggested text
- Suggested text must preserve factual accuracy
- No new skills or experiences can be added
- Evidence must reference actual resume content
- JD alignment must reference actual JD requirements

**Post-Generation Validation:**
1. Compare suggested text to original for factual consistency
2. Verify no new claims are introduced
3. Check that all evidence exists in resume
4. Ensure professional tone maintained
5. Validate no keyword stuffing


### Cover Letter Output Schema

```json
{
  "type": "object",
  "required": ["content", "metadata", "evidence_map"],
  "properties": {
    "content": {
      "type": "object",
      "required": ["opening", "body", "closing"],
      "properties": {
        "opening": {"type": "string", "minLength": 20, "maxLength": 200},
        "body": {
          "type": "array",
          "items": {"type": "string", "minLength": 50},
          "minItems": 2,
          "maxItems": 3
        },
        "closing": {"type": "string", "minLength": 20, "maxLength": 150}
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "word_count": {"type": "number", "minimum": 250, "maximum": 400},
        "tone": {"type": "string", "enum": ["professional", "enthusiastic", "conversational"]},
        "personalization_score": {"type": "number", "minimum": 0, "maximum": 1}
      }
    },
    "evidence_map": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["claim", "resume_source"],
        "properties": {
          "claim": {"type": "string"},
          "resume_source": {"type": "string"},
          "section": {"type": "string"}
        }
      },
      "minItems": 2
    }
  }
}
```

**Validation Rules:**
- Word count must be 250-400 words
- Must include at least 2 specific examples from resume
- Every claim must map to resume evidence
- No generic or template language
- No placeholder text
- Professional tone maintained
- Proper grammar and spelling
- Personalized to specific role and company

**Content Quality Checks:**
1. Verify all examples exist in resume
2. Check for generic phrases (flag for review)
3. Ensure specific role/company mentions
4. Validate professional tone
5. Check for exaggeration or hyperbole
6. Verify no fabricated connections


### Interview Prep Output Schema

```json
{
  "type": "object",
  "required": ["technical_questions", "behavioral_questions", "star_examples"],
  "properties": {
    "technical_questions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question", "skill_area", "difficulty"],
        "properties": {
          "question": {"type": "string", "minLength": 10},
          "skill_area": {"type": "string"},
          "difficulty": {"type": "string", "enum": ["basic", "intermediate", "advanced"]},
          "jd_reference": {"type": "string"}
        }
      },
      "minItems": 5,
      "maxItems": 10
    },
    "behavioral_questions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question", "focus_area"],
        "properties": {
          "question": {"type": "string", "minLength": 10},
          "focus_area": {"type": "string"},
          "jd_reference": {"type": "string"}
        }
      },
      "minItems": 5,
      "maxItems": 8
    },
    "star_examples": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["scenario", "situation", "task", "action", "result", "resume_source"],
        "properties": {
          "scenario": {"type": "string"},
          "situation": {"type": "string", "minLength": 20},
          "task": {"type": "string", "minLength": 20},
          "action": {"type": "string", "minLength": 20},
          "result": {"type": "string", "minLength": 20},
          "resume_source": {"type": "string"},
          "applicable_questions": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      },
      "minItems": 3,
      "maxItems": 5
    },
    "questions_to_ask": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["question", "category"],
        "properties": {
          "question": {"type": "string", "minLength": 10},
          "category": {"type": "string", "enum": ["role", "team", "company", "growth", "culture"]},
          "why_ask": {"type": "string"}
        }
      },
      "minItems": 5,
      "maxItems": 7
    }
  }
}
```

**Validation Rules:**
- Technical questions must align with JD requirements
- Behavioral questions must relate to JD responsibilities
- All STAR examples must reference actual resume content
- STAR components must be complete and specific
- Questions to ask must be thoughtful and role-specific
- No generic or template questions

**STAR Example Validation:**
1. Verify situation exists in resume
2. Verify task was user's actual responsibility
3. Verify actions are plausible given user's role
4. Verify results are from resume or reasonable framework
5. Ensure no fabricated scenarios


## AI Prompt Engineering Guidelines

### System Prompt Structure

Every AI call must include:
1. Role definition (e.g., "You are a resume analysis assistant")
2. Core constraints (no fabrication, use only provided data)
3. Output format specification (JSON schema)
4. Quality standards (professional, concise, truthful)
5. Validation requirements

### Example System Prompt Template

```
You are a [ROLE] assistant for a job application platform.

CRITICAL CONSTRAINTS:
- Never fabricate or invent information
- Only use data from the provided resume/JD
- If information is missing, explicitly flag it as missing
- All outputs must be in valid JSON matching the provided schema

YOUR TASK:
[Specific task description]

OUTPUT FORMAT:
[JSON schema]

QUALITY STANDARDS:
- Professional and concise language
- Truthful and accurate
- Evidence-based reasoning
- No exaggeration or hyperbole
```

### User Prompt Best Practices

1. Provide complete context (resume data, JD data)
2. Be explicit about constraints
3. Request structured output
4. Ask for evidence/reasoning
5. Specify validation requirements

### Few-Shot Examples

Include 1-2 examples in prompts for:
- Complex parsing tasks
- Fit analysis categorization
- Tailoring suggestion format
- Cover letter structure


## Validation Implementation

### Pre-Generation Validation

Before sending to AI:
1. Verify input data completeness
2. Check data format and structure
3. Validate user permissions
4. Ensure required context is available

### Post-Generation Validation

After receiving AI output:
1. Validate against JSON schema
2. Check for required fields
3. Verify data types and formats
4. Validate business logic constraints
5. Check for prohibited content

### Validation Code Pattern

```python
from pydantic import BaseModel, ValidationError

def validate_ai_output(raw_output: dict, schema: BaseModel) -> BaseModel:
    """
    Validate AI output against schema and business rules.
    
    Raises:
        ValidationError: If output doesn't match schema
        ValueError: If business rules are violated
    """
    try:
        # Schema validation
        validated = schema(**raw_output)
        
        # Business rule validation
        validate_business_rules(validated)
        
        return validated
    except ValidationError as e:
        log_validation_error(e)
        raise
    except ValueError as e:
        log_business_rule_violation(e)
        raise

def validate_business_rules(data: BaseModel):
    """
    Check business-specific constraints.
    """
    # Example: Verify no fabricated skills
    if hasattr(data, 'suggestions'):
        for suggestion in data.suggestions:
            if suggestion.type == 'rephrase':
                verify_no_new_claims(suggestion.original, suggestion.suggested)
```

### Validation Failure Handling

When validation fails:
1. Log the failure with context
2. Retry with adjusted prompt (max 2 retries)
3. If still failing, return error to user
4. Never use unvalidated AI output


## Monitoring & Auditing

### Metrics to Track

**Quality Metrics:**
- Validation failure rate by feature
- User rejection rate of AI suggestions
- Average confidence scores
- Evidence mapping completeness

**Safety Metrics:**
- Fabrication detection rate
- Schema validation failures
- Business rule violations
- User-reported inaccuracies

**Performance Metrics:**
- AI response time by feature
- Token usage per request
- Cost per user action
- Retry rates

### Logging Requirements

Log every AI interaction:
```python
{
  "timestamp": "ISO-8601",
  "user_id": "uuid",
  "feature": "resume_tailoring",
  "input_hash": "sha256",
  "output_hash": "sha256",
  "validation_status": "success|failure",
  "validation_errors": [],
  "token_usage": 1234,
  "latency_ms": 2500,
  "model": "gpt-4",
  "prompt_version": "v1.2"
}
```

### Audit Trail

Maintain audit trail for:
- All AI-generated suggestions
- User approvals/rejections
- Applied changes to resumes
- Generated documents
- Validation failures

### Review Process

**Regular Reviews:**
- Weekly: Review validation failure patterns
- Monthly: Analyze user rejection rates
- Quarterly: Audit sample outputs for quality

**Incident Response:**
- User reports fabrication → Immediate investigation
- High validation failure rate → Prompt review
- Unusual patterns → Manual audit


## Error Messages & User Communication

### When AI Validation Fails

**User-Facing Messages:**

- **Resume Parsing Failure:**
  "We couldn't parse your resume. Please try uploading a different format (PDF or DOCX) or check that the file isn't corrupted."

- **JD Analysis Failure:**
  "We had trouble analyzing this job description. Please ensure it includes clear requirements and responsibilities."

- **Tailoring Generation Failure:**
  "We couldn't generate tailoring suggestions. This might be because the job description is too vague or your resume needs more detail."

- **Cover Letter Generation Failure:**
  "We couldn't generate a cover letter. Please ensure your resume has sufficient experience details to reference."

**Internal Error Codes:**
- `PARSE_ERROR`: Parsing failed
- `VALIDATION_ERROR`: Schema validation failed
- `BUSINESS_RULE_VIOLATION`: Guardrail constraint violated
- `AI_TIMEOUT`: AI request timed out
- `INSUFFICIENT_DATA`: Not enough resume data for task

### Transparency with Users

Always communicate:
- What the AI can and cannot do
- Why certain suggestions are made
- What data is being used
- When requirements are missing vs. matched

### Disclaimers

Include appropriate disclaimers:
- "AI-generated content should be reviewed before use"
- "Suggestions are based on your resume data only"
- "We never fabricate experience or skills"
- "Final decisions about content are yours"


## Testing AI Guardrails

### Unit Tests for Validation

Test each validation function:
```python
def test_resume_parser_rejects_fabricated_skills():
    """Ensure parser doesn't add skills not in resume."""
    resume_text = "Experience with Python and JavaScript"
    parsed = parse_resume(resume_text)
    
    # Should not include skills not mentioned
    assert "Java" not in parsed.skills.languages
    assert "React" not in parsed.skills.frameworks

def test_tailoring_preserves_facts():
    """Ensure tailoring doesn't change factual content."""
    original = "Built REST API with 3 endpoints"
    suggestion = generate_tailoring_suggestion(original, jd_data)
    
    # Should not inflate numbers or add technologies
    assert "3 endpoints" in suggestion.suggested or "three endpoints" in suggestion.suggested
    assert not any(tech in suggestion.suggested for tech in ["GraphQL", "gRPC"] if tech not in original)
```

### Integration Tests

Test end-to-end flows:
1. Upload resume → Parse → Verify no fabrication
2. Analyze JD → Generate suggestions → Verify evidence mapping
3. Generate cover letter → Verify all claims have resume source
4. Generate interview prep → Verify STAR examples use real content

### Adversarial Testing

Test with challenging inputs:
- Sparse resumes (minimal content)
- Vague job descriptions
- Mismatched resume-JD pairs
- Edge cases (career changers, gaps, etc.)

### Manual Review

Periodically review:
- Sample of AI outputs for quality
- User-rejected suggestions for patterns
- Validation failures for false positives
- Edge cases and unusual scenarios


## Model Selection & Configuration

### Model Recommendations by Task

**GPT-4 (Higher Quality, Higher Cost):**
- Resume tailoring suggestions
- Cover letter generation
- Complex fit analysis
- Interview prep generation

**GPT-3.5-turbo (Faster, Lower Cost):**
- Resume parsing (structured extraction)
- JD parsing (structured extraction)
- Simple keyword extraction
- Basic categorization tasks

### Temperature Settings

- **Parsing tasks:** temperature = 0.0 (deterministic)
- **Analysis tasks:** temperature = 0.2 (mostly deterministic)
- **Generation tasks:** temperature = 0.3-0.5 (slight creativity)
- **Never use:** temperature > 0.7 (too unpredictable)

### Token Limits

Set appropriate max_tokens:
- Resume parsing: 2000 tokens
- JD parsing: 1500 tokens
- Fit analysis: 1000 tokens
- Tailoring suggestions: 1500 tokens
- Cover letter: 800 tokens
- Interview prep: 2000 tokens

### Function Calling

Always use function calling for structured outputs:
```python
functions = [{
    "name": "parse_resume",
    "description": "Extract structured data from resume",
    "parameters": RESUME_SCHEMA
}]

response = openai.chat.completions.create(
    model="gpt-4",
    messages=messages,
    functions=functions,
    function_call={"name": "parse_resume"},
    temperature=0.0
)
```


## Continuous Improvement

### Feedback Loop

Collect feedback on:
- User acceptance/rejection of suggestions
- User edits to AI-generated content
- User-reported inaccuracies
- Validation failure patterns

### Prompt Iteration

Regularly update prompts based on:
- Common validation failures
- User rejection patterns
- Quality issues identified in review
- New edge cases discovered

### Version Control

Maintain versions of:
- System prompts
- JSON schemas
- Validation rules
- Business logic constraints

Track changes and their impact on quality metrics.

### A/B Testing

Test prompt variations:
- Different instruction phrasing
- Different example formats
- Different constraint emphasis
- Different output structures

Measure impact on:
- Validation success rate
- User acceptance rate
- Output quality scores
- Processing time

### Model Updates

When OpenAI releases new models:
1. Test with existing validation suite
2. Compare output quality
3. Measure cost/performance tradeoffs
4. Gradual rollout with monitoring
5. Rollback plan if quality degrades


## Edge Cases & Special Scenarios

### Career Changers

**Challenge:** Limited relevant experience for target role

**Guardrails:**
- Don't invent relevant experience
- Clearly flag missing requirements
- Suggest emphasizing transferable skills (if they exist)
- Don't overstate relevance of unrelated experience

**Approach:**
- Focus on transferable skills explicitly mentioned
- Highlight relevant projects or coursework
- Be honest about gaps in cover letter
- Suggest skill development in gap analysis

### Entry-Level Candidates

**Challenge:** Limited professional experience

**Guardrails:**
- Don't inflate internships to full-time roles
- Don't fabricate years of experience
- Don't claim professional skills from coursework only

**Approach:**
- Emphasize relevant coursework and projects
- Highlight internships and part-time work
- Focus on demonstrated skills through projects
- Be honest about experience level

### Employment Gaps

**Challenge:** Gaps in work history

**Guardrails:**
- Never fabricate employment to fill gaps
- Don't extend employment dates
- Don't invent freelance work

**Approach:**
- Focus on skills and achievements, not timeline
- If user provides gap explanation, incorporate it
- Don't draw attention to gaps unnecessarily
- Emphasize most recent relevant experience

### Sparse Resumes

**Challenge:** Minimal content to work with

**Guardrails:**
- Don't generate content to fill space
- Don't assume skills or experience
- Be explicit about limitations

**Approach:**
- Work with available content only
- Suggest user add more detail (don't do it for them)
- Focus on quality over quantity
- Clearly communicate when more info is needed


## Compliance & Ethics

### Ethical AI Use

**Commitments:**
- Transparency about AI involvement
- User control over all outputs
- Honesty in all generated content
- No deceptive practices
- Respect for user data privacy

**Prohibited Practices:**
- Generating false credentials
- Fabricating work history
- Inflating qualifications
- Manipulating dates or durations
- Creating fake references or recommendations
- Encouraging dishonest interview responses

### Legal Considerations

**Resume Content:**
- Don't generate content that could be considered fraud
- Don't suggest misrepresenting protected characteristics
- Don't encourage discrimination in any form
- Respect intellectual property (no copying others' content)

**Data Privacy:**
- Handle resume data as sensitive personal information
- Comply with data protection regulations (GDPR, CCPA)
- Don't share user data with third parties
- Provide data deletion capabilities

### Bias Mitigation

**Awareness:**
- AI models may have inherent biases
- Job descriptions may contain biased language
- Resume parsing may favor certain formats

**Mitigation Strategies:**
- Focus on skills and qualifications only
- Avoid assumptions based on names, locations, etc.
- Test with diverse resume samples
- Monitor for disparate impact
- Allow users to control all content

### Responsible Disclosure

**To Users:**
- Clearly state AI is used in the product
- Explain what AI does and doesn't do
- Provide transparency about limitations
- Offer human review options when possible

**To Employers:**
- Don't hide that resumes were AI-assisted
- Ensure all content is truthful and user-approved
- Maintain user's authentic voice and story


## Implementation Checklist

### Before Launch

**Validation Infrastructure:**
- [ ] JSON schemas defined for all AI outputs
- [ ] Pydantic models implemented for validation
- [ ] Business rule validation functions implemented
- [ ] Error handling for validation failures
- [ ] Retry logic with backoff

**Guardrail Implementation:**
- [ ] System prompts include fabrication constraints
- [ ] Evidence mapping required for all suggestions
- [ ] User approval flow implemented
- [ ] Diff preview functionality working
- [ ] Original data preservation verified

**Testing:**
- [ ] Unit tests for all validation functions
- [ ] Integration tests for end-to-end flows
- [ ] Adversarial testing with edge cases
- [ ] Manual review of sample outputs
- [ ] Performance testing under load

**Monitoring:**
- [ ] Logging infrastructure in place
- [ ] Metrics collection configured
- [ ] Alerting for high failure rates
- [ ] Audit trail implementation
- [ ] User feedback collection

**Documentation:**
- [ ] User-facing disclaimers written
- [ ] Error messages defined
- [ ] API documentation complete
- [ ] Internal runbooks created
- [ ] Incident response plan documented

### Post-Launch

**Week 1:**
- Monitor validation failure rates
- Review user feedback
- Check for unexpected edge cases
- Verify logging and metrics

**Month 1:**
- Analyze user acceptance rates
- Review sample outputs for quality
- Identify prompt improvement opportunities
- Assess cost and performance

**Ongoing:**
- Regular quality audits
- Prompt iteration based on feedback
- Schema updates as needed
- Model evaluation and updates
- Continuous improvement cycle


## Summary

This document establishes comprehensive guardrails for AI usage in the AI Job Application Copilot. The core principle is absolute truthfulness: the AI must never fabricate information and must always ground its outputs in the user's actual resume data.

### Key Takeaways

1. **Truthfulness is non-negotiable** - No fabrication of any kind
2. **Validation is mandatory** - All AI outputs must pass schema and business rule validation
3. **User control is paramount** - All changes require explicit approval
4. **Transparency builds trust** - Show reasoning and evidence for all suggestions
5. **Structured outputs ensure reliability** - Use JSON schemas and function calling
6. **Monitoring enables improvement** - Track metrics and iterate on quality

### Enforcement

These guardrails must be:
- Implemented in code (validation functions)
- Enforced at runtime (reject invalid outputs)
- Monitored continuously (metrics and alerts)
- Reviewed regularly (quality audits)
- Updated as needed (continuous improvement)

### Responsibility

Every team member working on AI features must:
- Understand these guardrails thoroughly
- Implement validation rigorously
- Test edge cases comprehensively
- Monitor quality continuously
- Report issues promptly

### Success Criteria

The AI system is successful when:
- Zero fabrication incidents reported
- High user trust and satisfaction
- Low validation failure rates
- High suggestion acceptance rates
- Consistent output quality

---

**Document Version:** 1.0  
**Last Updated:** April 1, 2026  
**Maintained By:** AI Safety Team  
**Review Frequency:** Quarterly or after significant incidents
