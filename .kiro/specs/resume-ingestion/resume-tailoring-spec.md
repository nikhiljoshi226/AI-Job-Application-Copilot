# Resume Tailoring Workflow Specification

## Overview
The Resume Tailoring Workflow uses parsed resume data and job description analysis to generate intelligent, truthful tailoring suggestions that enhance resume alignment without fabricating experience.

## Goals
- Use parsed resume JSON and parsed JD JSON as inputs
- Generate truthful tailoring suggestions based on existing experience
- Do not invent experience or unsupported claims
- Show diff preview before applying changes
- Allow users to accept, reject, or edit each suggestion
- Build final tailored resume JSON after approval

## AI Orchestration Flow

### 1. Input Processing Stage
```
Parsed Resume JSON + Parsed JD JSON → Input Validation → Context Preparation
```

**Components:**
- **Input Validator**: Ensure both JSON schemas are valid and complete
- **Context Builder**: Create unified context with resume and JD data
- **Evidence Indexer**: Index all resume experiences, skills, and achievements

### 2. Gap Analysis Stage
```
Context Preparation → Skill Gap Analysis → Experience Mapping → Alignment Scoring
```

**Components:**
- **Skill Gap Analyzer**: Identify missing or underemphasized skills from JD
- **Experience Mapper**: Map resume experiences to JD requirements
- **Alignment Scorer**: Calculate current alignment percentage

### 3. Suggestion Generation Stage
```
Gap Analysis → Content Enhancement → Reordering Logic → Keyword Optimization
```

**Components:**
- **Content Enhancer**: Suggest experience rephrasing for better alignment
- **Reordering Engine**: Recommend section reordering for impact
- **Keyword Optimizer**: Suggest keyword additions without fabrication

### 4. Evidence Validation Stage
```
Generated Suggestions → Evidence Verification → Truthfulness Check → Confidence Scoring
```

**Components:**
- **Evidence Verifier**: Ensure all suggestions have supporting evidence
- **Truthfulness Checker**: Validate against fabrication rules
- **Confidence Scorer**: Assign confidence scores to each suggestion

### 5. Output Generation Stage
```
Validated Suggestions → Diff Generation → Preview Builder → Final Assembly
```

**Components:**
- **Diff Generator**: Create before/after comparisons
- **Preview Builder**: Format suggestions for user review
- **Final Assembler**: Prepare approved changes for application

## Structured Output Schema for Suggestions

### Main Suggestion Response
```json
{
  "tailoring_session_id": "uuid",
  "resume_id": "uuid",
  "job_analysis_id": "uuid",
  "current_alignment_score": 65,
  "potential_alignment_score": 92,
  "suggestions": [
    {
      "suggestion_id": "uuid",
      "type": "experience_enhancement",
      "category": "technical_skills",
      "priority": "high",
      "confidence_score": 0.85,
      "impact_score": 0.78,
      "description": "Rephrase Python experience to emphasize Django framework",
      "original_content": {
        "section": "experience",
        "item_id": "exp_001",
        "text": "Developed web applications using Python"
      },
      "suggested_content": {
        "section": "experience",
        "item_id": "exp_001",
        "text": "Developed scalable web applications using Python and Django framework"
      },
      "evidence_mapping": {
        "source_items": ["exp_001_skill_python", "exp_001_tech_django"],
        "supporting_text": "Resume shows Python development and Django technology listed",
        "confidence_rationale": "Direct evidence from experience section"
      },
      "jd_alignment": {
        "matched_requirements": ["Python", "Django"],
        "alignment_boost": 0.15,
        "keyword_coverage": ["web applications", "scalable"]
      },
      "change_type": "modification",
      "estimated_impact": "high"
    }
  ],
  "summary": {
    "total_suggestions": 12,
    "high_priority": 5,
    "medium_priority": 4,
    "low_priority": 3,
    "estimated_improvement": "27% increase in alignment score",
    "processing_time_ms": 2500
  },
  "metadata": {
    "model_version": "v2.1",
    "processing_timestamp": "2026-04-02T22:09:00Z",
    "truthfulness_score": 0.92
  }
}
```

