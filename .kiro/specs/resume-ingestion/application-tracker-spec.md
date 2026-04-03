# Application Tracker Module Specification

## Overview
The Application Tracker module provides a simple, intuitive system for users to track job applications throughout the entire application process, linking all related documents and activities in one centralized location.

## Goals
- Allow users to track applications by company, role, date, and status
- Link each application to job description, tailored resume, cover letter, outreach draft, and interview prep
- Keep the tracker simple and easy to use for repeated job applications

## Status Flow
```
planned → applied → interview → (rejected | offer)
```

**Status Definitions:**
- **planned**: Application identified but not yet submitted
- **applied**: Application submitted to company
- **interview**: Interview scheduled or in progress
- **rejected**: Application rejected by company
- **offer**: Job offer received from company

## Data Model

### Core Application Entity
```json
{
  "application_id": "uuid",
  "user_id": "uuid",
  "company": {
    "name": "Tech Corp",
    "website": "https://techcorp.com",
    "industry": "technology",
    "size": "mid-size",
    "location": "San Francisco, CA",
    "remote_policy": "hybrid"
  },
  "position": {
    "title": "Senior Software Engineer",
    "level": "senior",
    "department": "engineering",
    "employment_type": "full-time",
    "salary_range": {
      "min": 120000,
      "max": 180000,
      "currency": "USD"
    }
  },
  "timeline": {
    "created_at": "2026-04-02T22:12:00Z",
    "planned_date": "2026-04-02T22:12:00Z",
    "applied_date": "2026-04-03T10:30:00Z",
    "interview_date": "2026-04-10T14:00:00Z",
    "status_updated_at": "2026-04-10T16:30:00Z"
  },
  "status": "interview",
  "priority": "high", // "high", "medium", "low"
  "source": "LinkedIn", // "LinkedIn", "Indeed", "Company Website", "Referral", "Other"
  "source_url": "https://linkedin.com/jobs/view/12345",
  "notes": "Great company culture, team of 8 engineers",
  "tags": ["python", "django", "remote"],
  "linked_content": {
    "job_analysis_id": "uuid",
    "tailored_resume_id": "uuid",
    "cover_letter_id": "uuid",
    "outreach_content_id": "uuid",
    "interview_prep_id": "uuid"
  },
  "contacts": [
    {
      "name": "Sarah Johnson",
      "title": "Technical Recruiter",
      "email": "sarah@techcorp.com",
      "phone": "+1-555-0123",
      "linkedin": "https://linkedin.com/in/sarahjohnson",
      "notes": "Primary contact, very responsive"
    }
  ],
  "interview_details": {
    "type": "technical", // "technical", "behavioral", "panel", "phone", "onsite"
    "format": "video call", // "video call", "phone", "onsite", "assessment"
    "duration_minutes": 60,
    "interviewers": [
      {
        "name": "Mike Chen",
        "title": "Senior Engineer",
        "role": "hiring_manager"
      }
    ],
    "location": "Zoom meeting",
    "preparation_notes": "Focus on system design and Python experience"
  },
  "follow_up_actions": [
    {
      "action": "Send thank-you email",
      "due_date": "2026-04-11T09:00:00Z",
      "completed": false,
      "priority": "high"
    }
  ],
  "outcome": {
    "final_status": null, // "rejected", "offer", "withdrawn"
    "rejection_reason": null, // "not qualified", "culture fit", "position filled", "other"
    "offer_details": null, // Offer details if received
    "feedback": null // Company feedback if provided
  }
}
```

### Application Status History
```json
{
  "status_history_id": "uuid",
  "application_id": "uuid",
  "status_changes": [
    {
      "from_status": "planned",
      "to_status": "applied",
      "changed_at": "2026-04-03T10:30:00Z",
      "notes": "Applied through company website",
      "triggered_by": "user" // "user", "system", "automatic"
    },
    {
      "from_status": "applied",
      "to_status": "interview",
      "changed_at": "2026-04-08T15:20:00Z",
      "notes": "Interview scheduled for April 10th",
      "triggered_by": "user"
    }
  ]
}
```

### Application Activity Log
```json
{
  "activity_id": "uuid",
  "application_id": "uuid",
  "activities": [
    {
      "type": "content_generated", // "content_generated", "status_updated", "contact_added", "note_added"
      "description": "Cover letter generated",
      "timestamp": "2026-04-02T22:15:00Z",
      "details": {
        "content_type": "cover_letter",
        "content_id": "uuid"
      }
    },
    {
      "type": "interview_scheduled",
      "description": "Technical interview scheduled",
      "timestamp": "2026-04-08T15:20:00Z",
      "details": {
        "interview_date": "2026-04-10T14:00:00Z",
        "interview_type": "technical"
      }
    }
  ]
}
```

## Database Schema

