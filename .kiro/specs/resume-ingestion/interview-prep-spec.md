# Interview Preparation Module Specification

## Overview
The Interview Preparation module generates personalized interview questions and answer drafts based on job description requirements and the user's actual background, creating comprehensive interview prep materials linked to each application.

## Goals
- Generate likely interview questions from the job description
- Generate simple answer drafts based on the user's actual background
- Generate STAR-format stories from resume experiences
- Save interview prep results under the application record

## Backend Workflow

### 1. Input Processing Stage
```
Job Analysis JSON + Tailored Resume JSON + Application Context → Content Preparation
```

**Input Sources:**
- **Job Analysis**: Parsed JD with requirements, skills, and responsibilities
- **Tailored Resume**: User's approved resume with experiences and skills
- **Application Context**: Company, role, interview type, and format

### 2. Question Generation Stage
```
Content Preparation → Question Categorization → Question Generation → Question Validation
```

**Components:**
- **Question Categorizer**: Identify question types (technical, behavioral, situational)
- **Question Generator**: Create specific questions based on JD requirements
- **Question Validator**: Ensure questions are relevant and appropriate
- **Difficulty Assessor**: Rate question difficulty and complexity

### 3. Answer Generation Stage
```
Validated Questions + Resume Data → Experience Mapping → Answer Drafting → STAR Formatting
```

**Components:**
- **Experience Mapper**: Link questions to relevant resume experiences
- **Answer Drafter**: Generate initial answer drafts
- **STAR Formatter**: Structure answers in STAR format
- **Truthfulness Validator**: Ensure answers align with actual experience

### 4. Story Generation Stage
```
Resume Experiences + JD Requirements → Story Selection → STAR Story Creation → Story Validation
```

**Components:**
- **Story Selector**: Choose best experiences for STAR stories
- **Story Creator**: Generate STAR format stories
- **Story Validator**: Ensure stories are truthful and impactful
- **Story Categorizer**: Categorize stories by question types

### 5. Output Assembly Stage
```
Questions + Answers + Stories → Content Organization → Validation → Storage
```

**Components:**
- **Content Organizer**: Structure all generated content
- **Final Validator**: Comprehensive content validation
- **Metadata Generator**: Create content metadata and analytics
- **Storage Manager**: Save to application record

## Structured Output Schema

### Main Interview Prep Response
```json
{
  "interview_prep_id": "uuid",
  "application_id": "uuid",
  "job_analysis_id": "uuid",
  "resume_id": "uuid",
  "interview_context": {
    "company": "Tech Corp",
    "position": "Senior Software Engineer",
    "interview_type": "technical",
    "interview_format": "video call",
    "duration_minutes": 60,
    "interviewers": [
      {
        "name": "Mike Chen",
        "title": "Senior Engineer",
        "role": "hiring_manager"
      }
    ]
  },
  "generated_at": "2026-04-02T22:13:00Z",
  "content_summary": {
    "total_questions": 15,
    "technical_questions": 8,
    "behavioral_questions": 4,
    "situational_questions": 3,
    "star_stories": 5,
    "estimated_prep_time_minutes": 45
  },
  "questions": [
    {
      "question_id": "uuid",
      "type": "technical",
      "category": "programming_concepts",
      "difficulty": "medium",
      "priority": "high",
      "question_text": "Can you explain how you would design a scalable REST API using Python and Django?",
      "context": "Based on JD requirement for 'scalable web applications'",
      "jd_reference": {
        "section": "responsibilities",
        "requirement": "Design and develop scalable applications",
        "importance": "high"
      },
      "answer_draft": {
        "draft": "In my previous role at Company X, I designed and implemented a scalable REST API using Django REST Framework...",
        "evidence_references": ["exp_001_api_design", "skills_django", "skills_python"],
        "confidence_score": 0.85,
        "truthfulness_score": 0.92,
        "length_words": 120,
        "estimated_speaking_time_seconds": 45
      },
      "follow_up_questions": [
        "How would you handle database optimization?",
        "What caching strategies would you implement?"
      ]
    }
  ],
  "star_stories": [
    {
      "story_id": "uuid",
      "title": "API Performance Optimization",
      "category": "technical_achievement",
      "related_questions": ["q001", "q002"],
      "situation": "We were experiencing slow response times on our customer-facing API, with average response times of 2+ seconds affecting user experience.",
      "task": "My task was to identify the performance bottlenecks and optimize the API to achieve sub-500ms response times while maintaining data integrity.",
      "action": "I analyzed the API endpoints using profiling tools, identified N+1 query problems, implemented database query optimization, added Redis caching for frequently accessed data, and introduced pagination for large datasets.",
      "result": "Reduced average API response time from 2.3 seconds to 380 milliseconds (83% improvement), increased throughput by 150%, and received positive feedback from customers about improved application responsiveness.",
      "evidence_references": ["exp_001_performance", "achievements_optimization"],
      "confidence_score": 0.95,
      "truthfulness_score": 0.98,
      "usage_tips": "Use this for questions about performance optimization, problem-solving, or technical achievements."
    }
  ],
  "preparation_guide": {
    "focus_areas": [
      {
        "area": "Python and Django",
        "importance": "high",
        "prep_time_minutes": 15,
        "key_topics": ["REST API design", "Database optimization", "Caching strategies"]
      }
    ],
    "recommended_preparation": [
      "Review your Django REST Framework projects",
      "Prepare examples of API design decisions",
      "Think about scalability challenges you've faced"
    ],
    "day_of_interview_tips": [
      "Have specific metrics ready for your API projects",
      "Prepare to discuss your decision-making process",
      "Bring up the performance optimization story"
    ]
  },
  "metadata": {
    "generation_model": "gpt-4-turbo",
    "processing_time_ms": 3200,
    "content_quality_score": 0.88,
    "personalization_score": 0.91,
    "truthfulness_score": 0.93
  }
}
```