### Suggestion Types Schema

#### Experience Enhancement
```json
{
  "type": "experience_enhancement",
  "original_content": {
    "section": "experience",
    "item_id": "exp_003",
    "text": "Managed team projects",
    "metrics": null
  },
  "suggested_content": {
    "section": "experience",
    "item_id": "exp_003",
    "text": "Led cross-functional team of 5 developers on agile projects",
    "metrics": {
      "team_size": 5,
      "methodology": "agile"
    }
  },
  "evidence_mapping": {
    "source_items": ["exp_003_team_lead", "skills_leadership"],
    "supporting_text": "Leadership role mentioned in skills section",
    "confidence_rationale": "Team leadership experience supported by skills section"
  }
}
```

#### Skill Reordering
```json
{
  "type": "skill_reordering",
  "section": "technical_skills",
  "original_order": ["Python", "JavaScript", "React", "Node.js"],
  "suggested_order": ["Python", "Django", "JavaScript", "React", "Node.js"],
  "evidence_mapping": {
    "source_items": ["jd_required_python", "jd_preferred_django"],
    "supporting_text": "JD prioritizes Python and Django skills",
    "confidence_rationale": "Direct JD requirement alignment"
  },
  "jd_alignment": {
    "matched_requirements": ["Python", "Django"],
    "alignment_boost": 0.08
  }
}
```

#### Keyword Addition
```json
{
  "type": "keyword_addition",
  "section": "summary",
  "original_content": {
    "text": "Software engineer with 5 years of experience"
  },
  "suggested_content": {
    "text": "Software engineer with 5 years of experience in full-stack development and cloud technologies"
  },
  "added_keywords": ["full-stack development", "cloud technologies"],
  "evidence_mapping": {
    "source_items": ["exp_001_fullstack", "exp_002_aws"],
    "supporting_text": "Experience includes full-stack and AWS cloud work",
    "confidence_rationale": "Keywords supported by project experience"
  }
}
```

#### Section Reordering
```json
{
  "type": "section_reordering",
  "original_structure": ["summary", "experience", "education", "skills"],
  "suggested_structure": ["summary", "skills", "experience", "education"],
  "evidence_mapping": {
    "source_items": ["jd_role_type_senior", "resume_experience_level"],
    "supporting_text": "Senior role benefits from skills prominence",
    "confidence_rationale": "Industry best practice for senior positions"
  },
  "rationale": "Skills section should appear early for senior technical roles"
}
```

## Evidence Mapping Design

### Evidence Sources
```json
{
  "evidence_sources": {
    "direct_experience": {
      "type": "experience_section",
      "weight": 1.0,
      "description": "Direct mention in work experience"
    },
    "skills_section": {
      "type": "skills_list",
      "weight": 0.8,
      "description": "Listed in skills section"
    },
    "project_details": {
      "type": "project_work",
      "weight": 0.9,
      "description": "Demonstrated in project descriptions"
    },
    "certifications": {
      "type": "certification",
      "weight": 0.7,
      "description": "Certified through formal training"
    },
    "education": {
      "type": "academic",
      "weight": 0.6,
      "description": "Learned through formal education"
    }
  }
}
```

### Evidence Chain Schema
```json
{
  "evidence_chain": {
    "primary_evidence": {
      "source": "exp_001",
      "type": "direct_experience",
      "text": "Developed Python applications for 3 years",
      "confidence": 0.95
    },
    "supporting_evidence": [
      {
        "source": "skills_python",
        "type": "skills_section",
        "text": "Python (Advanced)",
        "confidence": 0.8
      },
      {
        "source": "project_web_app",
        "type": "project_details",
        "text": "Built web application using Python and Django",
        "confidence": 0.9
      }
    ],
    "overall_confidence": 0.91,
    "verification_status": "verified"
  }
}
```

