"""Type definitions for skill gap analysis."""

from typing import Dict, List, Any, Optional, TypedDict, Union
from enum import Enum


class SkillCategory(str, Enum):
    """Skill categories for analysis."""
    TECHNICAL = "technical"
    SOFT_SKILLS = "soft_skills"
    TOOLS = "tools"
    LANGUAGES = "languages"
    FRAMEWORKS = "frameworks"
    DATABASES = "databases"
    PLATFORMS = "platforms"


class ImportanceLevel(str, Enum):
    """Importance levels for skills."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Priority(str, Enum):
    """Priority levels for recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Difficulty(str, Enum):
    """Difficulty levels for projects."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Assessment(str, Enum):
    """Assessment levels for skill coverage."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    NEEDS_IMPROVEMENT = "needs_improvement"


class SkillInfo(TypedDict):
    """Information about a skill."""
    skill: str
    frequency: int
    importance: int
    jobs: List[str]
    companies: List[str]
    priority_score: float
    category: Optional[str]


class LearningRecommendation(TypedDict):
    """Learning recommendation for a skill."""
    type: str
    skill: Optional[str]
    category: Optional[str]
    title: str
    description: str
    priority: Priority
    time_estimate: str
    resources: List[str]
    learning_path: List[str]
    prerequisites: List[str]


class ProjectSuggestion(TypedDict):
    """Portfolio project suggestion."""
    title: str
    description: str
    skills_covered: List[str]
    difficulty: Difficulty
    time_estimate: str
    tech_stack: List[str]
    learning_outcomes: List[str]
    portfolio_value: str


class ActionItem(TypedDict):
    """Actionable recommendation."""
    type: str
    priority: Priority
    title: str
    description: str
    timeline: str
    resources: List[str]
    success_metrics: List[str]


class AnalysisOptions(TypedDict, total=False):
    """Options for skill gap analysis."""
    include_soft_skills: bool
    include_technical_skills: bool
    min_gap_frequency: int
    project_suggestion_count: int
    learning_recommendation_count: int
    priority_threshold: float


class TruthBank(TypedDict):
    """User's truth bank containing skills and experience."""
    skills: Dict[str, List[str]]
    experience: Dict[str, Union[List[str], int]]
    education: Dict[str, List[str]]
    projects: Dict[str, List[str]]


class SkillGap(TypedDict):
    """Skill gap information."""
    missing_technical: List[SkillInfo]
    missing_soft_skills: List[SkillInfo]
    missing_tools: List[SkillInfo]
    missing_languages: List[SkillInfo]
    missing_frameworks: List[SkillInfo]
    missing_databases: List[SkillInfo]
    missing_platforms: List[SkillInfo]
    gap_summary: Dict[str, Any]


class RepeatedGaps(TypedDict):
    """Repeated skill gaps analysis."""
    high_frequency_gaps: List[SkillInfo]
    critical_gaps: List[SkillInfo]
    category_gaps: Dict[str, List[SkillInfo]]
    gap_analysis: Dict[str, Any]


class RoleExpectations(TypedDict):
    """Common role expectations across job descriptions."""
    common_responsibilities: List[Dict[str, Any]]
    common_qualifications: List[Dict[str, Any]]
    experience_requirements: List[Dict[str, Any]]
    company_culture_aspects: List[str]
    industry_trends: List[str]


class AnalysisSummary(TypedDict):
    """Summary of the skill gap analysis."""
    overall_assessment: Assessment
    assessment_message: str
    skill_coverage_score: float
    total_missing_skills: int
    high_frequency_gaps: int
    critical_gaps: int
    key_findings: List[str]
    recommendations_summary: List[str]


class SkillGapAnalysisResult(TypedDict):
    """Complete skill gap analysis result."""
    analysis_name: str
    job_count: int
    analysis_summary: AnalysisSummary
    missing_skills: SkillGap
    repeated_gaps: RepeatedGaps
    role_expectations: RoleExpectations
    learning_recommendations: List[LearningRecommendation]
    project_suggestions: List[ProjectSuggestion]
    skill_coverage_score: float
    action_items: List[ActionItem]


class AnalysisMetadata(TypedDict):
    """Metadata for the analysis."""
    processing_time_ms: int
    analysis_options: AnalysisOptions
    generated_at: str


class CompleteAnalysisResult(TypedDict):
    """Complete result including metadata."""
    skill_gap_analysis: SkillGapAnalysisResult
    metadata: AnalysisMetadata