### Question Schema
```json
{
  "question_id": "uuid",
  "type": "technical", // "technical", "behavioral", "situational", "case_study"
  "category": "programming_concepts", // "programming_concepts", "system_design", "problem_solving", "leadership", "teamwork", "conflict_resolution"
  "difficulty": "medium", // "easy", "medium", "hard"
  "priority": "high", // "high", "medium", "low"
  "question_text": "Can you explain how you would design a scalable REST API using Python and Django?",
  "context": "Based on JD requirement for 'scalable web applications'",
  "jd_reference": {
    "section": "responsibilities",
    "requirement": "Design and develop scalable applications",
    "importance": "high",
    "keywords": ["scalable", "API", "Python", "Django"]
  },
  "answer_draft": {
    "draft": "In my previous role at Company X, I designed and implemented a scalable REST API using Django REST Framework...",
    "evidence_references": ["exp_001_api_design", "skills_django", "skills_python"],
    "confidence_score": 0.85,
    "truthfulness_score": 0.92,
    "length_words": 120,
    "estimated_speaking_time_seconds": 45,
    "key_points": [
      "Experience with Django REST Framework",
      "Understanding of scalability principles",
      "Real-world implementation examples"
    ]
  },
  "follow_up_questions": [
    {
      "question": "How would you handle database optimization?",
      "type": "technical_follow_up",
      "difficulty": "medium"
    },
    {
      "question": "What caching strategies would you implement?",
      "type": "technical_follow_up",
      "difficulty": "medium"
    }
  ],
  "related_experiences": [
    {
      "experience_id": "exp_001",
      "title": "Senior Software Engineer",
      "company": "Company X",
      "relevance_score": 0.9,
      "shared_skills": ["Python", "Django", "API design"]
    }
  ]
}
```

### STAR Story Schema
```json
{
  "story_id": "uuid",
  "title": "API Performance Optimization",
  "category": "technical_achievement", // "technical_achievement", "leadership", "problem_solving", "teamwork", "innovation", "conflict_resolution"
  "related_questions": ["q001", "q002", "q005"],
  "situation": {
    "text": "We were experiencing slow response times on our customer-facing API, with average response times of 2+ seconds affecting user experience.",
    "duration": "3 months",
    "impact": "High - affecting customer satisfaction",
    "complexity": "Medium - involved multiple system components"
  },
  "task": {
    "text": "My task was to identify the performance bottlenecks and optimize the API to achieve sub-500ms response times while maintaining data integrity.",
    "objectives": [
      "Reduce API response time to under 500ms",
      "Maintain data integrity and accuracy",
      "Minimize disruption to existing services"
    ],
    "constraints": [
      "Could not break existing functionality",
      "Limited downtime window",
      "Team coordination required"
    ]
  },
  "action": {
    "text": "I analyzed the API endpoints using profiling tools, identified N+1 query problems, implemented database query optimization, added Redis caching for frequently accessed data, and introduced pagination for large datasets.",
    "steps": [
      "Set up performance monitoring and profiling",
      "Identified database query bottlenecks",
      "Optimized database queries and added indexes",
      "Implemented Redis caching layer",
      "Added pagination to large dataset endpoints",
      "Conducted load testing and validation"
    ],
    "skills_demonstrated": [
      "Performance analysis",
      "Database optimization",
      "Caching strategies",
      "Problem-solving"
    ],
    "tools_used": ["Django Debug Toolbar", "Redis", "PostgreSQL", "JMeter"]
  },
  "result": {
    "text": "Reduced average API response time from 2.3 seconds to 380 milliseconds (83% improvement), increased throughput by 150%, and received positive feedback from customers about improved application responsiveness.",
    "metrics": [
      {
        "metric": "API Response Time",
        "before": "2.3 seconds",
        "after": "380 milliseconds",
        "improvement": "83%"
      },
      {
        "metric": "Throughput",
        "before": "1000 requests/minute",
        "after": "2500 requests/minute",
        "improvement": "150%"
      }
    ],
    "impact": "Significant improvement in user experience and system capacity",
    "recognition": "Received team award for technical excellence",
    "lessons_learned": "Importance of performance monitoring and proactive optimization"
  },
  "evidence_references": ["exp_001_performance", "achievements_optimization", "skills_performance"],
  "confidence_score": 0.95,
  "truthfulness_score": 0.98,
  "usage_tips": [
    "Use this for questions about performance optimization",
    "Emphasize the measurable results",
    "Highlight your systematic approach to problem-solving"
  ],
  "alternative_versions": [
    {
      "focus": "leadership",
      "modifications": "Emphasize coordinating with team members and communicating with stakeholders"
    },
    {
      "focus": "technical_depth",
      "modifications": "Go deeper into technical implementation details and specific optimizations"
    }
  ]
}
```