### Truthfulness Validation Rules
```json
{
  "truthfulness_rules": {
    "no_fabrication": {
      "rule": "Cannot add skills not present in any evidence source",
      "enforcement": "strict"
    },
    "no_exaggeration": {
      "rule": "Cannot inflate metrics beyond supported evidence",
      "enforcement": "strict"
    },
    "context_preservation": {
      "rule": "Must maintain original context and timeframe",
      "enforcement": "moderate"
    },
    "evidence_threshold": {
      "rule": "Minimum evidence confidence of 0.7 required",
      "enforcement": "strict"
    },
    "plausible_enhancement": {
      "rule": "Enhancements must be plausible within original context",
      "enforcement": "moderate"
    }
  }
}
```

## Diff Preview Data Shape

### Diff Response Schema
```json
{
  "diff_session_id": "uuid",
  "tailoring_session_id": "uuid",
  "resume_id": "uuid",
  "diff_view": {
    "sections": [
      {
        "section_name": "summary",
        "section_type": "text",
        "changes": [
          {
            "change_id": "change_001",
            "type": "addition",
            "position": {
              "start": 45,
              "end": 45
            },
            "original_text": "",
            "suggested_text": "specializing in full-stack development",
            "context": "Software engineer with 5 years of experience || specializing in full-stack development || and cloud technologies",
            "evidence_highlight": {
              "sources": ["exp_001_fullstack", "exp_002_cloud"],
              "confidence": 0.85
            }
          }
        ]
      },
      {
        "section_name": "experience",
        "section_type": "list",
        "items": [
          {
            "item_id": "exp_001",
            "changes": [
              {
                "change_id": "change_002",
                "type": "modification",
                "field": "description",
                "original_text": "Developed web applications using Python",
                "suggested_text": "Developed scalable web applications using Python and Django framework",
                "word_changes": [
                  {
                    "type": "addition",
                    "word": "scalable",
                    "position": 10
                  },
                  {
                    "type": "addition",
                    "phrase": "and Django framework",
                    "position": 35
                  }
                ],
                "evidence_highlight": {
                  "sources": ["exp_001_django_mention", "skills_django"],
                  "confidence": 0.92
                }
              }
            ]
          }
        ]
      }
    ]
  },
  "summary_statistics": {
    "total_changes": 8,
    "additions": 5,
    "modifications": 3,
    "deletions": 0,
    "sections_affected": 3,
    "estimated_impact_score": 0.78
  },
  "interactive_elements": {
    "accept_all_enabled": true,
    "reject_all_enabled": true,
    "individual_review_required": true,
    "edit_suggestions_available": true
  }
}
```

### Interactive Diff Controls
```json
{
  "diff_controls": {
    "change_actions": [
      {
        "change_id": "change_001",
        "available_actions": ["accept", "reject", "edit"],
        "default_action": "review",
        "edit_constraints": {
          "max_length_increase": 50,
          "must_preserve_evidence": true,
          "cannot_add_new_skills": true
        }
      }
    ],
    "bulk_actions": {
      "accept_all": {
        "enabled": true,
        "confirmation_required": true,
        "warning_message": "This will apply all suggested changes"
      },
      "reject_all": {
        "enabled": true,
        "confirmation_required": false
      },
      "accept_high_priority": {
        "enabled": true,
        "filter_criteria": {
          "priority": "high",
          "confidence_min": 0.8
        }
      }
    }
  }
}
```

## Backend API Endpoints

### 1. Generate Tailoring Suggestions
```
POST /api/v1/resume-tailoring/generate-suggestions
```

