---
inclusion: auto
---

# AI Job Application Copilot - UI/UX Steering Document

## Design Philosophy

The AI Job Application Copilot should feel like a professional productivity tool that job seekers trust and want to use repeatedly. The interface prioritizes clarity, efficiency, and user control over flashy features or unnecessary complexity.

### Core Design Principles

1. **Trust Through Transparency** - Users should always understand what the AI is doing and why
2. **Efficiency Over Novelty** - Optimize for repeated use, not first impressions
3. **Control Over Automation** - Users approve all changes; nothing happens automatically
4. **Clarity Over Density** - Use space generously; don't cram information
5. **Professional Over Playful** - This is a career tool, not a consumer app

## Visual Design System

### Color Palette

**Primary Colors:**
- Primary: Blue (#2563EB) - Actions, links, primary buttons
- Success: Green (#10B981) - Confirmations, strong matches
- Warning: Amber (#F59E0B) - Partial matches, cautions
- Error: Red (#EF4444) - Missing requirements, errors
- Neutral: Gray scale (#F9FAFB to #111827) - Text, backgrounds, borders

**Usage Guidelines:**
- Use color sparingly and meaningfully
- Primary color for main actions only
- Success/Warning/Error for status indication
- Neutral grays for structure and hierarchy
- Avoid bright, saturated colors
- Maintain WCAG AA contrast ratios minimum


### Typography

**Font Stack:**
- Primary: Inter, system-ui, -apple-system, sans-serif
- Monospace: 'Fira Code', 'Courier New', monospace (for diffs)

**Type Scale:**
- Heading 1: 32px / 2rem (Page titles)
- Heading 2: 24px / 1.5rem (Section titles)
- Heading 3: 20px / 1.25rem (Subsection titles)
- Body Large: 18px / 1.125rem (Important content)
- Body: 16px / 1rem (Default text)
- Body Small: 14px / 0.875rem (Secondary text, labels)
- Caption: 12px / 0.75rem (Metadata, timestamps)

**Font Weights:**
- Regular: 400 (Body text)
- Medium: 500 (Emphasis, labels)
- Semibold: 600 (Headings, buttons)
- Bold: 700 (Strong emphasis, use sparingly)

**Line Height:**
- Headings: 1.2
- Body text: 1.5
- Dense content: 1.4

### Spacing System

Use consistent spacing scale (4px base unit):
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

**Application:**
- Component padding: md (16px)
- Section spacing: xl (32px)
- Page margins: lg to xl (24-32px)
- Card spacing: md to lg (16-24px)
- Element gaps: sm to md (8-16px)

### Layout Grid

- Max content width: 1280px
- Responsive breakpoints:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px
- Sidebar width: 240px (collapsed: 64px)
- Main content: Flexible with max-width constraints


### Component Styles

**Cards:**
- Background: White (#FFFFFF)
- Border: 1px solid Gray-200 (#E5E7EB)
- Border radius: 8px
- Shadow: Subtle (0 1px 3px rgba(0,0,0,0.1))
- Padding: md to lg (16-24px)
- Hover: Slight shadow increase (if interactive)

**Buttons:**

Primary:
- Background: Primary blue
- Text: White
- Padding: 12px 24px
- Border radius: 6px
- Font weight: 600
- Hover: Slightly darker

Secondary:
- Background: White
- Border: 1px solid Gray-300
- Text: Gray-700
- Hover: Gray-50 background

Danger:
- Background: Red-600
- Text: White
- Use for destructive actions

Ghost:
- Background: Transparent
- Text: Gray-600
- Hover: Gray-100 background

**Inputs:**
- Border: 1px solid Gray-300
- Border radius: 6px
- Padding: 10px 12px
- Focus: Primary blue border, subtle shadow
- Error state: Red border
- Disabled: Gray-100 background, Gray-400 text

**Badges/Tags:**
- Small, rounded rectangles
- Padding: 4px 8px
- Font size: 12px
- Color-coded by status:
  - Strong Match: Green background, dark green text
  - Partial Match: Amber background, dark amber text
  - Missing: Red background, dark red text
  - Status: Gray background, dark gray text


## Application Layout

### Overall Structure

```
┌─────────────────────────────────────────────────────┐
│ Top Navigation Bar                                   │
├──────────┬──────────────────────────────────────────┤
│          │                                           │
│ Sidebar  │  Main Content Area                        │
│          │                                           │
│          │                                           │
│          │                                           │
│          │                                           │
└──────────┴──────────────────────────────────────────┘
```

### Top Navigation

**Contents:**
- Logo/App name (left)
- User profile menu (right)
- Notifications icon (optional, right)

**Style:**
- Height: 64px
- Background: White
- Border bottom: 1px solid Gray-200
- Fixed position on scroll

### Sidebar Navigation

**Contents:**
- Dashboard
- Resumes
- Applications
- Interview Prep
- Insights (optional)
- Settings

**Style:**
- Width: 240px (collapsed: 64px)
- Background: Gray-50
- Icons + labels
- Active state: Primary blue background, white text
- Hover state: Gray-100 background

**Behavior:**
- Collapsible on mobile
- Persistent on desktop
- Active route highlighted

### Main Content Area

**Structure:**
- Page header with title and actions
- Content sections in cards
- Generous spacing between sections
- Max width: 1200px (centered)


## Key User Flows & Screens

### Dashboard

**Purpose:** Central hub for quick access to recent activity and common actions

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│ Dashboard                                            │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│ │ Quick Action │  │ Quick Action │  │ Quick      │ │
│ │ Upload Resume│  │ New App      │  │ Action     │ │
│ └──────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
│ Recent Applications                                  │
│ ┌──────────────────────────────────────────────┐   │
│ │ Company | Role | Status | Date | Actions     │   │
│ │ ...                                           │   │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ Your Resumes                                         │
│ ┌──────────────────────────────────────────────┐   │
│ │ Resume cards with preview and actions        │   │
│ └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Components:**
- Quick action cards (3-4 prominent actions)
- Recent applications table (5-10 most recent)
- Resume library (card grid)
- Stats overview (optional: applications this month, interviews, etc.)

**UX Considerations:**
- One-click access to common tasks
- Clear visual hierarchy
- Scannable at a glance
- Empty states with helpful CTAs


### Resume Upload & Management

**Upload Flow:**

1. **Upload Screen**
   - Large drop zone (dashed border)
   - "Drop file here or click to browse"
   - Supported formats clearly stated (PDF, DOCX)
   - File size limit shown (5MB)
   - Drag-and-drop visual feedback

2. **Parsing State**
   - Loading spinner with message
   - "Analyzing your resume..."
   - Progress indication if possible
   - Cancel option

3. **Review Parsed Data**
   - Structured display of extracted information
   - Sections: Contact, Experience, Education, Skills, Projects
   - Edit capability for corrections
   - "Looks good" confirmation button
   - "Re-upload" option if parsing failed

**Resume Library:**
- Card grid layout (2-3 columns on desktop)
- Each card shows:
  - Resume name (editable)
  - Upload date
  - Preview thumbnail (optional)
  - Actions: View, Edit, Delete, Use for Application
- Default resume indicator
- Search/filter if many resumes

**UX Considerations:**
- Clear error messages for unsupported formats
- Ability to edit parsed data before saving
- Visual confirmation of successful upload
- Easy access to previously uploaded resumes


### New Application Flow

**Step 1: Select Resume**
- Grid of available resumes
- Radio selection or card selection
- Preview on hover
- "Continue" button

**Step 2: Job Description Input**
- Large textarea for JD paste
- Character count indicator
- Optional fields:
  - Company name (auto-extracted but editable)
  - Job title (auto-extracted but editable)
  - Job URL (optional)
- "Analyze" button (primary, prominent)
- Save as draft option

**Step 3: Fit Analysis Results**

Layout:
```
┌─────────────────────────────────────────────────────┐
│ Fit Analysis: [Job Title] at [Company]              │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Overall Match: 75%  [Visual progress bar]           │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Strong Matches (5)                           │    │
│ │ ✓ Python - 3 years experience in projects   │    │
│ │ ✓ REST APIs - Built FastAPI applications    │    │
│ │ ...                                          │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Partial Matches (3)                          │    │
│ │ ⚠ AWS - Cloud deployment experience         │    │
│ │   Gap: No specific AWS services mentioned   │    │
│ │ ...                                          │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Missing Requirements (2)                     │    │
│ │ ✗ Kubernetes - No evidence in resume        │    │
│ │ ✗ GraphQL - Not mentioned                   │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ [Continue to Tailoring] [Save Analysis]             │
└─────────────────────────────────────────────────────┘
```

**Visual Design:**
- Color-coded sections (green, amber, red)
- Expandable items for detailed evidence
- Clear iconography (✓, ⚠, ✗)
- Progress bar for overall match
- Collapsible sections if content is long

**UX Considerations:**
- Honest, transparent presentation of gaps
- Evidence shown for each match
- No false positives
- Easy to scan and understand
- Clear next steps


### Resume Tailoring & Review

**Step 4: Tailoring Suggestions**

Layout:
```
┌─────────────────────────────────────────────────────┐
│ Resume Tailoring Suggestions                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Review and approve changes to optimize your resume  │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Suggestion 1: Reorder Experience              │    │
│ │                                               │    │
│ │ Move "Software Engineer Intern" to top       │    │
│ │ Reason: Most relevant to JD requirements     │    │
│ │                                               │    │
│ │ [✓ Accept] [✗ Reject]                        │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Suggestion 2: Rephrase Bullet Point          │    │
│ │                                               │    │
│ │ Before:                                       │    │
│ │ Built web application for user management    │    │
│ │                                               │    │
│ │ After:                                        │    │
│ │ Developed full-stack web application using   │    │
│ │ React and Node.js for user management        │    │
│ │                                               │    │
│ │ Reason: Emphasizes React and Node.js from JD │    │
│ │                                               │    │
│ │ [✓ Accept] [✏️ Edit] [✗ Reject]              │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ [Preview Tailored Resume] [Accept All] [Reject All] │
└─────────────────────────────────────────────────────┘
```

**Diff Display for Rephrasing:**
- Side-by-side or inline diff
- Deletions in red with strikethrough
- Additions in green with highlight
- Unchanged text in normal style
- Monospace font for clarity

**Individual Suggestion Card:**
- Clear suggestion type (badge)
- Before/after comparison
- Reasoning explanation
- Evidence from resume
- JD alignment note
- Three actions: Accept, Edit, Reject
- Visual feedback on selection

**Bulk Actions:**
- Accept all / Reject all (with confirmation)
- Filter by suggestion type
- Show only pending suggestions
- Counter: "3 of 8 suggestions accepted"

**UX Considerations:**
- Easy to review one by one
- Clear visual diff for changes
- Ability to manually edit suggestions
- No auto-apply; explicit approval required
- Progress tracking
- Can save and return later


**Step 5: Preview & Generate**

Layout:
```
┌─────────────────────────────────────────────────────┐
│ Preview Tailored Resume                              │
├─────────────────────────────────────────────────────┤
│                                                      │
│ ┌─────────────────┐  ┌─────────────────────────┐   │
│ │                 │  │ [Your Name]              │   │
│ │  Resume         │  │ [Contact Info]           │   │
│ │  Preview        │  │                          │   │
│ │  (Read-only)    │  │ Experience               │   │
│ │                 │  │ • [Bullet with changes]  │   │
│ │                 │  │ • [Bullet]               │   │
│ │                 │  │                          │   │
│ │                 │  │ Education                │   │
│ │                 │  │ ...                      │   │
│ │                 │  │                          │   │
│ └─────────────────┘  └─────────────────────────┘   │
│                                                      │
│ Changes Applied: 5 suggestions accepted              │
│                                                      │
│ [← Back to Edit] [Generate Resume]                   │
└─────────────────────────────────────────────────────┘
```

**Preview Display:**
- Two-column layout (preview + formatted view)
- Highlight applied changes (subtle green background)
- Read-only formatted preview
- Summary of changes applied
- Back button to modify
- Generate button (primary, prominent)

**Generation State:**
- Loading indicator
- "Generating your tailored resume..."
- Progress message

**Success State:**
- Success message with checkmark
- Download button (primary)
- Preview generated document
- Save to applications option
- Generate cover letter CTA

**UX Considerations:**
- Final review before generation
- Clear indication of what changed
- Easy to go back and modify
- Predictable output format
- Immediate download after generation


### Cover Letter Generation

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│ Generate Cover Letter                                │
├─────────────────────────────────────────────────────┤
│                                                      │
│ Optional Context (helps personalization):            │
│ ┌─────────────────────────────────────────────┐    │
│ │ How did you find this role?                  │    │
│ │ [Text input]                                 │    │
│ │                                              │    │
│ │ Why are you interested in this company?     │    │
│ │ [Text input]                                 │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ Tone:                                                │
│ ○ Professional  ○ Enthusiastic  ○ Conversational    │
│                                                      │
│ [Generate Cover Letter]                              │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Generated Cover Letter                       │    │
│ │                                              │    │
│ │ [Editable text area with generated content] │    │
│ │                                              │    │
│ │ Word count: 325                              │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ Evidence Map:                                        │
│ • "3 years Python experience" → Resume: Experience  │
│ • "FastAPI project" → Resume: Projects section      │
│                                                      │
│ [Regenerate] [Copy to Clipboard] [Download]         │
└─────────────────────────────────────────────────────┘
```

**Features:**
- Optional context inputs for personalization
- Tone selection (radio buttons)
- Editable output (textarea)
- Word count indicator
- Evidence mapping (collapsible)
- Regenerate option
- Copy and download actions

**UX Considerations:**
- Generated content is editable
- Clear evidence for claims
- Multiple export options
- Can regenerate with different tone
- Save draft functionality


### Application Tracking

**Applications List View:**

```
┌─────────────────────────────────────────────────────┐
│ My Applications                    [+ New Application]│
├─────────────────────────────────────────────────────┤
│                                                      │
│ Filters: [All] [Applied] [Interviewing] [Offer]     │
│ Sort by: [Date ▼]                                    │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ Software Engineer                             │   │
│ │ Acme Corp                                     │   │
│ │                                               │   │
│ │ Status: Interviewing  Applied: Jan 15, 2026  │   │
│ │                                               │   │
│ │ [View Details] [Update Status] [Interview Prep]│  │
│ └──────────────────────────────────────────────┘   │
│                                                      │
│ ┌──────────────────────────────────────────────┐   │
│ │ Frontend Developer                            │   │
│ │ Tech Startup Inc                              │   │
│ │                                               │   │
│ │ Status: Applied  Applied: Jan 10, 2026       │   │
│ │                                               │   │
│ │ [View Details] [Update Status] [Interview Prep]│  │
│ └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Application Card:**
- Job title (prominent)
- Company name
- Status badge (color-coded)
- Application date
- Quick actions
- Hover: Show more details

**Status Options:**
- Applied (blue)
- Interviewing (amber)
- Offer (green)
- Rejected (red)
- Withdrawn (gray)

**Detail View:**
- Full job description
- Resume used
- Fit analysis results
- Cover letter (if generated)
- Timeline of status changes
- Notes section (editable)
- Documents attached
- Interview prep link

**UX Considerations:**
- Lightweight, not overwhelming
- Quick status updates
- Easy filtering and sorting
- Minimal required fields
- Focus on actionable information
- Link to interview prep


### Interview Preparation

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│ Interview Prep: [Job Title] at [Company]            │
├─────────────────────────────────────────────────────┤
│                                                      │
│ [Generate Prep Materials] (if not generated yet)    │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Technical Questions                          │    │
│ │                                              │    │
│ │ 1. Explain how you would design a REST API  │    │
│ │    [Toggle notes]                            │    │
│ │                                              │    │
│ │ 2. What is your experience with Python?     │    │
│ │    [Toggle notes]                            │    │
│ │                                              │    │
│ │ ...                                          │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Behavioral Questions                         │    │
│ │                                              │    │
│ │ 1. Tell me about a time you led a project   │    │
│ │    [Toggle STAR example]                     │    │
│ │                                              │    │
│ │    Situation: At my internship...            │    │
│ │    Task: I was responsible for...            │    │
│ │    Action: I organized...                    │    │
│ │    Result: We delivered...                   │    │
│ │                                              │    │
│ │ ...                                          │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ ┌─────────────────────────────────────────────┐    │
│ │ Questions to Ask                             │    │
│ │                                              │    │
│ │ • What does success look like in this role? │    │
│ │ • How does the team collaborate?            │    │
│ │ ...                                          │    │
│ └─────────────────────────────────────────────┘    │
│                                                      │
│ [Print Prep Sheet] [Export PDF] [Add Notes]         │
└─────────────────────────────────────────────────────┘
```

**Features:**
- Collapsible sections for each category
- Expandable questions with notes
- STAR examples pre-filled from resume
- Editable notes for each question
- Print-friendly format
- Export to PDF

**Visual Design:**
- Clean, scannable layout
- Numbered lists for questions
- Indented STAR components
- Checkbox for "prepared" status (optional)
- Minimal styling for easy reading

**UX Considerations:**
- Easy to skim quickly
- Expandable for detail
- Editable for personalization
- Print/export for offline use
- Linked to specific application
- Can regenerate if JD changes


## Interaction Patterns

### Loading States

**Principles:**
- Always show loading feedback for operations > 200ms
- Use skeleton screens for content loading
- Use spinners for actions (buttons)
- Show progress messages for AI operations
- Provide cancel option for long operations

**Examples:**

Parsing Resume:
```
┌─────────────────────────────────────┐
│  [Spinner] Analyzing your resume... │
│                                     │
│  This may take 10-15 seconds        │
│                                     │
│  [Cancel]                           │
└─────────────────────────────────────┘
```

Generating Suggestions:
```
┌─────────────────────────────────────┐
│  [Spinner] Generating tailoring     │
│            suggestions...            │
│                                     │
│  Analyzing fit: ✓                   │
│  Creating suggestions: ...          │
└─────────────────────────────────────┘
```

### Empty States

**Principles:**
- Friendly, helpful messaging
- Clear call-to-action
- Optional illustration (simple, professional)
- Explain what the section will contain

**Examples:**

No Resumes:
```
┌─────────────────────────────────────┐
│                                     │
│     [Simple icon]                   │
│                                     │
│  No resumes yet                     │
│                                     │
│  Upload your first resume to get    │
│  started with tailored applications │
│                                     │
│  [Upload Resume]                    │
│                                     │
└─────────────────────────────────────┘
```

No Applications:
```
┌─────────────────────────────────────┐
│                                     │
│  Start tracking your applications   │
│                                     │
│  Keep all your job applications     │
│  organized in one place             │
│                                     │
│  [Create First Application]         │
│                                     │
└─────────────────────────────────────┘
```


### Error States

**Principles:**
- Clear, non-technical error messages
- Explain what went wrong
- Provide actionable next steps
- Offer retry or alternative actions
- Use appropriate tone (helpful, not blaming)

**Examples:**

Upload Failed:
```
┌─────────────────────────────────────┐
│  ⚠ Upload Failed                    │
│                                     │
│  We couldn't process this file.     │
│  Please try:                        │
│  • Using PDF or DOCX format         │
│  • Ensuring file is under 5MB       │
│  • Checking file isn't corrupted    │
│                                     │
│  [Try Again] [Choose Different File]│
└─────────────────────────────────────┘
```

AI Generation Failed:
```
┌─────────────────────────────────────┐
│  ⚠ Generation Failed                │
│                                     │
│  We couldn't generate suggestions.  │
│  This might be because:             │
│  • The job description is too vague │
│  • Your resume needs more detail    │
│                                     │
│  [Try Again] [Edit Resume] [Contact Support]│
└─────────────────────────────────────┘
```

### Success Feedback

**Principles:**
- Confirm successful actions
- Use checkmark icon
- Brief, positive message
- Auto-dismiss after 3-5 seconds (for toasts)
- Provide next action when appropriate

**Examples:**

Toast Notification:
```
┌─────────────────────────────────────┐
│  ✓ Resume uploaded successfully     │
└─────────────────────────────────────┘
```

Inline Success:
```
┌─────────────────────────────────────┐
│  ✓ Tailored resume generated        │
│                                     │
│  Your resume is ready to download   │
│                                     │
│  [Download Resume] [View Preview]   │
└─────────────────────────────────────┘
```


### Modals & Dialogs

**Usage:**
- Confirmation for destructive actions
- Forms that require focus
- Important information that needs attention
- Keep content minimal

**Structure:**
- Header with title
- Content area
- Action buttons (right-aligned)
- Close button (X in top-right)
- Overlay background (semi-transparent black)

**Example - Delete Confirmation:**
```
        ┌─────────────────────────────┐
        │ Delete Resume?           [X]│
        ├─────────────────────────────┤
        │                             │
        │ Are you sure you want to    │
        │ delete "Software Engineer   │
        │ Resume v2"?                 │
        │                             │
        │ This action cannot be       │
        │ undone.                     │
        │                             │
        │         [Cancel] [Delete]   │
        └─────────────────────────────┘
```

**Best Practices:**
- Use sparingly
- Clear title and message
- Primary action on right
- Destructive actions in red
- ESC key to close
- Click outside to close (for non-critical)

### Tooltips

**Usage:**
- Explain icons or abbreviated labels
- Provide additional context
- Show keyboard shortcuts

**Style:**
- Small, dark background
- White text
- Arrow pointing to element
- Appear on hover (delay: 500ms)
- Max width: 200px

**Example:**
```
  [?]  ← Hover target
  ↓
┌─────────────────────────┐
│ This score represents   │
│ how well your resume    │
│ matches the job         │
│ requirements            │
└─────────────────────────┘
```


## Animation & Motion

### Principles

**Use animation to:**
- Provide feedback for user actions
- Guide attention to important changes
- Smooth transitions between states
- Indicate loading or processing

**Don't use animation for:**
- Decoration without purpose
- Slowing down the interface
- Distracting from content
- Making users wait unnecessarily

### Animation Guidelines

**Duration:**
- Micro-interactions: 100-200ms (hover, focus)
- Transitions: 200-300ms (page changes, modals)
- Loading states: Continuous until complete
- Never exceed 500ms for UI animations

**Easing:**
- Use ease-out for entering elements
- Use ease-in for exiting elements
- Use ease-in-out for moving elements
- Avoid linear easing (feels robotic)

**Examples:**

Button Hover:
- Duration: 150ms
- Property: background-color
- Easing: ease-out

Modal Open:
- Duration: 250ms
- Properties: opacity, transform (scale)
- Easing: ease-out

Page Transition:
- Duration: 200ms
- Property: opacity
- Easing: ease-in-out

Loading Spinner:
- Continuous rotation
- Smooth, consistent speed

### Reduced Motion

**Accessibility:**
- Respect `prefers-reduced-motion` media query
- Disable decorative animations
- Keep functional animations (loading indicators)
- Use instant transitions instead

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```


## Responsive Design

### Breakpoints

- Mobile: < 640px (single column)
- Tablet: 640px - 1024px (flexible layout)
- Desktop: > 1024px (full layout with sidebar)

### Mobile Adaptations

**Navigation:**
- Hamburger menu for sidebar
- Bottom navigation bar (optional)
- Collapsible sections

**Layout:**
- Single column layout
- Stack cards vertically
- Full-width components
- Larger touch targets (min 44x44px)

**Typography:**
- Slightly smaller font sizes
- Maintain readability (min 16px body)
- Reduce heading sizes proportionally

**Interactions:**
- Touch-friendly buttons and controls
- Swipe gestures where appropriate
- Avoid hover-dependent interactions
- Larger form inputs

### Tablet Adaptations

**Layout:**
- Two-column grid where appropriate
- Collapsible sidebar
- Flexible card layouts
- Maintain desktop functionality

**Navigation:**
- Icon-only sidebar (collapsed)
- Full sidebar on demand

### Desktop Optimizations

**Layout:**
- Multi-column layouts
- Persistent sidebar
- Wider content areas
- Side-by-side comparisons

**Interactions:**
- Keyboard shortcuts
- Hover states
- Drag and drop (where useful)
- Multi-select capabilities


## Accessibility

### WCAG Compliance

**Target:** WCAG 2.1 AA compliance minimum

**Key Requirements:**

**Color Contrast:**
- Text: 4.5:1 minimum (normal text)
- Large text: 3:1 minimum (18px+ or 14px+ bold)
- UI components: 3:1 minimum
- Don't rely on color alone for information

**Keyboard Navigation:**
- All interactive elements keyboard accessible
- Visible focus indicators
- Logical tab order
- Skip links for main content
- Keyboard shortcuts documented

**Screen Readers:**
- Semantic HTML elements
- ARIA labels where needed
- Alt text for images
- Form labels properly associated
- Status messages announced

**Focus Management:**
- Clear focus indicators (2px outline)
- Focus trap in modals
- Return focus after modal close
- Skip navigation links

### Semantic HTML

Use proper HTML elements:
- `<button>` for actions
- `<a>` for navigation
- `<nav>` for navigation sections
- `<main>` for main content
- `<header>`, `<footer>` for page structure
- `<h1>` - `<h6>` for headings (hierarchical)
- `<form>` for forms
- `<label>` for form labels

### ARIA Attributes

Use when semantic HTML isn't enough:
- `aria-label` for icon buttons
- `aria-describedby` for additional context
- `aria-live` for dynamic content updates
- `aria-expanded` for collapsible sections
- `role` attributes when needed

**Example:**
```html
<button aria-label="Delete resume" aria-describedby="delete-warning">
  <TrashIcon />
</button>
<span id="delete-warning" class="sr-only">
  This action cannot be undone
</span>
```


### Form Accessibility

**Labels:**
- Every input has a visible label
- Labels properly associated with inputs
- Placeholder text is not a substitute for labels

**Validation:**
- Clear error messages
- Errors announced to screen readers
- Error summary at top of form
- Inline validation after blur
- Success confirmation

**Example:**
```html
<div class="form-field">
  <label for="company-name">Company Name</label>
  <input 
    id="company-name" 
    type="text"
    aria-required="true"
    aria-invalid="false"
    aria-describedby="company-error"
  />
  <span id="company-error" class="error" role="alert">
    <!-- Error message appears here -->
  </span>
</div>
```

### Screen Reader Only Content

Use for context that's visual but needs to be announced:

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

**Usage:**
- Loading state messages
- Icon button labels
- Status updates
- Navigation hints


## Content Guidelines

### Writing Principles

**Tone:**
- Professional but approachable
- Clear and direct
- Supportive and encouraging
- Honest and transparent
- Action-oriented

**Voice:**
- Use "you" and "your" (user-focused)
- Use active voice
- Be concise
- Avoid jargon
- Use plain language

### UI Copy Examples

**Buttons:**
- Good: "Upload Resume", "Generate Cover Letter", "Accept Suggestion"
- Avoid: "Submit", "OK", "Click Here"

**Headings:**
- Good: "Review Tailoring Suggestions", "Your Applications"
- Avoid: "Suggestions", "Apps"

**Empty States:**
- Good: "No resumes yet. Upload your first resume to get started."
- Avoid: "No data available."

**Error Messages:**
- Good: "We couldn't upload your file. Please try a PDF or DOCX format."
- Avoid: "Error: Invalid file type."

**Success Messages:**
- Good: "Resume uploaded successfully"
- Avoid: "Operation completed"

### Microcopy

**Form Labels:**
- Clear and specific
- Use sentence case
- Include help text when needed

**Placeholders:**
- Show example format
- Don't replace labels
- Use sparingly

**Help Text:**
- Brief and helpful
- Appears below input
- Explains format or requirements

**Example:**
```
Company Name
[Input field]
The company you're applying to

Job Title
[Input field]
e.g., "Senior Software Engineer"
```


## Performance & Optimization

### Performance Targets

- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1
- First Input Delay: < 100ms

### Optimization Strategies

**Images:**
- Use WebP format with fallbacks
- Lazy load below-the-fold images
- Provide appropriate sizes for responsive
- Compress images (80-85% quality)
- Use SVG for icons and logos

**Fonts:**
- Limit to 2 font families
- Use system fonts when possible
- Subset fonts to required characters
- Use font-display: swap

**Code Splitting:**
- Route-based code splitting
- Lazy load heavy components
- Dynamic imports for modals
- Separate vendor bundles

**Caching:**
- Cache static assets
- Use SWR/React Query for data
- Implement optimistic updates
- Cache AI responses when appropriate

**Loading Strategies:**
- Show skeleton screens
- Progressive enhancement
- Prioritize above-the-fold content
- Defer non-critical JavaScript

### Perceived Performance

**Techniques:**
- Optimistic UI updates
- Instant feedback for actions
- Skeleton screens during loading
- Progressive loading of content
- Smooth transitions between states

**Example - Optimistic Update:**
```
User clicks "Accept Suggestion"
→ Immediately show as accepted (optimistic)
→ Send request to server
→ If fails, revert and show error
→ If succeeds, keep accepted state
```


## Design Checklist

### Before Implementation

**Design Review:**
- [ ] Follows design system guidelines
- [ ] Consistent spacing and typography
- [ ] Proper color usage
- [ ] Clear visual hierarchy
- [ ] Responsive design considered
- [ ] Accessibility requirements met
- [ ] Loading and error states designed
- [ ] Empty states designed

**UX Review:**
- [ ] User flow is logical
- [ ] Actions are clear and discoverable
- [ ] Feedback is provided for all actions
- [ ] Error prevention measures in place
- [ ] Help text where needed
- [ ] Keyboard navigation works
- [ ] Mobile experience considered

### During Implementation

**Code Quality:**
- [ ] Semantic HTML used
- [ ] ARIA attributes where needed
- [ ] Proper form labels
- [ ] Focus management implemented
- [ ] Keyboard shortcuts work
- [ ] Responsive breakpoints tested

**Testing:**
- [ ] Tested in Chrome, Firefox, Safari
- [ ] Tested on mobile devices
- [ ] Tested with keyboard only
- [ ] Tested with screen reader
- [ ] Tested loading states
- [ ] Tested error states
- [ ] Tested empty states

### Before Launch

**Final Checks:**
- [ ] All interactive elements accessible
- [ ] Color contrast meets WCAG AA
- [ ] Performance targets met
- [ ] No console errors
- [ ] Analytics events implemented
- [ ] Error tracking configured
- [ ] User feedback mechanism in place


## Component Library Recommendations

### Suggested Libraries

**UI Components:**
- Headless UI (accessible components)
- Radix UI (unstyled primitives)
- shadcn/ui (copy-paste components)

**Styling:**
- Tailwind CSS (utility-first)
- CSS Modules (scoped styles)

**Icons:**
- Heroicons (clean, professional)
- Lucide Icons (consistent style)

**Forms:**
- React Hook Form (performance)
- Zod (validation)

**Data Fetching:**
- React Query / SWR (caching, optimistic updates)

### Custom Components to Build

**Core Components:**
- Button (variants: primary, secondary, danger, ghost)
- Input (text, textarea, select)
- Card (container for content sections)
- Badge (status indicators)
- Modal (confirmations, forms)
- Toast (notifications)
- Dropdown (menus, selects)
- Tabs (content organization)

**Application-Specific:**
- ResumeCard (resume library display)
- ApplicationCard (application tracking)
- FitAnalysisDisplay (match visualization)
- DiffViewer (before/after comparison)
- SuggestionCard (tailoring suggestions)
- ProgressBar (match percentage)

### Component Documentation

Each component should have:
- Props interface (TypeScript)
- Usage examples
- Accessibility notes
- Variants and states
- Responsive behavior

**Example:**
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick: () => void;
  children: React.ReactNode;
}
```


## User Feedback & Iteration

### Feedback Collection

**Methods:**
- In-app feedback button
- Post-action surveys (optional)
- Usage analytics
- Error tracking
- User interviews (for major features)

**What to Track:**
- Feature usage rates
- Completion rates for flows
- Time to complete tasks
- Error rates
- User satisfaction scores

### Metrics to Monitor

**Engagement:**
- Daily/weekly active users
- Feature adoption rates
- Return user rate
- Session duration

**Efficiency:**
- Time to complete application flow
- Number of clicks to complete tasks
- Suggestion acceptance rate
- Resume generation success rate

**Quality:**
- Error rates by feature
- User-reported issues
- Validation failure rates
- Support ticket volume

### Iteration Process

1. **Collect Data:** Analytics, feedback, support tickets
2. **Identify Issues:** Patterns in user behavior or complaints
3. **Prioritize:** Impact vs. effort
4. **Design Solutions:** Iterate on designs
5. **Test:** User testing or A/B testing
6. **Implement:** Roll out changes
7. **Measure:** Track impact on metrics
8. **Repeat:** Continuous improvement

### A/B Testing Opportunities

- Button copy variations
- Layout alternatives
- Onboarding flow variations
- Feature placement
- Color scheme variations
- Call-to-action wording


## Common UI Patterns

### Progressive Disclosure

**Principle:** Show only what's necessary, reveal more on demand

**Examples:**
- Collapsible sections for detailed information
- "Show more" links for long content
- Expandable cards for additional details
- Tabs for organizing related content
- Accordions for FAQ or help content

### Confirmation Patterns

**When to Confirm:**
- Destructive actions (delete, remove)
- Actions that can't be undone
- Actions with significant consequences
- Bulk operations

**When Not to Confirm:**
- Reversible actions
- Low-risk operations
- Frequent actions
- Actions with clear undo

**Example:**
```
Delete Resume
Are you sure you want to delete "Resume v2"?
This action cannot be undone.

[Cancel] [Delete]
```

### Undo Patterns

**Preferred over confirmation for:**
- Frequent actions
- Low-risk operations
- Actions that can be reversed

**Implementation:**
```
Toast: "Resume deleted" [Undo]
→ Auto-dismiss after 5 seconds
→ Click Undo to restore
```

### Inline Editing

**Use for:**
- Quick edits to existing content
- Single field updates
- Frequent modifications

**Pattern:**
- Display mode: Show value with edit icon
- Edit mode: Replace with input field
- Actions: Save/Cancel or auto-save on blur
- Validation: Inline error messages


## Mobile-Specific Considerations

### Touch Targets

**Minimum Sizes:**
- Buttons: 44x44px minimum
- Links: 44x44px tap area (padding)
- Form inputs: 44px height minimum
- Icons: 24x24px with 44x44px tap area

**Spacing:**
- Minimum 8px between touch targets
- Prefer 16px spacing for comfort

### Mobile Navigation

**Patterns:**
- Bottom navigation bar (3-5 items)
- Hamburger menu for secondary items
- Swipe gestures for navigation
- Back button in header

**Example Bottom Nav:**
```
┌─────────────────────────────────────┐
│                                     │
│         Main Content                │
│                                     │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ [Home] [Resumes] [Apps] [Profile]  │
└─────────────────────────────────────┘
```

### Mobile Forms

**Optimizations:**
- Appropriate input types (email, tel, number)
- Minimize typing with selects/radios
- Auto-capitalize where appropriate
- Show password toggle
- Large, easy-to-tap buttons
- Sticky submit button

**Input Types:**
```html
<input type="email" inputmode="email" />
<input type="tel" inputmode="tel" />
<input type="number" inputmode="numeric" />
<input type="url" inputmode="url" />
```

### Mobile Gestures

**Common Gestures:**
- Swipe to delete (lists)
- Pull to refresh (lists)
- Swipe between tabs
- Pinch to zoom (images)
- Long press for context menu

**Implementation:**
- Provide visual feedback
- Include alternative button actions
- Don't rely solely on gestures
- Educate users on first use


## Dark Mode (Future Enhancement)

### Considerations

**If implementing dark mode:**

**Color Adjustments:**
- Background: Dark gray (#1F2937), not pure black
- Text: Light gray (#F9FAFB), not pure white
- Reduce contrast slightly (easier on eyes)
- Adjust color saturation (less vibrant)
- Maintain WCAG contrast ratios

**Component Adjustments:**
- Reduce shadows (use borders instead)
- Adjust card backgrounds (lighter than page)
- Invert icon colors
- Adjust image brightness

**Implementation:**
- Use CSS custom properties
- Respect system preference
- Provide manual toggle
- Persist user preference
- Test all components in both modes

**Example:**
```css
:root {
  --bg-primary: #FFFFFF;
  --text-primary: #111827;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #1F2937;
    --text-primary: #F9FAFB;
  }
}
```

**Priority:** Low for MVP, consider for future enhancement


## Summary

This UI/UX steering document establishes the design foundation for the AI Job Application Copilot. The interface should feel like a professional productivity tool that users trust and want to use repeatedly.

### Key Principles Recap

1. **Trust Through Transparency** - Always show what the AI is doing and why
2. **Efficiency Over Novelty** - Optimize for repeated use
3. **Control Over Automation** - Users approve all changes
4. **Clarity Over Density** - Use space generously
5. **Professional Over Playful** - This is a career tool

### Design System Essentials

- Minimal color palette (blue, green, amber, red, grays)
- Clean typography (Inter font family)
- Consistent spacing (4px base unit)
- Card-based layout
- Clear visual hierarchy
- Accessible by default (WCAG AA minimum)

### Critical UX Patterns

- Dashboard-first navigation
- Simple resume upload and management
- Visual fit analysis with color-coded matches
- Diff-based review for tailoring suggestions
- Individual accept/reject for all AI suggestions
- Preview before final generation
- Lightweight application tracking
- Scannable interview prep materials

### Implementation Priorities

**MVP Focus:**
- Core user flows (upload → analyze → tailor → generate)
- Essential components (buttons, cards, forms, modals)
- Responsive design (mobile, tablet, desktop)
- Accessibility fundamentals
- Loading and error states

**Post-MVP:**
- Advanced interactions (drag-and-drop, inline editing)
- Dark mode
- Advanced animations
- Keyboard shortcuts
- Onboarding flow

### Success Metrics

The UI is successful when:
- Users complete application flow quickly (< 5 minutes)
- High suggestion acceptance rate (> 70%)
- Low error rates
- High return user rate
- Positive user feedback on clarity and trust

---

**Document Version:** 1.0  
**Last Updated:** April 1, 2026  
**Maintained By:** Design Team  
**Review Frequency:** Quarterly or after major feature releases