### Preparation Guide Schema
```json
{
  "focus_areas": [
    {
      "area": "Python and Django",
      "importance": "high",
      "prep_time_minutes": 15,
      "key_topics": [
        "REST API design principles",
        "Database optimization techniques",
        "Caching strategies and implementation",
        "Django REST Framework features"
      ],
      "related_questions": ["q001", "q002", "q003"],
      "related_stories": ["story_001"],
      "preparation_resources": [
        "Review your Django projects",
        "Study REST API best practices",
        "Prepare specific examples of optimizations"
      ]
    }
  ],
  "recommended_preparation": [
    "Review your Django REST Framework projects and be ready to discuss specific design decisions",
    "Prepare concrete examples of how you've handled scalability challenges",
    "Think about times you've improved system performance and have metrics ready",
    "Review the job description and align your examples with their requirements"
  ],
  "day_of_interview_tips": [
    "Have specific metrics ready for your API projects (response times, throughput, etc.)",
    "Prepare to discuss your decision-making process and trade-offs",
    "Bring up the performance optimization story when asked about problem-solving",
    "Be ready to discuss how you'd approach similar challenges at their company"
  ],
  "common_mistakes_to_avoid": [
    "Don't speak in generalities - use specific examples from your experience",
    "Avoid claiming expertise you don't have - be honest about your experience level",
    "Don't forget to mention the business impact of your technical work",
    "Avoid being too technical without explaining the business value"
  ],
  "estimated_total_prep_time_minutes": 45
}
```

## Backend API Endpoints

### 1. Generate Interview Preparation
```
POST /api/v1/interview-prep/generate
```

**Request Body:**
```json
{
  "application_id": "uuid",
  "job_analysis_id": "uuid",
  "resume_id": "uuid",
  "interview_context": {
    "interview_type": "technical", // "technical", "behavioral", "mixed", "case_study"
    "interview_format": "video call", // "video call", "phone", "onsite", "panel"
    "duration_minutes": 60,
    "interviewers": [
      {
        "name": "Mike Chen",
        "title": "Senior Engineer",
        "role": "hiring_manager"
      }
    ]
  },
  "generation_options": {
    "question_types": ["technical", "behavioral", "situational"],
    "difficulty_level": "medium", // "easy", "medium", "hard"
    "max_questions": 15,
    "include_star_stories": true,
    "max_star_stories": 5,
    "focus_areas": ["python", "django", "api_design"]
  }
}
```

**Response:**
```json
{
  "interview_prep_id": "uuid",
  "status": "completed",
  "generated_at": "2026-04-02T22:13:00Z",
  "interview_prep": { ... } // Full interview prep schema
}
```

### 2. Get Interview Preparation
```
GET /api/v1/interview-prep/{interview_prep_id}
```

**Response:**
```json
{
  "interview_prep_id": "uuid",
  "application_id": "uuid",
  "interview_prep": { ... }, // Full interview prep content
  "created_at": "2026-04-02T22:13:00Z",
  "updated_at": "2026-04-02T22:13:00Z",
  "last_accessed_at": "2026-04-02T22:15:00Z"
}
```

### 3. Update Interview Preparation
```
PUT /api/v1/interview-prep/{interview_prep_id}
```

**Request Body:**
```json
{
  "updates": {
    "questions": [
      {
        "question_id": "uuid",
        "answer_draft": {
          "draft": "Updated answer draft based on user feedback...",
          "user_modifications": "Added more specific examples"
        }
      }
    ],
    "star_stories": [
      {
        "story_id": "uuid",
        "result": {
          "text": "Updated result with additional metrics..."
        }
      }
    ],
    "preparation_guide": {
      "recommended_preparation": [
        "Updated preparation tip..."
      ]
    }
  },
  "change_reason": "User requested more specific examples"
}
```

**Response:**
```json
{
  "interview_prep_id": "uuid",
  "updated_fields": ["questions", "star_stories"],
  "updated_at": "2026-04-02T22:20:00Z",
  "interview_prep": { ... } // Updated full content
}
```

### 4. Get Application Interview Prep
```
GET /api/v1/interview-prep/application/{application_id}
```

**Response:**
```json
{
  "application_id": "uuid",
  "interview_preps": [
    {
      "interview_prep_id": "uuid",
      "interview_type": "technical",
      "created_at": "2026-04-02T22:13:00Z",
      "content_summary": {
        "total_questions": 15,
        "star_stories": 5,
        "estimated_prep_time_minutes": 45
      }
    }
  ]
}
```

### 5. Delete Interview Preparation
```
DELETE /api/v1/interview-prep/{interview_prep_id}
```

**Response:**
```json
{
  "interview_prep_id": "uuid",
  "deleted": true,
  "deleted_at": "2026-04-02T22:25:00Z"
}
```

### 6. Generate Additional Questions
```
POST /api/v1/interview-prep/{interview_prep_id}/additional-questions
```

**Request Body:**
```json
{
  "focus_areas": ["system_design", "leadership"],
  "question_types": ["technical", "behavioral"],
  "max_questions": 5,
  "difficulty_level": "hard"
}
```

**Response:**
```json
{
  "additional_questions": [
    {
      "question_id": "uuid",
      "type": "technical",
      "question_text": "How would you design a system to handle 1 million concurrent users?",
      "answer_draft": { ... }
    }
  ],
  "generated_at": "2026-04-02T22:30:00Z"
}
```