**Request Body:**
```json
{
  "resume_id": "uuid",
  "job_analysis_id": "uuid",
  "options": {
    "aggressiveness": "moderate", // "conservative", "moderate", "aggressive"
    "focus_areas": ["skills", "experience", "keywords"],
    "max_suggestions": 20,
    "require_evidence_threshold": 0.7
  }
}
```

**Response:**
```json
{
  "tailoring_session_id": "uuid",
  "status": "completed",
  "suggestions": { ... }, // Full suggestions schema
  "processing_metadata": {
    "duration_ms": 2500,
    "model_version": "v2.1",
    "truthfulness_score": 0.92
  }
}
```

### 2. Get Diff Preview
```
POST /api/v1/resume-tailoring/preview-diff
```

**Request Body:**
```json
{
  "tailoring_session_id": "uuid",
  "selected_suggestions": ["uuid1", "uuid2", "uuid3"],
  "preview_options": {
    "show_evidence": true,
    "highlight_changes": true,
    "include_context": true
  }
}
```

**Response:**
```json
{
  "diff_session_id": "uuid",
  "diff_view": { ... }, // Full diff schema
  "summary_statistics": { ... }
}
```

### 3. Apply Tailored Changes
```
POST /api/v1/resume-tailoring/apply-changes
```

**Request Body:**
```json
{
  "tailoring_session_id": "uuid",
  "accepted_changes": [
    {
      "suggestion_id": "uuid",
      "action": "accept", // "accept", "reject", "modified"
      "modifications": { // Only if action is "modified"
        "suggested_text": "Custom modified text",
        "modification_reason": "User edited for clarity"
      }
    }
  ],
  "create_new_version": true,
  "version_label": "Tailored for Tech Corp - Senior Engineer"
}
```

**Response:**
```json
{
  "tailored_resume_id": "uuid",
  "original_resume_id": "uuid",
  "applied_changes_count": 8,
  "final_alignment_score": 92,
  "improvement_percentage": 27,
  "created_at": "2026-04-02T22:09:00Z"
}
```

### 4. Get Tailoring History
```
GET /api/v1/resume-tailoring/history/{resume_id}
```

**Response:**
```json
{
  "tailoring_sessions": [
    {
      "session_id": "uuid",
      "job_analysis_id": "uuid",
      "company": "Tech Corp",
      "job_title": "Senior Software Engineer",
      "alignment_before": 65,
      "alignment_after": 92,
      "applied_changes": 8,
      "created_at": "2026-04-02T22:09:00Z"
    }
  ],
  "total_sessions": 5,
  "average_improvement": 23.5
}
```

### 5. Validate Tailored Resume
```
POST /api/v1/resume-tailoring/validate
```

**Request Body:**
```json
{
  "tailored_resume_id": "uuid",
  "validation_options": {
    "check_truthfulness": true,
    "verify_evidence": true,
    "ats_compatibility": true,
    "grammar_check": true
  }
}
```

**Response:**
```json
{
  "validation_result": {
    "overall_score": 0.94,
    "truthfulness_score": 0.98,
    "evidence_verification": "passed",
    "ats_compatibility": "passed",
    "issues": [
      {
        "type": "warning",
        "message": "Some bullet points exceed recommended length",
        "location": "experience.exp_002.description"
      }
    ]
  }
}
```

## Frontend Review UX

### Review Interface Components

#### 1. Suggestion Dashboard
```
┌─────────────────────────────────────────────────────────┐
│ Resume Tailoring - Tech Corp, Senior Engineer          │
├─────────────────────────────────────────────────────────┤
│ Alignment Score: 65% → 92% (+27%)                      │
│ 12 Suggestions • 5 High Priority • 3 Medium • 4 Low    │
│                                                         │
│ [Accept All] [Accept High Priority] [Review Individually] │
└─────────────────────────────────────────────────────────┘
```