### applications Table
```sql
CREATE TABLE applications (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    company_name VARCHAR(255) NOT NULL,
    company_website VARCHAR(500),
    company_industry VARCHAR(100),
    company_size VARCHAR(50),
    company_location VARCHAR(255),
    company_remote_policy VARCHAR(50),
    position_title VARCHAR(255) NOT NULL,
    position_level VARCHAR(50),
    position_department VARCHAR(100),
    employment_type VARCHAR(50),
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'planned',
    priority VARCHAR(10) DEFAULT 'medium',
    source VARCHAR(50),
    source_url TEXT,
    notes TEXT,
    tags TEXT[], -- PostgreSQL array
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    planned_date TIMESTAMP,
    applied_date TIMESTAMP,
    interview_date TIMESTAMP,
    status_updated_at TIMESTAMP,
    
    -- Linked content IDs
    job_analysis_id UUID,
    tailored_resume_id UUID,
    cover_letter_id UUID,
    outreach_content_id UUID,
    interview_prep_id UUID,
    
    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('planned', 'applied', 'interview', 'rejected', 'offer')),
    CONSTRAINT valid_priority CHECK (priority IN ('high', 'medium', 'low')),
    CONSTRAINT valid_employment_type CHECK (employment_type IN ('full-time', 'part-time', 'contract', 'internship'))
);
```