## UI Design for Reading Interview Prep

### Main Interview Prep View
```jsx
<InterviewPrepView>
  <Header>
    <Title>Interview Preparation</Title>
    <InterviewContext 
      company="Tech Corp"
      position="Senior Software Engineer"
      type="Technical Interview"
      format="Video Call"
      duration="60 minutes"
    />
    <PrepSummary>
      <Metric label="Questions" value="15" />
      <Metric label="STAR Stories" value="5" />
      <Metric label="Prep Time" value="45 min" />
    </PrepSummary>
  </Header>
  
  <Tabs>
    <Tab label="Questions" badge={15}>
      <QuestionsView>
        <FilterBar>
          <QuestionTypeFilter options={["All", "Technical", "Behavioral", "Situational"]} />
          <DifficultyFilter options={["All", "Easy", "Medium", "Hard"]} />
          <PriorityFilter options={["All", "High", "Medium", "Low"]} />
          <CategoryFilter options={categories} />
        </FilterBar>
        
        <QuestionsList>
          <QuestionCard question={question1}>
            <QuestionHeader>
              <TypeBadge type="technical" />
              <DifficultyBadge difficulty="medium" />
              <PriorityBadge priority="high" />
            </QuestionHeader>
            
            <QuestionText>
              Can you explain how you would design a scalable REST API using Python and Django?
            </QuestionText>
            
            <JDContext>
              <ContextLabel>Based on JD requirement:</ContextLabel>
              <ContextText>"Design and develop scalable applications"</ContextText>
            </JDContext>
            
            <AnswerSection>
              <AnswerHeader>
                <AnswerLabel>Suggested Answer</AnswerLabel>
                <TruthfulnessIndicator score={0.92} />
                <ConfidenceIndicator score={0.85} />
              </AnswerHeader>
              
              <AnswerText>
                In my previous role at Company X, I designed and implemented a scalable REST API...
              </AnswerText>
              
              <EvidenceReferences>
                <ReferenceTag experience="exp_001" label="API Design Experience" />
                <ReferenceTag skill="python" label="Python" />
                <ReferenceTag skill="django" label="Django" />
              </EvidenceReferences>
              
              <AnswerMetrics>
                <Metric label="Words" value="120" />
                <Metric label="Speaking Time" value="45 sec" />
              </AnswerMetrics>
            </AnswerSection>
            
            <FollowUpQuestions>
              <FollowUpQuestion question="How would you handle database optimization?" />
              <FollowUpQuestion question="What caching strategies would you implement?" />
            </FollowUpQuestions>
            
            <Actions>
              <EditButton />
              <PracticeButton />
              <BookmarkButton />
            </Actions>
          </QuestionCard>
        </QuestionsList>
      </QuestionsView>
    </Tab>
    
    <Tab label="STAR Stories" badge={5}>
      <StoriesView>
        <StoriesGrid>
          <StoryCard story={story1}>
            <StoryHeader>
              <StoryTitle>API Performance Optimization</StoryTitle>
              <CategoryBadge category="technical_achievement" />
              <TruthfulnessIndicator score={0.98} />
            </StoryHeader>
            
            <StoryPreview>
              <PreviewText>
                Reduced API response time from 2.3 seconds to 380 milliseconds...
              </PreviewText>
              <MetricsPreview>
                <Metric label="Improvement" value="83%" />
                <Metric label="Throughput" value="+150%" />
              </MetricsPreview>
            </StoryPreview>
            
            <RelatedQuestions>
              <QuestionTag questionId="q001" />
              <QuestionTag questionId="q002" />
            </RelatedQuestions>
            
            <Actions>
              <ViewFullStoryButton />
              <PracticeButton />
              <EditButton />
            </Actions>
          </StoryCard>
        </StoriesGrid>
      </StoriesView>
    </Tab>
    
    <Tab label="Preparation Guide">
      <PreparationGuideView>
        <FocusAreas>
          <SectionTitle>Focus Areas</SectionTitle>
          <FocusAreaCard area={focusArea1}>
            <AreaHeader>
              <AreaName>Python and Django</AreaName>
              <ImportanceBadge importance="high" />
              <PrepTimeBadge time="15 min" />
            </AreaHeader>
            
            <KeyTopics>
              <Topic>REST API design principles</Topic>
              <Topic>Database optimization techniques</Topic>
              <Topic>Caching strategies and implementation</Topic>
            </KeyTopics>
            
            <RelatedContent>
              <RelatedQuestions count={3} />
              <RelatedStories count={1} />
            </RelatedContent>
            
            <PreparationResources>
              <Resource>Review your Django projects</Resource>
              <Resource>Study REST API best practices</Resource>
            </PreparationResources>
          </FocusAreaCard>
        </FocusAreas>
        
        <RecommendedPreparation>
          <SectionTitle>Recommended Preparation</SectionTitle>
          <PreparationList>
            <PreparationItem>
              Review your Django REST Framework projects and be ready to discuss specific design decisions
            </PreparationItem>
            <PreparationItem>
              Prepare concrete examples of how you've handled scalability challenges
            </PreparationItem>
          </PreparationList>
        </RecommendedPreparation>
        
        <DayOfInterviewTips>
          <SectionTitle>Day of Interview Tips</SectionTitle>
          <TipsList>
            <Tip>Have specific metrics ready for your API projects</Tip>
            <Tip>Prepare to discuss your decision-making process</Tip>
          </TipsList>
        </DayOfInterviewTips>
        
        <CommonMistakes>
          <SectionTitle>Common Mistakes to Avoid</SectionTitle>
          <MistakesList>
            <Mistake>Don't speak in generalities - use specific examples</Mistake>
            <Mistake>Avoid claiming expertise you don't have</Mistake>
          </MistakesList>
        </CommonMistakes>
      </PreparationGuideView>
    </Tab>
    
    <Tab label="Practice Mode">
      <PracticeMode>
        <PracticeSetup>
          <QuestionSelector />
          <TimerSettings />
          <PracticeModeOptions />
        </PracticeSetup>
        
        <PracticeInterface>
          <QuestionDisplay />
          <AnswerRecorder />
          <PlaybackControls />
          <FeedbackPanel />
        </PracticeInterface>
      </PracticeMode>
    </Tab>
  </Tabs>
  
  <ActionBar>
    <RegenerateButton />
    <ExportButton formats={["PDF", "Print"]} />
    <ShareButton />
    <PrintButton />
  </ActionBar>
</InterviewPrepView>
```