#### 2. Suggestion Card Component
```jsx
<SuggestionCard>
  <Header>
    <Type>Experience Enhancement</Type>
    <Priority>High</Priority>
    <Confidence>85%</Confidence>
  </Header>
  
  <Content>
    <OriginalText>
      "Developed web applications using Python"
    </OriginalText>
    <Arrow>→</Arrow>
    <SuggestedText>
      "Developed scalable web applications using Python and Django framework"
    </SuggestedText>
  </Content>
  
  <Evidence>
    <EvidenceTag source="Experience" confidence="95%" />
    <EvidenceTag source="Skills" confidence="80%" />
  </Evidence>
  
  <Impact>
    <AlignmentBoost>+15% skill alignment</AlignmentBoost>
    <KeywordCoverage>web applications, scalable</KeywordCoverage>
  </Impact>
  
  <Actions>
    <AcceptButton />
    <RejectButton />
    <EditButton />
  </Actions>
</SuggestionCard>
```

#### 3. Diff Preview Modal
```jsx
<DiffPreviewModal>
  <Header>
    <Title>Preview Changes</Title>
    <Summary>8 changes across 3 sections</Summary>
  </Header>
  
  <DiffContent>
    <Section name="Summary">
      <DiffLine type="unchanged">
        Software engineer with 5 years of experience
      </DiffLine>
      <DiffLine type="added" highlight="true">
        + specializing in full-stack development
      </DiffLine>
      <DiffLine type="unchanged">
        and cloud technologies
      </DiffLine>
    </Section>
    
    <Section name="Experience">
      <DiffLine type="removed">
        - Developed web applications using Python
      </DiffLine>
      <DiffLine type="added" highlight="true">
        + Developed scalable web applications using Python and Django framework
      </DiffLine>
    </Section>
  </DiffContent>
  
  <EvidencePanel>
    <EvidenceSource source="exp_001" type="Direct Experience" />
    <EvidenceSource source="skills_python" type="Skills Section" />
  </EvidencePanel>
  
  <Actions>
    <ApplyChangesButton />
    <BackToReviewButton />
  </Actions>
</DiffPreviewModal>
```

#### 4. Interactive Review Flow
```jsx
<ReviewWorkflow>
  <Step1>Generate Suggestions</Step1>
  <Step2>Review Dashboard</Step2>
  <Step3>Individual Review</Step3>
  <Step4>Preview Changes</Step4>
  <Step5>Apply & Save</Step5>
</ReviewWorkflow>
```

### User Interaction Patterns

#### Bulk Actions
- **Accept All**: Apply all suggestions with confirmation
- **Accept High Priority**: Auto-accept suggestions with high priority and confidence
- **Reject All**: Reject all suggestions
- **Custom Filter**: Filter by type, priority, or confidence

#### Individual Review
- **Quick Accept**: One-click acceptance for obvious improvements
- **Detailed Review**: Expandable view with evidence and impact
- **Inline Edit**: Edit suggestions directly in the preview
- **Evidence Inspection**: Click to view supporting evidence

#### Validation Feedback
- **Truthfulness Indicator**: Visual indicator for suggestion reliability
- **Evidence Strength**: Color-coded confidence levels
- **Impact Preview**: Show expected alignment improvement
- **Warning System**: Alert for potential issues

## Validation Rules

### Input Validation
```json
{
  "resume_validation": {
    "required_fields": ["sections", "experience", "skills"],
    "schema_compliance": "resume_schema_v2",
    "min_content_length": 500,
    "max_content_length": 50000
  },
  "job_analysis_validation": {
    "required_fields": ["parsed_jd", "fit_analysis"],
    "schema_compliance": "jd_analysis_schema_v1",
    "completeness_threshold": 0.8
  }
}
```

### Suggestion Validation
```json
{
  "suggestion_rules": {
    "evidence_requirement": {
      "min_confidence": 0.7,
      "min_sources": 1,
      "primary_source_required": true
    },
    "content_constraints": {
      "max_length_increase_percent": 30,
      "no_new_skills_fabrication": true,
      "context_preservation_required": true
    },
    "quality_thresholds": {
      "min_impact_score": 0.1,
      "min_alignment_boost": 0.02,
      "max_suggestions_per_section": 5
    }
  }
}
```