### application_contacts Table
```sql
CREATE TABLE application_contacts (
    id UUID PRIMARY KEY,
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    linkedin VARCHAR(500),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### application_interviews Table
```sql
CREATE TABLE application_interviews (
    id UUID PRIMARY KEY,
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    format VARCHAR(50) NOT NULL,
    scheduled_date TIMESTAMP NOT NULL,
    duration_minutes INTEGER,
    location VARCHAR(255),
    preparation_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT valid_interview_type CHECK (type IN ('technical', 'behavioral', 'panel', 'phone', 'onsite')),
    CONSTRAINT valid_interview_format CHECK (format IN ('video call', 'phone', 'onsite', 'assessment'))
);
```

### application_interviewers Table
```sql
CREATE TABLE application_interviewers (
    id UUID PRIMARY KEY,
    interview_id UUID NOT NULL REFERENCES application_interviews(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    role VARCHAR(100), -- "hiring_manager", "peer", "senior_leader", "hr"
    email VARCHAR(255),
    linkedin VARCHAR(500),
    notes TEXT
);
```

### application_status_history Table
```sql
CREATE TABLE application_status_history (
    id UUID PRIMARY KEY,
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    from_status VARCHAR(20),
    to_status VARCHAR(20) NOT NULL,
    changed_at TIMESTAMP DEFAULT NOW(),
    notes TEXT,
    triggered_by VARCHAR(20) DEFAULT 'user',
    
    CONSTRAINT valid_status CHECK (from_status IS NULL OR from_status IN ('planned', 'applied', 'interview', 'rejected', 'offer')),
    CONSTRAINT valid_to_status CHECK (to_status IN ('planned', 'applied', 'interview', 'rejected', 'offer'))
);
```

### application_activities Table
```sql
CREATE TABLE application_activities (
    id UUID PRIMARY KEY,
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    details JSONB,
    
    CONSTRAINT valid_activity_type CHECK (type IN ('content_generated', 'status_updated', 'contact_added', 'note_added', 'interview_scheduled', 'follow_up_created'))
);
```

### follow_up_actions Table
```sql
CREATE TABLE follow_up_actions (
    id UUID PRIMARY KEY,
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    due_date TIMESTAMP,
    completed BOOLEAN DEFAULT false,
    priority VARCHAR(10) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    CONSTRAINT valid_priority CHECK (priority IN ('high', 'medium', 'low'))
);
```

### Indexes
```sql
CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_created_at ON applications(created_at DESC);
CREATE INDEX idx_applications_company_name ON applications(company_name);
CREATE INDEX idx_applications_position_title ON applications(position_title);
CREATE INDEX idx_applications_tags ON applications USING GIN(tags);
CREATE INDEX idx_application_contacts_application_id ON application_contacts(application_id);
CREATE INDEX idx_application_interviews_application_id ON application_interviews(application_id);
CREATE INDEX idx_application_interviews_scheduled_date ON application_interviews(scheduled_date);
CREATE INDEX idx_application_status_history_application_id ON application_status_history(application_id);
CREATE INDEX idx_application_activities_application_id ON application_activities(application_id);
CREATE INDEX idx_application_activities_timestamp ON application_activities(timestamp DESC);
CREATE INDEX idx_follow_up_actions_application_id ON follow_up_actions(application_id);
CREATE INDEX idx_follow_up_actions_due_date ON follow_up_actions(due_date);
```

## API Endpoints

### 1. Create Application
```
POST /api/v1/applications
```

**Request Body:**
```json
{
  "company": {
    "name": "Tech Corp",
    "website": "https://techcorp.com",
    "industry": "technology",
    "location": "San Francisco, CA"
  },
  "position": {
    "title": "Senior Software Engineer",
    "level": "senior",
    "employment_type": "full-time",
    "salary_range": { "min": 120000, "max": 180000 }
  },
  "source": "LinkedIn",
  "source_url": "https://linkedin.com/jobs/view/12345",
  "priority": "high",
  "notes": "Interesting role in cloud computing",
  "tags": ["python", "django", "remote"]
}
```

**Response:**
```json
{
  "application_id": "uuid",
  "status": "planned",
  "created_at": "2026-04-02T22:12:00Z",
  "application": { ... } // Full application object
}
```

### 2. Get All Applications
```
GET /api/v1/applications
```

**Query Parameters:**
- `status`: Filter by status (planned, applied, interview, rejected, offer)
- `company`: Filter by company name
- `priority`: Filter by priority (high, medium, low)
- `tags`: Filter by tags (comma-separated)
- `source`: Filter by source
- `sort`: Sort by field (created_at, status, priority, company_name, position_title)
- `order`: Sort order (asc, desc)
- `limit`: Number of results (default: 50, max: 100)
- `offset`: Pagination offset

**Response:**
```json
{
  "applications": [
    {
      "application_id": "uuid",
      "company": { "name": "Tech Corp" },
      "position": { "title": "Senior Software Engineer" },
      "status": "interview",
      "priority": "high",
      "created_at": "2026-04-02T22:12:00Z",
      "updated_at": "2026-04-10T16:30:00Z",
      "next_action": "Technical interview on April 10",
      "days_in_current_status": 2
    }
  ],
  "pagination": {
    "total": 25,
    "limit": 50,
    "offset": 0,
    "has_more": false
  },
  "summary": {
    "total_applications": 25,
    "by_status": {
      "planned": 5,
      "applied": 10,
      "interview": 6,
      "rejected": 3,
      "offer": 1
    }
  }
}
```

### 3. Get Application Details
```
GET /api/v1/applications/{application_id}
```

**Response:**
```json
{
  "application": { ... }, // Full application object
  "status_history": [
    {
      "from_status": "planned",
      "to_status": "applied",
      "changed_at": "2026-04-03T10:30:00Z",
      "notes": "Applied through company website"
    }
  ],
  "contacts": [
    {
      "name": "Sarah Johnson",
      "title": "Technical Recruiter",
      "email": "sarah@techcorp.com"
    }
  ],
  "interviews": [
    {
      "type": "technical",
      "format": "video call",
      "scheduled_date": "2026-04-10T14:00:00Z",
      "interviewers": [
        {
          "name": "Mike Chen",
          "title": "Senior Engineer",
          "role": "hiring_manager"
        }
      ]
    }
  ],
  "follow_up_actions": [
    {
      "action": "Send thank-you email",
      "due_date": "2026-04-11T09:00:00Z",
      "completed": false,
      "priority": "high"
    }
  ],
  "linked_content": {
    "job_analysis": { ... },
    "tailored_resume": { ... },
    "cover_letter": { ... },
    "outreach_content": { ... },
    "interview_prep": { ... }
  }
}
```

### 4. Update Application
```
PUT /api/v1/applications/{application_id}
```

**Request Body:**
```json
{
  "status": "interview",
  "notes": "Interview scheduled for next week",
  "priority": "high",
  "tags": ["python", "django", "remote", "urgent"]
}
```

**Response:**
```json
{
  "application_id": "uuid",
  "updated_fields": ["status", "notes", "priority", "tags"],
  "updated_at": "2026-04-08T15:20:00Z",
  "application": { ... } // Updated full application object
}
```

### 5. Update Application Status
```
PUT /api/v1/applications/{application_id}/status
```

**Request Body:**
```json
{
  "status": "interview",
  "notes": "Technical interview scheduled with Mike Chen",
  "interview_details": {
    "type": "technical",
    "format": "video call",
    "scheduled_date": "2026-04-10T14:00:00Z",
    "duration_minutes": 60
  }
}
```

**Response:**
```json
{
  "application_id": "uuid",
  "status": "interview",
  "previous_status": "applied",
  "changed_at": "2026-04-08T15:20:00Z",
  "status_history_entry": {
    "from_status": "applied",
    "to_status": "interview",
    "changed_at": "2026-04-08T15:20:00Z",
    "notes": "Technical interview scheduled with Mike Chen"
  }
}
```

### 6. Add Contact
```
POST /api/v1/applications/{application_id}/contacts
```

**Request Body:**
```json
{
  "name": "Sarah Johnson",
  "title": "Technical Recruiter",
  "email": "sarah@techcorp.com",
  "phone": "+1-555-0123",
  "linkedin": "https://linkedin.com/in/sarahjohnson",
  "notes": "Primary contact, very responsive"
}
```

**Response:**
```json
{
  "contact_id": "uuid",
  "application_id": "uuid",
  "created_at": "2026-04-02T22:15:00Z",
  "contact": { ... } // Full contact object
}
```

### 7. Schedule Interview
```
POST /api/v1/applications/{application_id}/interviews
```

**Request Body:**
```json
{
  "type": "technical",
  "format": "video call",
  "scheduled_date": "2026-04-10T14:00:00Z",
  "duration_minutes": 60,
  "location": "Zoom meeting",
  "preparation_notes": "Focus on system design and Python experience",
  "interviewers": [
    {
      "name": "Mike Chen",
      "title": "Senior Engineer",
      "role": "hiring_manager",
      "email": "mike@techcorp.com"
    }
  ]
}
```

**Response:**
```json
{
  "interview_id": "uuid",
  "application_id": "uuid",
  "scheduled_date": "2026-04-10T14:00:00Z",
  "interview": { ... } // Full interview object
}
```

### 8. Add Follow-up Action
```
POST /api/v1/applications/{application_id}/follow-up-actions
```

**Request Body:**
```json
{
  "action": "Send thank-you email",
  "due_date": "2026-04-11T09:00:00Z",
  "priority": "high"
}
```

**Response:**
```json
{
  "action_id": "uuid",
  "application_id": "uuid",
  "created_at": "2026-04-08T15:25:00Z",
  "follow_up_action": { ... } // Full follow-up action object
}
```

### 9. Link Content
```
PUT /api/v1/applications/{application_id}/linked-content
```

**Request Body:**
```json
{
  "job_analysis_id": "uuid",
  "tailored_resume_id": "uuid",
  "cover_letter_id": "uuid",
  "outreach_content_id": "uuid",
  "interview_prep_id": "uuid"
}
```

**Response:**
```json
{
  "application_id": "uuid",
  "linked_content": {
    "job_analysis_id": "uuid",
    "tailored_resume_id": "uuid",
    "cover_letter_id": "uuid",
    "outreach_content_id": "uuid",
    "interview_prep_id": "uuid"
  },
  "updated_at": "2026-04-02T22:20:00Z"
}
```

### 10. Delete Application
```
DELETE /api/v1/applications/{application_id}
```

**Response:**
```json
{
  "application_id": "uuid",
  "deleted": true,
  "deleted_at": "2026-04-02T22:25:00Z"
}
```

### 11. Get Application Statistics
```
GET /api/v1/applications/statistics
```

**Query Parameters:**
- `period`: Time period (week, month, quarter, year)
- `start_date`: Start date for custom period
- `end_date`: End date for custom period

**Response:**
```json
{
  "period": "month",
  "start_date": "2026-03-01T00:00:00Z",
  "end_date": "2026-03-31T23:59:59Z",
  "summary": {
    "total_applications": 15,
    "applications_by_status": {
      "planned": 3,
      "applied": 7,
      "interview": 4,
      "rejected": 1,
      "offer": 0
    },
    "success_rate": 0.07, // offers / total
    "interview_rate": 0.27, // interviews / total
    "response_rate": 0.47 // responses (interview + offer) / applied
  },
  "timeline": [
    {
      "date": "2026-03-01",
      "applications_created": 2,
      "applications_applied": 1,
      "interviews_scheduled": 0
    }
  ],
  "top_companies": [
    {
      "company_name": "Tech Corp",
      "application_count": 3,
      "success_count": 1
    }
  ],
  "average_time_in_status": {
    "planned": 3.5, // days
    "applied": 7.2,
    "interview": 14.1
  }
}
```

## Frontend Table/Dashboard View

### Main Dashboard Component
```jsx
<ApplicationTracker>
  <Header>
    <Title>Application Tracker</Title>
    <SummaryCards>
      <Card title="Total Applications" value={25} change="+3 this week" />
      <Card title="Interviews" value={6} change="+2 this week" />
      <Card title="Offers" value={1} change="0 this week" />
      <Card title="Success Rate" value="4%" change="+1%" />
    </SummaryCards>
  </Header>
  
  <Controls>
    <FilterPanel>
      <StatusFilter options={["All", "Planned", "Applied", "Interview", "Rejected", "Offer"]} />
      <CompanyFilter placeholder="Filter by company..." />
      <PriorityFilter options={["All", "High", "Medium", "Low"]} />
      <TagFilter availableTags={["python", "django", "remote"]} />
      <DateRangeFilter />
    </FilterPanel>
    
    <SortControls>
      <SortBy options={["Date Created", "Status", "Priority", "Company", "Position"]} />
      <SortOrder toggle={true} />
    </SortControls>
    
    <Actions>
      <AddApplicationButton />
      <ExportButton />
      <BulkActions />
    </Actions>
  </Controls>
  
  <ApplicationsTable>
    <Column header="Company" sortable={true} filterable={true} />
    <Column header="Position" sortable={true} />
    <Column header="Status" sortable={true} filterable={true} />
    <Column header="Priority" sortable={true} />
    <Column header="Applied Date" sortable={true} />
    <Column header="Next Action" />
    <Column header="Tags" filterable={true} />
    <Column header="Actions" />
    
    <Row application={application1}>
      <Cell> Tech Corp </Cell>
      <Cell> Senior Software Engineer </Cell>
      <Cell> <StatusBadge status="interview" /> </Cell>
      <Cell> <PriorityBadge priority="high" /> </Cell>
      <Cell> Apr 3, 2026 </Cell>
      <Cell> Interview on Apr 10 </Cell>
      <Cell> <TagList tags={["python", "django"]} /> </Cell>
      <Cell> <ActionMenu application={application1} /> </Cell>
    </Row>
  </ApplicationsTable>
  
  <Pagination>
    <PageInfo showing="1-10 of 25" />
    <PageControls />
  </Pagination>
</ApplicationTracker>
```

### Application Detail View
```jsx
<ApplicationDetail>
  <Header>
    <CompanyInfo company="Tech Corp" position="Senior Software Engineer" />
    <StatusIndicator status="interview" />
    <PriorityIndicator priority="high" />
  </Header>
  
  <Tabs>
    <Tab label="Overview">
      <OverviewPanel>
        <Timeline events={statusHistory} />
        <KeyInfo application={application} />
        <QuickActions />
      </OverviewPanel>
    </Tab>
    
    <Tab label="Documents">
      <DocumentsPanel>
        <LinkedDocument type="job_analysis" />
        <LinkedDocument type="tailored_resume" />
        <LinkedDocument type="cover_letter" />
        <LinkedDocument type="outreach_content" />
        <LinkedDocument type="interview_prep" />
      </DocumentsPanel>
    </Tab>
    
    <Tab label="Contacts">
      <ContactsPanel>
        <ContactList contacts={contacts} />
        <AddContactButton />
      </ContactsPanel>
    </Tab>
    
    <Tab label="Interviews">
      <InterviewsPanel>
        <InterviewList interviews={interviews} />
        <ScheduleInterviewButton />
      </InterviewsPanel>
    </Tab>
    
    <Tab label="Follow-ups">
      <FollowUpsPanel>
        <FollowUpList actions={followUpActions} />
        <AddFollowUpButton />
      </FollowUpsPanel>
    </Tab>
    
    <Tab label="Activity">
      <ActivityPanel>
        <ActivityTimeline activities={activities} />
      </ActivityPanel>
    </Tab>
  </Tabs>
</ApplicationDetail>
```

### Add/Edit Application Modal
```jsx
<ApplicationModal mode="create">
  <Form>
    <Section title="Company Information">
      <Input label="Company Name" required />
      <Input label="Company Website" />
      <Select label="Industry" options={industries} />
      <Input label="Location" />
      <Select label="Remote Policy" options={["On-site", "Hybrid", "Remote"]} />
    </Section>
    
    <Section title="Position Information">
      <Input label="Position Title" required />
      <Select label="Level" options={["Entry", "Junior", "Mid", "Senior", "Lead", "Principal"]} />
      <Select label="Employment Type" options={["Full-time", "Part-time", "Contract", "Internship"]} />
      <SalaryRangeInput />
    </Section>
    
    <Section title="Application Details">
      <Select label="Status" options={statusOptions} />
      <Select label="Priority" options={priorityOptions} />
      <Select label="Source" options={sourceOptions} />
      <Input label="Source URL" />
      <TextArea label="Notes" />
      <TagInput availableTags={commonTags} />
    </Section>
  </Form>
  
  <Actions>
    <SaveButton />
    <CancelButton />
  </Actions>
</ApplicationModal>
```

## Filtering and Sorting

### Filter Options
```javascript
const filterOptions = {
  status: {
    type: 'multi-select',
    options: ['planned', 'applied', 'interview', 'rejected', 'offer'],
    default: []
  },
  company: {
    type: 'text',
    placeholder: 'Filter by company name...',
    operator: 'contains'
  },
  priority: {
    type: 'multi-select',
    options: ['high', 'medium', 'low'],
    default: []
  },
  tags: {
    type: 'multi-select',
    options: [], // Populated from user's tags
    default: []
  },
  source: {
    type: 'multi-select',
    options: ['LinkedIn', 'Indeed', 'Company Website', 'Referral', 'Other'],
    default: []
  },
  dateRange: {
    type: 'date-range',
    field: 'created_at',
    default: 'last_30_days'
  },
  salaryRange: {
    type: 'range',
    field: 'salary_min',
    min: 0,
    max: 300000
  }
};
```

### Sort Options
```javascript
const sortOptions = {
  created_at: {
    label: 'Date Created',
    default: 'desc',
    type: 'date'
  },
  status: {
    label: 'Status',
    default: 'asc',
    type: 'categorical',
    order: ['planned', 'applied', 'interview', 'offer', 'rejected']
  },
  priority: {
    label: 'Priority',
    default: 'desc',
    type: 'categorical',
    order: ['high', 'medium', 'low']
  },
  company_name: {
    label: 'Company',
    default: 'asc',
    type: 'text'
  },
  position_title: {
    label: 'Position',
    default: 'asc',
    type: 'text'
  },
  applied_date: {
    label: 'Applied Date',
    default: 'desc',
    type: 'date'
  },
  interview_date: {
    label: 'Interview Date',
    default: 'asc',
    type: 'date'
  }
};
```

## Validation Rules

### Input Validation
```json
{
  "application_validation": {
    "company_name": {
      "required": true,
      "min_length": 2,
      "max_length": 255,
      "pattern": "^[a-zA-Z0-9\\s\\-\\.,]+$"
    },
    "position_title": {
      "required": true,
      "min_length": 3,
      "max_length": 255,
      "pattern": "^[a-zA-Z0-9\\s\\-\\.,]+$"
    },
    "status": {
      "required": true,
      "enum": ["planned", "applied", "interview", "rejected", "offer"]
    },
    "priority": {
      "required": true,
      "enum": ["high", "medium", "low"],
      "default": "medium"
    },
    "employment_type": {
      "enum": ["full-time", "part-time", "contract", "internship"]
    },
    "salary_range": {
      "min": 0,
      "max": 1000000,
      "currency": "USD",
      "validation": "min <= max"
    },
    "source_url": {
      "format": "url",
      "max_length": 500
    },
    "tags": {
      "type": "array",
      "max_items": 10,
      "item_pattern": "^[a-zA-Z0-9\\-_]+$",
      "item_max_length": 50
    },
    "notes": {
      "max_length": 2000,
      "sanitize": true
    }
  }
}
```

### Business Logic Validation
```json
{
  "status_flow_validation": {
    "planned_to_applied": {
      "allowed": true,
      "requirements": ["applied_date"],
      "auto_set_fields": ["applied_date"]
    },
    "applied_to_interview": {
      "allowed": true,
      "requirements": ["interview_date"],
      "auto_set_fields": ["interview_date"]
    },
    "interview_to_offer": {
      "allowed": true,
      "requirements": ["offer_details"],
      "auto_set_fields": []
    },
    "interview_to_rejected": {
      "allowed": true,
      "requirements": ["rejection_reason"],
      "auto_set_fields": []
    },
    "applied_to_rejected": {
      "allowed": true,
      "requirements": ["rejection_reason"],
      "auto_set_fields": []
    },
    "any_to_planned": {
      "allowed": false,
      "error": "Cannot move back to planned status"
    }
  }
}
```

### Data Integrity Validation
```json
{
  "referential_integrity": {
    "linked_content": {
      "job_analysis_id": "must_exist_in_job_analyses",
      "tailored_resume_id": "must_exist_in_resumes",
      "cover_letter_id": "must_exist_in_content_library",
      "outreach_content_id": "must_exist_in_content_library",
      "interview_prep_id": "must_exist_in_content_library"
    },
    "user_ownership": {
      "application": "must_belong_to_user",
      "contacts": "must_belong_to_application",
      "interviews": "must_belong_to_application"
    }
  }
}
```

## Test Cases

### Unit Tests

#### Application CRUD Tests
```javascript
describe('Application CRUD Operations', () => {
  test('should create new application with valid data', async () => {
    const applicationData = {
      company: { name: 'Tech Corp', industry: 'technology' },
      position: { title: 'Senior Software Engineer', employment_type: 'full-time' },
      status: 'planned',
      priority: 'high'
    };
    
    const result = await createApplication(userId, applicationData);
    
    expect(result.application_id).toBeDefined();
    expect(result.status).toBe('planned');
    expect(result.created_at).toBeDefined();
  });
  
  test('should reject application with missing required fields', async () => {
    const invalidData = {
      company: { name: '' }, // Empty company name
      position: { title: 'Software Engineer' },
      status: 'planned'
    };
    
    await expect(createApplication(userId, invalidData))
      .rejects.toThrow('Company name is required');
  });
  
  test('should update application status with valid flow', async () => {
    const application = await createTestApplication();
    
    const updated = await updateApplicationStatus(application.id, 'applied', {
      notes: 'Applied through company website'
    });
    
    expect(updated.status).toBe('applied');
    expect(updated.applied_date).toBeDefined();
    expect(updated.status_history).toHaveLength(2);
  });
  
  test('should reject invalid status transitions', async () => {
    const application = await createTestApplication({ status: 'interview' });
    
    await expect(updateApplicationStatus(application.id, 'planned'))
      .rejects.toThrow('Cannot move back to planned status');
  });
});
```

#### Contact Management Tests
```javascript
describe('Contact Management', () => {
  test('should add contact to application', async () => {
    const application = await createTestApplication();
    const contactData = {
      name: 'Sarah Johnson',
      title: 'Technical Recruiter',
      email: 'sarah@techcorp.com'
    };
    
    const contact = await addContact(application.id, contactData);
    
    expect(contact.contact_id).toBeDefined();
    expect(contact.name).toBe('Sarah Johnson');
    expect(contact.email).toBe('sarah@techcorp.com');
  });
  
  test('should validate email format for contacts', async () => {
    const application = await createTestApplication();
    const invalidContact = {
      name: 'John Doe',
      email: 'invalid-email' // Invalid email format
    };
    
    await expect(addContact(application.id, invalidContact))
      .rejects.toThrow('Invalid email format');
  });
});
```

#### Interview Scheduling Tests
```javascript
describe('Interview Scheduling', () => {
  test('should schedule interview with valid data', async () => {
    const application = await createTestApplication();
    const interviewData = {
      type: 'technical',
      format: 'video call',
      scheduled_date: '2026-04-10T14:00:00Z',
      duration_minutes: 60,
      interviewers: [
        { name: 'Mike Chen', title: 'Senior Engineer', role: 'hiring_manager' }
      ]
    };
    
    const interview = await scheduleInterview(application.id, interviewData);
    
    expect(interview.interview_id).toBeDefined();
    expect(interview.type).toBe('technical');
    expect(interview.scheduled_date).toBe('2026-04-10T14:00:00Z');
  });
  
  test('should auto-update application status when interview scheduled', async () => {
    const application = await createTestApplication({ status: 'applied' });
    
    await scheduleInterview(application.id, {
      type: 'technical',
      scheduled_date: '2026-04-10T14:00:00Z'
    });
    
    const updated = await getApplication(application.id);
    expect(updated.status).toBe('interview');
  });
});
```

### Integration Tests

#### End-to-End Workflow Tests
```javascript
describe('Application Tracker Workflow', () => {
  test('should complete full application lifecycle', async () => {
    // Create application
    const application = await createApplication(userId, {
      company: { name: 'Tech Corp' },
      position: { title: 'Senior Software Engineer' },
      status: 'planned'
    });
    
    // Update to applied
    await updateApplicationStatus(application.id, 'applied');
    
    // Add contact
    await addContact(application.id, {
      name: 'Sarah Johnson',
      email: 'sarah@techcorp.com'
    });
    
    // Schedule interview
    await scheduleInterview(application.id, {
      type: 'technical',
      scheduled_date: '2026-04-10T14:00:00Z'
    });
    
    // Verify final state
    const final = await getApplication(application.id);
    expect(final.status).toBe('interview');
    expect(final.contacts).toHaveLength(1);
    expect(final.interviews).toHaveLength(1);
  });
});
```

#### API Integration Tests
```javascript
describe('API Integration', () => {
  test('GET /applications should return paginated results', async () => {
    await createMultipleApplications(15); // Create 15 test applications
    
    const response = await request(app)
      .get('/api/v1/applications')
      .query({ limit: 10, offset: 0 });
    
    expect(response.status).toBe(200);
    expect(response.body.applications).toHaveLength(10);
    expect(response.body.pagination.total).toBe(15);
    expect(response.body.pagination.has_more).toBe(true);
  });
  
  test('GET /applications with filters should return filtered results', async () => {
    await createTestApplications([
      { status: 'applied', company: { name: 'Tech Corp' } },
      { status: 'interview', company: { name: 'Data Corp' } },
      { status: 'applied', company: { name: 'AI Corp' } }
    ]);
    
    const response = await request(app)
      .get('/api/v1/applications')
      .query({ status: 'applied' });
    
    expect(response.status).toBe(200);
    expect(response.body.applications).toHaveLength(2);
    response.body.applications.forEach(app => {
      expect(app.status).toBe('applied');
    });
  });
});
```

### Performance Tests

#### Load Testing
```javascript
describe('Performance Tests', () => {
  test('should handle large number of applications efficiently', async () => {
    // Create 1000 applications
    await createBulkApplications(1000);
    
    const startTime = Date.now();
    const response = await request(app)
      .get('/api/v1/applications')
      .query({ limit: 50 });
    
    const duration = Date.now() - startTime;
    
    expect(response.status).toBe(200);
    expect(duration).toBeLessThan(1000); // Should respond in under 1 second
    expect(response.body.applications).toHaveLength(50);
  });
  
  test('should handle concurrent requests', async () => {
    const concurrentRequests = 20;
    const requests = Array(concurrentRequests).fill().map(() =>
      request(app).get('/api/v1/applications')
    );
    
    const results = await Promise.all(requests);
    
    results.forEach(response => {
      expect(response.status).toBe(200);
      expect(response.body.applications).toBeDefined();
    });
  });
});
```

### User Acceptance Tests

#### Usability Tests
```javascript
describe('User Experience Tests', () => {
  test('should provide intuitive filtering interface', () => {
    const component = mount(<ApplicationTracker />);
    
    // Test status filter
    component.find('[data-testid="status-filter"]').simulate('change', 'applied');
    expect(component.state('filters.status)).toBe('applied');
    
    // Test company filter
    component.find('[data-testid="company-filter"]')
      .simulate('change', { target: { value: 'Tech Corp' } });
    expect(component.state('filters.company')).toBe('Tech Corp');
  });
  
  test('should show clear application status indicators', () => {
    const application = { status: 'interview', priority: 'high' };
    const component = mount(<ApplicationRow application={application} />);
    
    expect(component.find('[data-testid="status-badge"]').text()).toBe('Interview');
    expect(component.find('[data-testid="priority-badge"]').text()).toBe('High');
  });
});
```

### Test Data Sets

#### Positive Test Cases
```javascript
const positiveTestCases = [
  {
    name: 'Complete application with all data',
    data: {
      company: { name: 'Tech Corp', industry: 'technology', location: 'San Francisco' },
      position: { title: 'Senior Software Engineer', level: 'senior', employment_type: 'full-time' },
      status: 'applied',
      priority: 'high',
      source: 'LinkedIn',
      tags: ['python', 'django', 'remote']
    },
    expected: 'Application created successfully'
  },
  {
    name: 'Application with interview scheduled',
    data: {
      company: { name: 'Data Corp' },
      position: { title: 'Data Engineer' },
      status: 'interview',
      interview: {
        type: 'technical',
        scheduled_date: '2026-04-10T14:00:00Z'
      }
    },
    expected: 'Application with interview created'
  }
];
```

#### Negative Test Cases
```javascript
const negativeTestCases = [
  {
    name: 'Missing required company name',
    data: {
      company: { name: '' },
      position: { title: 'Software Engineer' },
      status: 'planned'
    },
    expected_error: 'Company name is required'
  },
  {
    name: 'Invalid status transition',
    data: {
      current_status: 'rejected',
      new_status: 'planned'
    },
    expected_error: 'Cannot move back to planned status'
  },
  {
    name: 'Invalid email format for contact',
    data: {
      contact: {
        name: 'John Doe',
        email: 'invalid-email-format'
      }
    },
    expected_error: 'Invalid email format'
  }
];
```

## Implementation Tasks

### Phase 1: Core Database & API (2 weeks)
- [ ] **Design database schema** - Complete ERD and table definitions
- [ ] **Implement database migrations** - Version-controlled schema changes
- [ ] **Create application CRUD operations** - Basic create, read, update, delete
- [ ] **Implement status management** - Status transitions and validation
- [ ] **Build contact management** - Add, update, delete contacts
- [ ] **Create interview scheduling** - Interview CRUD with validation
- [ ] **Implement follow-up actions** - Task management for applications
- [ ] **Add activity logging** - Track all application activities

### Phase 2: Advanced Features (2 weeks)
- [ ] **Implement filtering and sorting** - Advanced query capabilities
- [ ] **Create statistics API** - Application analytics and metrics
- [ ] **Build content linking** - Connect to resumes, cover letters, etc.
- [ ] **Add status history tracking** - Complete audit trail
- [ ] **Implement search functionality** - Full-text search across applications
- [ ] **Create export functionality** - Export to CSV, PDF
- [ ] **Add notification system** - Follow-up reminders and status changes
- [ ] **Implement data validation** - Comprehensive input validation

### Phase 3: Frontend Development (2 weeks)
- [ ] **Build main dashboard** - Application table with filtering/sorting
- [ ] **Create application detail view** - Complete application information
- [ ] **Implement add/edit modals** - Forms for creating and editing
- [ ] **Add status management UI** - Status updates and transitions
- [ ] **Create contact management interface** - Contact CRUD UI
- [ ] **Build interview scheduling UI** - Interview management interface
- [ ] **Implement follow-up tracking** - Task management UI
- [ ] **Add statistics dashboard** - Visual analytics and charts

### Phase 4: Integration & Testing (1 week)
- [ ] **End-to-end workflow testing** - Complete user journey testing
- [ ] **Performance optimization** - Query optimization and caching
- [ ] **Security validation** - Data protection and access controls
- [ ] **User acceptance testing** - Usability and satisfaction testing
- [ ] **Mobile responsiveness** - Test on mobile devices
- [ ] **Browser compatibility** - Cross-browser testing
- [ ] **Accessibility testing** - WCAG compliance verification
- [ ] **Documentation completion** - API docs and user guides

### Phase 5: Deployment & Monitoring (1 week)
- [ ] **Production deployment** - Deploy to production environment
- [ ] **Monitoring setup** - Performance and health monitoring
- [ ] **Backup procedures** - Data backup and recovery
- [ ] **User training materials** - Guides and tutorials
- [ ] **Launch preparation** - Final checks and go-live
- [ ] **Post-launch monitoring** - Track performance and usage
- [ ] **User support setup** - Help desk and support procedures
- [ ] **Continuous improvement** - Feedback collection and iteration