### STAR Story Detail View
```jsx
<StoryDetailView>
  <StoryHeader>
    <StoryTitle>API Performance Optimization</StoryTitle>
    <CategoryBadge category="technical_achievement" />
    <TruthfulnessIndicator score={0.98} />
    <EditButton />
  </StoryHeader>
  
  <StoryContent>
    <STARSection>
      <SectionHeader>
        <SectionTitle>Situation</SectionTitle>
        <DurationBadge duration="3 months" />
        <ImpactBadge impact="High" />
      </SectionHeader>
      <SituationText>
        We were experiencing slow response times on our customer-facing API, with average response times of 2+ seconds affecting user experience.
      </SituationText>
    </STARSection>
    
    <STARSection>
      <SectionHeader>
        <SectionTitle>Task</SectionTitle>
      </SectionHeader>
      <TaskText>
        My task was to identify the performance bottlenecks and optimize the API to achieve sub-500ms response times while maintaining data integrity.
      </TaskText>
      <ObjectivesList>
        <Objective>Reduce API response time to under 500ms</Objective>
        <Objective>Maintain data integrity and accuracy</Objective>
      </ObjectivesList>
    </STARSection>
    
    <STARSection>
      <SectionHeader>
        <SectionTitle>Action</SectionTitle>
      </SectionHeader>
      <ActionText>
        I analyzed the API endpoints using profiling tools, identified N+1 query problems, implemented database query optimization...
      </ActionText>
      <StepsList>
        <Step>Set up performance monitoring and profiling</Step>
        <Step>Identified database query bottlenecks</Step>
      </StepsList>
      <SkillsDemonstrated>
        <Skill>Performance analysis</Skill>
        <Skill>Database optimization</Skill>
      </SkillsDemonstrated>
    </STARSection>
    
    <STARSection>
      <SectionHeader>
        <SectionTitle>Result</SectionTitle>
      </SectionHeader>
      <ResultText>
        Reduced average API response time from 2.3 seconds to 380 milliseconds (83% improvement)...
      </ResultText>
      <MetricsTable>
        <MetricRow metric="API Response Time" before="2.3 seconds" after="380 milliseconds" improvement="83%" />
        <MetricRow metric="Throughput" before="1000 req/min" after="2500 req/min" improvement="150%" />
      </MetricsTable>
    </STARSection>
  </StoryContent>
  
  <EvidencePanel>
    <EvidenceHeader>Supporting Evidence</EvidenceHeader>
    <EvidenceList>
      <EvidenceItem type="experience" id="exp_001" label="Senior Software Engineer at Company X" />
      <EvidenceItem type="achievement" id="ach_001" label="Performance optimization award" />
    </EvidenceList>
  </EvidencePanel>
  
  <UsageTips>
    <TipsHeader>Usage Tips</TipsHeader>
    <TipsList>
      <Tip>Use this for questions about performance optimization</Tip>
      <Tip>Emphasize the measurable results</Tip>
    </TipsList>
  </UsageTips>
  
  <RelatedContent>
    <RelatedHeader>Related Questions</RelatedHeader>
    <RelatedQuestions>
      <QuestionLink id="q001" text="How do you approach performance optimization?" />
      <QuestionLink id="q002" text="Tell me about a time you improved system performance." />
    </RelatedQuestions>
  </RelatedContent>
</StoryDetailView>
```

## Validation Rules

### Input Validation
```json
{
  "input_validation": {
    "application_id": {
      "required": true,
      "exists_in_applications": true,
      "belongs_to_user": true
    },
    "job_analysis_id": {
      "required": true,
      "exists_in_job_analyses": true,
      "matches_application": true
    },
    "resume_id": {
      "required": true,
      "exists_in_resumes": true,
      "matches_application": true
    },
    "interview_context": {
      "interview_type": {
        "required": true,
        "enum": ["technical", "behavioral", "mixed", "case_study"]
      },
      "interview_format": {
        "required": true,
        "enum": ["video call", "phone", "onsite", "panel"]
      },
      "duration_minutes": {
        "required": true,
        "min": 15,
        "max": 240
      }
    },
    "generation_options": {
      "max_questions": {
        "min": 5,
        "max": 50,
        "default": 15
      },
      "max_star_stories": {
        "min": 1,
        "max": 20,
        "default": 5
      }
    }
  }
}
```