### Output Validation
```json
{
  "output_validation": {
    "resume_schema_compliance": true,
    "truthfulness_score_min": 0.85,
    "no_duplicate_content": true,
    "readability_score_min": 0.7,
    "ats_compatibility": true
  }
}
```

## Safety Checks

### Truthfulness Verification
```json
{
  "truthfulness_checks": {
    "evidence_verification": {
      "check": "All suggestions must have verifiable evidence",
      "enforcement": "strict",
      "failure_action": "reject_suggestion"
    },
    "fabrication_prevention": {
      "check": "No new skills or experience can be invented",
      "enforcement": "strict",
      "failure_action": "block_generation"
    },
    "context_integrity": {
      "check": "Original context must be preserved",
      "enforcement": "moderate",
      "failure_action": "flag_for_review"
    },
    "metric_validation": {
      "check": "Metrics must be supported by evidence",
      "enforcement": "strict",
      "failure_action": "reject_suggestion"
    }
  }
}
```

### Content Safety
```json
{
  "content_safety": {
    "bias_prevention": {
      "check": "No biased or discriminatory language",
      "enforcement": "strict",
      "failure_action": "reject_suggestion"
    },
    "professional_standards": {
      "check": "Maintain professional tone and language",
      "enforcement": "moderate",
      "failure_action": "flag_for_review"
    },
    "legal_compliance": {
      "check": "No false claims or misleading statements",
      "enforcement": "strict",
      "failure_action": "reject_suggestion"
    }
  }
}
```

### User Safety
```json
{
  "user_safety": {
    "change_transparency": {
      "check": "All changes must be clearly visible",
      "enforcement": "strict",
      "failure_action": "block_application"
    },
    "reversibility": {
      "check": "All changes must be reversible",
      "enforcement": "strict",
      "failure_action": "block_application"
    },
    "consent_required": {
      "check": "Explicit user consent required for changes",
      "enforcement": "strict",
      "failure_action": "block_application"
    }
  }
}
```

## Tests

### Unit Tests

#### Suggestion Generation Tests
```javascript
describe('Suggestion Generation', () => {
  test('should not suggest skills without evidence', () => {
    const resume = { skills: ['Python', 'JavaScript'] };
    const jd = { required_skills: ['Python', 'Django', 'AWS'] };
    
    const suggestions = generateSuggestions(resume, jd);
    
    expect(suggestions.filter(s => s.suggested_content.includes('Django'))).toHaveLength(0);
  });
  
  test('should enhance existing experience with supporting evidence', () => {
    const resume = {
      experience: [{ text: 'Developed web apps', skills: ['Python', 'Django'] }]
    };
    const jd = { required_skills: ['Python', 'Django', 'scalable'] };
    
    const suggestions = generateSuggestions(resume, jd);
    
    const enhancement = suggestions.find(s => s.type === 'experience_enhancement');
    expect(enhancement.suggested_content).toContain('scalable');
    expect(enhancement.evidence_mapping.confidence).toBeGreaterThan(0.7);
  });
});
```

#### Evidence Validation Tests
```javascript
describe('Evidence Validation', () => {
  test('should reject suggestions with insufficient evidence', () => {
    const suggestion = {
      suggested_content: 'Expert in machine learning',
      evidence_mapping: { confidence: 0.3 }
    };
    
    const validation = validateEvidence(suggestion);
    
    expect(validation.is_valid).toBe(false);
    expect(validation.reason).toContain('insufficient evidence');
  });
  
  test('should accept suggestions with strong evidence', () => {
    const suggestion = {
      suggested_content: 'Developed Python applications',
      evidence_mapping: { 
        confidence: 0.9,
        primary_evidence: { type: 'direct_experience' }
      }
    };
    
    const validation = validateEvidence(suggestion);
    
    expect(validation.is_valid).toBe(true);
  });
});
```

