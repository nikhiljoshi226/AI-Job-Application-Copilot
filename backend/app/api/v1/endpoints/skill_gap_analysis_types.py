"""Type definitions for skill gap analysis API endpoints."""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class SkillGapAnalysisRequest(BaseModel):
    """Request model for skill gap analysis."""
    resume_id: int = Field(..., description="ID of the resume to analyze")
    job_description_ids: List[int] = Field(..., description="List of job description IDs to analyze")
    analysis_name: Optional[str] = Field(None, description="Custom name for the analysis")
    analysis_options: Optional[Dict[str, Any]] = Field(None, description="Analysis configuration options")


class SkillGapAnalysisResponse(BaseModel):
    """Response model for skill gap analysis."""
    success: bool = Field(..., description="Whether the analysis was successful")
    analysis_id: Optional[int] = Field(None, description="ID of the created analysis")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Analysis results")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    validation_errors: List[str] = Field(default_factory=list, description="List of validation errors")


class SkillGapAnalysisUpdateRequest(BaseModel):
    """Request model for updating skill gap analysis."""
    analysis_name: Optional[str] = Field(None, description="Updated analysis name")
    analysis_summary: Optional[Dict[str, Any]] = Field(None, description="Updated analysis summary")
    learning_recommendations: Optional[List[Dict[str, Any]]] = Field(None, description="Updated learning recommendations")
    project_suggestions: Optional[List[Dict[str, Any]]] = Field(None, description="Updated project suggestions")
    action_items: Optional[List[Dict[str, Any]]] = Field(None, description="Updated action items")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata")


class SkillGapAnalysisSummaryResponse(BaseModel):
    """Response model for skill gap analysis summary."""
    analysis_name: str = Field(..., description="Name of the analysis")
    job_count: int = Field(..., description="Number of jobs analyzed")
    skill_coverage_score: float = Field(..., description="Overall skill coverage score")
    analysis_summary: Dict[str, Any] = Field(..., description="Analysis summary")
    missing_skills_count: int = Field(..., description="Number of missing skills")
    repeated_gaps_count: int = Field(..., description="Number of repeated gaps")
    critical_gaps_count: int = Field(..., description="Number of critical gaps")
    learning_recommendations_count: int = Field(..., description="Number of learning recommendations")
    project_suggestions_count: int = Field(..., description="Number of project suggestions")
    action_items_count: int = Field(..., description="Number of action items")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")


class MissingSkillsResponse(BaseModel):
    """Response model for missing skills endpoint."""
    missing_skills: Dict[str, Any] = Field(..., description="Missing skills by category")
    total_missing: int = Field(..., description="Total number of missing skills")
    categories: Dict[str, int] = Field(..., description="Skill counts by category")


class RepeatedGapsResponse(BaseModel):
    """Response model for repeated gaps endpoint."""
    high_frequency_gaps: List[Dict[str, Any]] = Field(..., description="High-frequency skill gaps")
    critical_gaps: List[Dict[str, Any]] = Field(..., description="Critical skill gaps")
    category_gaps: Dict[str, List[Dict[str, Any]]] = Field(..., description="Gaps by category")
    gap_analysis: Dict[str, Any] = Field(..., description="Gap analysis summary")


class LearningRecommendationsResponse(BaseModel):
    """Response model for learning recommendations endpoint."""
    learning_recommendations: List[Dict[str, Any]] = Field(..., description="Learning recommendations")
    total_count: int = Field(..., description="Total number of recommendations")


class ProjectSuggestionsResponse(BaseModel):
    """Response model for project suggestions endpoint."""
    project_suggestions: List[Dict[str, Any]] = Field(..., description="Project suggestions")
    total_count: int = Field(..., description="Total number of suggestions")


class ActionItemsResponse(BaseModel):
    """Response model for action items endpoint."""
    action_items: List[Dict[str, Any]] = Field(..., description="Action items")
    total_count: int = Field(..., description="Total number of action items")


class AnalysisOptionsResponse(BaseModel):
    """Response model for analysis options endpoint."""
    analysis_options: Dict[str, Any] = Field(..., description="Available analysis options")
    skill_categories: List[Dict[str, Any]] = Field(..., description="Available skill categories")