### Content Generation Validation
```json
{
  "content_validation": {
    "questions": {
      "question_text": {
        "required": true,
        "min_length": 10,
        "max_length": 500,
        "appropriate_for_interview": true
      },
      "type": {
        "required": true,
        "enum": ["technical", "behavioral", "situational", "case_study"]
      },
      "difficulty": {
        "required": true,
        "enum": ["easy", "medium", "hard"]
      },
      "answer_draft": {
        "draft": {
          "required": true,
          "min_length": 50,
          "max_length": 1000,
          "based_on_resume": true
        },
        "evidence_references": {
          "required": true,
          "min_items": 1,
          "valid_references": true
        },
        "truthfulness_score": {
          "required": true,
          "min": 0.7
        }
      }
    },
    "star_stories": {
      "situation": {
        "required": true,
        "min_length": 20,
        "based_on_experience": true
      },
      "task": {
        "required": true,
        "min_length": 20,
        "achievable": true
      },
      "action": {
        "required": true,
        "min_length": 50,
        "specific_actions": true
      },
      "result": {
        "required": true,
        "min_length": 20,
        "measurable_impact": true
      },
      "truthfulness_score": {
        "required": true,
        "min": 0.8
      }
    }
  }
}
```

### Output Validation
```json
{
  "output_validation": {
    "interview_prep": {
      "required_sections": ["questions", "star_stories", "preparation_guide"],
      "min_questions": 5,
      "max_questions": 50,
      "min_star_stories": 1,
      "max_star_stories": 20,
      "content_quality_score_min": 0.7,
      "personalization_score_min": 0.6,
      "truthfulness_score_min": 0.8
    },
    "metadata": {
      "generation_model": {
        "required": true,
        "valid_model": true
      },
      "processing_time_ms": {
        "required": true,
        "max": 30000
      },
      "content_quality_score": {
        "required": true,
        "min": 0.7
      }
    }
  }
}
```

## Test Cases

### Unit Tests

#### Question Generation Tests
```javascript
describe('Question Generation', () => {
  test('should generate technical questions based on JD requirements', async () => {
    const jobAnalysis = createTestJobAnalysis({
      required_skills: ['Python', 'Django', 'REST API'],
      responsibilities: ['Design scalable applications']
    });
    const resume = createTestResume({
      experience: ['Python development', 'API design'],
      skills: ['Python', 'Django']
    });
    
    const result = await generateInterviewPrep({
      job_analysis_id: jobAnalysis.id,
      resume_id: resume.id,
      generation_options: {
        question_types: ['technical'],
        max_questions: 10
      }
    });
    
    expect(result.questions).toHaveLength(10);
    result.questions.forEach(question => {
      expect(question.type).toBe('technical');
      expect(question.answer_draft.evidence_references).not.toHaveLength(0);
      expect(question.answer_draft.truthfulness_score).toBeGreaterThan(0.7);
    });
  });
  
  test('should generate appropriate difficulty levels', async () => {
    const result = await generateInterviewPrep({
      generation_options: {
        difficulty_level: 'medium',
        max_questions: 5
      }
    });
    
    result.questions.forEach(question => {
      expect(question.difficulty).toBe('medium');
    });
  });
  
  test('should not generate questions without resume evidence', async () => {
    const jobAnalysis = createTestJobAnalysis({
      required_skills: ['Machine Learning', 'AI']
    });
    const resume = createTestResume({
      skills: ['Python', 'JavaScript'] // No ML/AI experience
    });
    
    const result = await generateInterviewPrep({
      job_analysis_id: jobAnalysis.id,
      resume_id: resume.id
    });
    
    // Should not generate questions about ML/AI
    const mlQuestions = result.questions.filter(q => 
      q.question_text.toLowerCase().includes('machine learning') ||
      q.question_text.toLowerCase().includes('ai')
    );
    expect(mlQuestions).toHaveLength(0);
  });
});
```

#### STAR Story Generation Tests
```javascript
describe('STAR Story Generation', () => {
  test('should generate STAR stories from resume experiences', async () => {
    const resume = createTestResume({
      experience: [
        {
          title: 'Senior Software Engineer',
          achievements: ['Reduced API response time by 80%', 'Led team of 5 developers']
        }
      ]
    });
    
    const result = await generateInterviewPrep({
      resume_id: resume.id,
      generation_options: {
        include_star_stories: true,
        max_star_stories: 3
      }
    });
    
    expect(result.star_stories).toHaveLength(3);
    result.star_stories.forEach(story => {
      expect(story.situation).toBeDefined();
      expect(story.task).toBeDefined();
      expect(story.action).toBeDefined();
      expect(story.result).toBeDefined();
      expect(story.truthfulness_score).toBeGreaterThan(0.8);
    });
  });
  
  test('should include measurable results in STAR stories', async () => {
    const result = await generateInterviewPrep({
      generation_options: { include_star_stories: true }
    });
    
    result.star_stories.forEach(story => {
      expect(story.result.metrics).toBeDefined();
      expect(story.result.metrics.length).toBeGreaterThan(0);
      story.result.metrics.forEach(metric => {
        expect(metric.before).toBeDefined();
        expect(metric.after).toBeDefined();
        expect(metric.improvement).toBeDefined();
      });
    });
  });
  
  test('should validate STAR story truthfulness', async () => {
    const result = await generateInterviewPrep({
      generation_options: { include_star_stories: true }
    });
    
    result.star_stories.forEach(story => {
      expect(story.truthfulness_score).toBeGreaterThan(0.8);
      expect(story.evidence_references).not.toHaveLength(0);
    });
  });
});
```