#### Truthfulness Tests
```javascript
describe('Truthfulness Checks', () => {
  test('should prevent fabrication of new skills', () => {
    const resume = { skills: ['Python', 'JavaScript'] };
    const suggestion = {
      type: 'skill_addition',
      suggested_skill: 'Machine Learning',
      evidence_mapping: { confidence: 0.1 }
    };
    
    const check = performTruthfulnessCheck(resume, suggestion);
    
    expect(check.passed).toBe(false);
    expect(check.violation).toBe('fabrication_prevention');
  });
  
  test('should allow enhancement of existing skills', () => {
    const resume = { skills: ['Python'] };
    const suggestion = {
      type: 'experience_enhancement',
      suggested_content: 'Advanced Python development',
      evidence_mapping: { confidence: 0.8 }
    };
    
    const check = performTruthfulnessCheck(resume, suggestion);
    
    expect(check.passed).toBe(true);
  });
});
```

### Integration Tests

#### End-to-End Flow Tests
```javascript
describe('Tailoring Workflow Integration', () => {
  test('should complete full tailoring workflow', async () => {
    const resume = createTestResume();
    const jd = createTestJobAnalysis();
    
    // Generate suggestions
    const session = await generateTailoringSession(resume.id, jd.id);
    expect(session.suggestions).toHaveLength(greaterThan(0));
    
    // Preview diff
    const diff = await previewDiff(session.id, session.suggestions.slice(0, 3));
    expect(diff.diff_view.sections).toHaveLength(greaterThan(0));
    
    // Apply changes
    const tailored = await applyChanges(session.id, [
      { suggestion_id: session.suggestions[0].id, action: 'accept' }
    ]);
    
    expect(tailored.final_alignment_score).toBeGreaterThan(resume.alignment_score);
  });
});
```

#### API Integration Tests
```javascript
describe('API Integration', () => {
  test('POST /generate-suggestions should return valid suggestions', async () => {
    const response = await request(app)
      .post('/api/v1/resume-tailoring/generate-suggestions')
      .send({
        resume_id: testResume.id,
        job_analysis_id: testJobAnalysis.id
      });
    
    expect(response.status).toBe(200);
    expect(response.body.suggestions).toBeDefined();
    expect(response.body.suggestions.length).toBeGreaterThan(0);
  });
  
  test('POST /apply-changes should create tailored resume', async () => {
    const session = await createTailoringSession();
    
    const response = await request(app)
      .post('/api/v1/resume-tailoring/apply-changes')
      .send({
        tailoring_session_id: session.id,
        accepted_changes: [
          { suggestion_id: session.suggestions[0].id, action: 'accept' }
        ]
      });
    
    expect(response.status).toBe(200);
    expect(response.body.tailored_resume_id).toBeDefined();
  });
});
```

### Performance Tests

#### Load Testing
```javascript
describe('Performance Tests', () => {
  test('should handle concurrent tailoring requests', async () => {
    const concurrentRequests = 20;
    const requests = Array(concurrentRequests).fill().map(() =>
      generateTailoringSession(testResume.id, testJobAnalysis.id)
    );
    
    const results = await Promise.all(requests);
    
    expect(results).toHaveLength(concurrentRequests);
    results.forEach(result => {
      expect(result.processing_metadata.duration_ms).toBeLessThan(5000);
    });
  });
  
  test('should process large resumes efficiently', async () => {
    const largeResume = createLargeTestResume(); // 10,000+ words
    
    const startTime = Date.now();
    const session = await generateTailoringSession(largeResume.id, testJobAnalysis.id);
    const duration = Date.now() - startTime;
    
    expect(duration).toBeLessThan(10000);
    expect(session.suggestions.length).toBeGreaterThan(0);
  });
});
```