#### Answer Draft Generation Tests
```javascript
describe('Answer Draft Generation', () => {
  test('should generate answer drafts based on resume evidence', async () => {
    const result = await generateInterviewPrep();
    
    result.questions.forEach(question => {
      expect(question.answer_draft.draft).toBeDefined();
      expect(question.answer_draft.draft.length).toBeGreaterThan(50);
      expect(question.answer_draft.evidence_references).not.toHaveLength(0);
      expect(question.answer_draft.truthfulness_score).toBeGreaterThan(0.7);
    });
  });
  
  test('should estimate appropriate speaking time', async () => {
    const result = await generateInterviewPrep();
    
    result.questions.forEach(question => {
      const wordsPerMinute = 150;
      const estimatedTime = (question.answer_draft.length_words / wordsPerMinute) * 60;
      expect(question.answer_draft.estimated_speaking_time_seconds).toBeCloseTo(estimatedTime, 10);
    });
  });
  
  test('should include relevant evidence references', async () => {
    const result = await generateInterviewPrep();
    
    result.questions.forEach(question => {
      question.answer_draft.evidence_references.forEach(ref => {
        expect(ref).toMatch(/^(exp_|skill_|ach_)/); // Valid reference format
      });
    });
  });
});
```

### Integration Tests

#### End-to-End Workflow Tests
```javascript
describe('Interview Prep Workflow', () => {
  test('should complete full interview prep generation workflow', async () => {
    const application = await createTestApplication();
    const jobAnalysis = await createTestJobAnalysis();
    const resume = await createTestResume();
    
    // Generate interview prep
    const prepResult = await generateInterviewPrep({
      application_id: application.id,
      job_analysis_id: jobAnalysis.id,
      resume_id: resume.id
    });
    
    expect(prepResult.interview_prep_id).toBeDefined();
    expect(prepResult.questions).not.toHaveLength(0);
    expect(prepResult.star_stories).not.toHaveLength(0);
    
    // Retrieve interview prep
    const retrieved = await getInterviewPrep(prepResult.interview_prep_id);
    expect(retrieved.interview_prep_id).toBe(prepResult.interview_prep_id);
    
    // Update interview prep
    const updated = await updateInterviewPrep(prepResult.interview_prep_id, {
      updates: {
        questions: [
          {
            question_id: prepResult.questions[0].question_id,
            answer_draft: {
              draft: "Updated answer with more specific examples..."
            }
          }
        ]
      }
    });
    
    expect(updated.updated_fields).toContain('questions');
  });
});
```

#### API Integration Tests
```javascript
describe('API Integration', () => {
  test('POST /interview-prep/generate should return valid interview prep', async () => {
    const response = await request(app)
      .post('/api/v1/interview-prep/generate')
      .send({
        application_id: testApplication.id,
        job_analysis_id: testJobAnalysis.id,
        resume_id: testResume.id,
        interview_context: {
          interview_type: 'technical',
          interview_format: 'video call',
          duration_minutes: 60
        }
      });
    
    expect(response.status).toBe(200);
    expect(response.body.interview_prep_id).toBeDefined();
    expect(response.body.interview_prep.questions).toBeDefined();
    expect(response.body.interview_prep.star_stories).toBeDefined();
  });
  
  test('GET /interview-prep/{id} should return interview prep details', async () => {
    const prep = await createTestInterviewPrep();
    
    const response = await request(app)
      .get(`/api/v1/interview-prep/${prep.interview_prep_id}`);
    
    expect(response.status).toBe(200);
    expect(response.body.interview_prep_id).toBe(prep.interview_prep_id);
    expect(response.body.interview_prep).toBeDefined();
  });
});
```

### Performance Tests

#### Load Testing
```javascript
describe('Performance Tests', () => {
  test('should handle concurrent interview prep generation', async () => {
    const concurrentRequests = 10;
    const requests = Array(concurrentRequests).fill().map(() =>
      generateInterviewPrep({
        application_id: testApplication.id,
        job_analysis_id: testJobAnalysis.id,
        resume_id: testResume.id
      })
    );
    
    const results = await Promise.all(requests);
    
    expect(results).toHaveLength(concurrentRequests);
    results.forEach(result => {
      expect(result.interview_prep_id).toBeDefined();
      expect(result.metadata.processing_time_ms).toBeLessThan(10000);
    });
  });
  
  test('should maintain quality under load', async () => {
    const results = await Promise.all(
      Array(5).fill().map(() => generateInterviewPrep())
    );
    
    results.forEach(result => {
      expect(result.metadata.content_quality_score).toBeGreaterThan(0.7);
      expect(result.metadata.truthfulness_score).toBeGreaterThan(0.8);
    });
  });
});
```

### User Acceptance Tests