### User Acceptance Tests

#### Usability Tests
```javascript
describe('User Experience Tests', () => {
  test('should provide clear diff preview', () => {
    const diff = generateDiffPreview(testSuggestions);
    
    expect(diff.diff_view.sections).toBeDefined();
    expect(diff.summary_statistics.total_changes).toBeGreaterThan(0);
    expect(diff.interactive_elements.accept_all_enabled).toBe(true);
  });
  
  test('should allow individual suggestion review', () => {
    const suggestions = createTestSuggestions();
    
    suggestions.forEach(suggestion => {
      expect(suggestion.evidence_mapping).toBeDefined();
      expect(suggestion.confidence_score).toBeGreaterThan(0);
      expect(suggestion.impact_score).toBeGreaterThan(0);
    });
  });
});
```

### Test Data Sets

#### Positive Test Cases
```javascript
const positiveTestCases = [
  {
    name: 'Strong skill alignment available',
    resume: { skills: ['Python', 'Django', 'AWS'], experience: ['Web development'] },
    jd: { required_skills: ['Python', 'Django'], preferred_skills: ['AWS'] },
    expected_suggestions: 5,
    expected_truthfulness_score: 0.9
  },
  {
    name: 'Partial experience enhancement',
    resume: { experience: ['Team leadership'], skills: ['Communication'] },
    jd: { required_skills: ['Leadership', 'Communication'] },
    expected_suggestions: 3,
    expected_truthfulness_score: 0.85
  }
];
```

#### Negative Test Cases
```javascript
const negativeTestCases = [
  {
    name: 'No relevant experience',
    resume: { skills: ['Marketing'], experience: ['Sales'] },
    jd: { required_skills: ['Python', 'AWS'] },
    expected_suggestions: 0,
    expected_block_reason: 'insufficient_evidence'
  },
  {
    name: 'Attempt skill fabrication',
    resume: { skills: ['JavaScript'] },
    jd: { required_skills: ['Python', 'Machine Learning'] },
    expected_suggestions: 0,
    expected_block_reason: 'fabrication_prevention'
  }
];
```

## Implementation Timeline

### Phase 1: Core Engine (2 weeks)
- Evidence mapping system
- Suggestion generation algorithms
- Truthfulness validation framework
- Basic API endpoints

### Phase 2: AI Integration (2 weeks)
- ML model integration
- Advanced evidence detection
- Confidence scoring algorithms
- Safety check implementation

### Phase 3: User Interface (2 weeks)
- Review dashboard components
- Diff preview interface
- Interactive suggestion cards
- Bulk action controls

### Phase 4: Integration & Testing (1 week)
- End-to-end workflow
- Performance optimization
- Security validation
- User acceptance testing

### Phase 5: Deployment & Monitoring (1 week)
- Production deployment
- Monitoring setup
- Documentation completion
- User training

## Success Metrics

### Technical Metrics
- **Processing Speed**: <3 seconds for suggestion generation
- **Truthfulness Score**: >90% of suggestions pass validation
- **User Acceptance Rate**: >70% of suggestions accepted
- **Error Rate**: <2% failed tailoring sessions

### User Metrics
- **Alignment Improvement**: >20% average score increase
- **User Satisfaction**: >4.5/5 rating on usefulness
- **Completion Rate**: >80% of sessions completed
- **Reuse Rate**: >60% of users use feature multiple times

## Security & Privacy

### Data Protection
- **Resume Data Encryption**: Encrypt sensitive resume content
- **Evidence Anonymization**: Remove personally identifiable information
- **Access Controls**: User-only access to their resume data
- **Data Retention**: Configurable retention policies

### Model Security
- **Prompt Injection Prevention**: Secure AI prompt engineering
- **Output Validation**: Strict validation of AI-generated content
- **Rate Limiting**: Prevent abuse and resource exhaustion
- **Audit Logging**: Track all tailoring activities