#### Usability Tests
```javascript
describe('User Experience Tests', () => {
  test('should provide intuitive question categorization', () => {
    const prep = createTestInterviewPrep();
    const component = mount(<QuestionsView questions={prep.questions} />);
    
    // Should have filtering options
    expect(component.find('[data-testid="question-type-filter"]')).toHaveLength(1);
    expect(component.find('[data-testid="difficulty-filter"]')).toHaveLength(1);
    
    // Should display question metadata
    component.find('QuestionCard').forEach(card => {
      expect(card.find('[data-testid="type-badge"]')).toHaveLength(1);
      expect(card.find('[data-testid="difficulty-badge"]')).toHaveLength(1);
    });
  });
  
  test('should show clear evidence references', () => {
    const question = createTestQuestion();
    const component = mount(<QuestionCard question={question} />);
    
    expect(component.find('[data-testid="evidence-references"]')).toHaveLength(1);
    expect(component.find('[data-testid="truthfulness-indicator"]')).toHaveLength(1);
  });
});
```

### Test Data Sets

#### Positive Test Cases
```javascript
const positiveTestCases = [
  {
    name: 'Technical interview with strong Python background',
    job_analysis: {
      required_skills: ['Python', 'Django', 'REST API'],
      responsibilities: ['Design scalable applications']
    },
    resume: {
      experience: ['5 years Python development', 'API design'],
      skills: ['Python', 'Django', 'REST']
    },
    interview_context: {
      interview_type: 'technical',
      duration_minutes: 60
    },
    expected_outcome: 'High-quality technical questions with relevant answer drafts'
  },
  {
    name: 'Behavioral interview with leadership experience',
    job_analysis: {
      required_skills: ['Leadership', 'Communication'],
      responsibilities: ['Lead development team']
    },
    resume: {
      experience: ['Team lead for 3 years', 'Cross-functional collaboration'],
      achievements: ['Led team of 5 developers']
    },
    interview_context: {
      interview_type: 'behavioral',
      duration_minutes: 45
    },
    expected_outcome: 'Behavioral questions with leadership-focused STAR stories'
  }
];
```

#### Negative Test Cases
```javascript
const negativeTestCases = [
  {
    name: 'No relevant experience for required skills',
    job_analysis: {
      required_skills: ['Machine Learning', 'Deep Learning'],
      responsibilities: ['Develop ML models']
    },
    resume: {
      experience: ['Web development'],
      skills: ['JavaScript', 'React']
    },
    expected_outcome: 'Limited questions, focus on transferable skills'
  },
  {
    name: 'Incomplete resume data',
    job_analysis: {
      required_skills: ['Python']
    },
    resume: {
      experience: [],
      skills: [],
      achievements: []
    },
    expected_outcome: 'Generic questions with minimal personalization'
  }
];
```

## Implementation Tasks

### Phase 1: Core Generation Engine (2 weeks)
- [ ] **Design interview prep pipeline** - Architecture for content generation
- [ ] **Implement question generation service** - Create question generation logic
- [ ] **Build answer drafting engine** - Generate answer drafts based on resume
- [ ] **Create STAR story generator** - Generate STAR format stories
- [ ] **Implement evidence mapping** - Link content to resume sources
- [ ] **Add truthfulness validation** - Ensure content accuracy
- [ ] **Create content organization** - Structure generated content
- [ ] **Build metadata generation** - Create content analytics

### Phase 2: API Development (1 week)
- [ ] **Implement generation endpoint** - POST /interview-prep/generate
- [ ] **Create retrieval endpoints** - GET interview prep content
- [ ] **Build update endpoints** - Modify generated content
- [ ] **Add deletion endpoints** - Remove interview prep
- [ ] **Implement application linking** - Link to application records
- [ ] **Create additional question generation** - Generate extra questions
- [ ] **Add content validation** - Validate generated content
- [ ] **Implement error handling** - Graceful error responses

### Phase 3: Frontend Development (2 weeks)
- [ ] **Build main interview prep view** - Primary content display
- [ ] **Create questions view** - Question list and filtering
- [ ] **Implement STAR stories view** - Story display and management
- [ ] **Build preparation guide** - Focus areas and tips
- [ ] **Add practice mode** - Interview practice functionality
- [ ] **Create content editing** - Edit questions and answers
- [ ] **Implement export functionality** - PDF and print options
- [ ] **Add responsive design** - Mobile-friendly interface

### Phase 4: Integration & Testing (1 week)
- [ ] **End-to-end workflow testing** - Complete generation to display
- [ ] **Performance optimization** - Improve generation speed
- [ ] **Content quality validation** - Ensure high-quality output
- [ ] **User acceptance testing** - Validate user experience
- [ ] **Cross-browser testing** - Ensure compatibility
- [ ] **Mobile testing** - Validate responsive design
- [ ] **Security validation** - Ensure data protection
- [ ] **Documentation completion** - API and user docs

### Phase 5: Deployment & Monitoring (1 week)
- [ ] **Production deployment** - Deploy to production
- [ ] **Set up monitoring** - Track performance and usage
- [ ] **Create user guides** - Help documentation
- [ ] **Implement analytics** - Track user engagement
- [ ] **Set up backup systems** - Data protection
- [ ] **Create support processes** - User support
- [ ] **Launch preparation** - Final checks
- [ ] **Post-launch monitoring** - Track success metrics
