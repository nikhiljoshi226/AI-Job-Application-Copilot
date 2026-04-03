"""Refactored skill gap analysis API endpoints with improved type safety and reduced duplication."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List

from app.core.database import get_db
from app.services.base_service import BaseService
from app.services.skill_gap import SkillGapAnalyzer
from .skill_gap_analysis_types import (
    SkillGapAnalysisRequest, SkillGapAnalysisResponse,
    SkillGapAnalysisUpdateRequest, SkillGapAnalysisSummaryResponse,
    MissingSkillsResponse, RepeatedGapsResponse,
    LearningRecommendationsResponse, ProjectSuggestionsResponse,
    ActionItemsResponse, AnalysisOptionsResponse
)

router = APIRouter()


class SkillGapAnalysisService(BaseService):
    """Service for skill gap analysis operations."""
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.analyzer = SkillGapAnalyzer()
    
    def create_analysis(self, request: SkillGapAnalysisRequest) -> SkillGapAnalysisResponse:
        """Create a new skill gap analysis."""
        try:
            user_id = self.get_current_user_id()
            
            # Verify resume ownership
            resume = self.verify_resume_ownership(request.resume_id, user_id)
            if not resume:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Resume not found"
                )
            
            # Verify job descriptions ownership
            job_descriptions = self.verify_job_descriptions_ownership(
                request.job_description_ids, user_id
            )
            if len(job_descriptions) != len(request.job_description_ids):
                found_ids = [jd.id for jd in job_descriptions]
                missing_ids = set(request.job_description_ids) - set(found_ids)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Job descriptions not found: {list(missing_ids)}"
                )
            
            # Prepare data for analysis
            resume_data = {"rendering_data": resume.rendering_content}
            job_descriptions_data = self.prepare_job_descriptions_data(job_descriptions)
            
            # Perform analysis
            result = self.analyzer.analyze_skill_gaps(
                resume_data, job_descriptions_data, request.analysis_options
            )
            
            # Create analysis record
            analysis = self.create_analysis_record(
                user_id=user_id,
                resume_id=request.resume_id,
                analysis_name=request.analysis_name or result["skill_gap_analysis"]["analysis_name"],
                job_description_ids=request.job_description_ids,
                analysis_result=result
            )
            
            return SkillGapAnalysisResponse(
                success=True,
                analysis_id=analysis.id,
                analysis=result
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error performing skill gap analysis: {str(e)}"
            )
    
    def get_analyses(self) -> Dict[str, Any]:
        """Get all skill gap analyses for current user."""
        try:
            user_id = self.get_current_user_id()
            
            from app.models.skill_gap_analysis import SkillGapAnalysis
            analyses = self.db.query(SkillGapAnalysis).filter(
                SkillGapAnalysis.user_id == user_id
            ).order_by(SkillGapAnalysis.created_at.desc()).all()
            
            return {
                "analyses": [
                    {
                        "id": analysis.id,
                        "analysis_name": analysis.analysis_name,
                        "resume_id": analysis.resume_id,
                        "job_description_ids": analysis.job_description_ids,
                        "job_count": len(analysis.job_description_ids),
                        "skill_coverage_score": analysis.skill_coverage_score,
                        "analysis_summary": analysis.analysis_summary,
                        "created_at": analysis.created_at,
                        "updated_at": analysis.updated_at,
                        "last_accessed_at": analysis.last_accessed_at
                    }
                    for analysis in analyses
                ],
                "total": len(analyses)
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching skill gap analyses: {str(e)}"
            )
    
    def get_analysis(self, analysis_id: int) -> Dict[str, Any]:
        """Get a specific skill gap analysis."""
        try:
            user_id = self.get_current_user_id()
            
            analysis = self.verify_analysis_ownership(analysis_id, user_id)
            if not analysis:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Skill gap analysis not found"
                )
            
            # Update last accessed time
            self.update_last_accessed(analysis)
            
            # Get related information
            resume = self.db.query(Resume).filter(
                Resume.id == analysis.resume_id
            ).first()
            
            job_descriptions = self.verify_job_descriptions_ownership(
                analysis.job_description_ids, user_id
            )
            
            return {
                "id": analysis.id,
                "analysis_name": analysis.analysis_name,
                "resume_id": analysis.resume_id,
                "job_description_ids": analysis.job_description_ids,
                "job_count": len(analysis.job_description_ids),
                "analysis_summary": analysis.analysis_summary,
                "missing_skills": analysis.missing_skills,
                "repeated_gaps": analysis.repeated_gaps,
                "role_expectations": analysis.role_expectations,
                "learning_recommendations": analysis.learning_recommendations,
                "project_suggestions": analysis.project_suggestions,
                "skill_coverage_score": analysis.skill_coverage_score,
                "action_items": analysis.action_items,
                "metadata": analysis.metadata,
                "created_at": analysis.created_at,
                "updated_at": analysis.updated_at,
                "last_accessed_at": analysis.last_accessed_at,
                "resume": {
                    "id": resume.id,
                    "title": resume.title,
                    "created_at": resume.created_at
                } if resume else None,
                "job_descriptions": [
                    {
                        "id": jd.id,
                        "job_title": jd.job_title,
                        "company": jd.company,
                        "created_at": jd.created_at
                    }
                    for jd in job_descriptions
                ]
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching skill gap analysis: {str(e)}"
            )
    
    def update_analysis(
        self, 
        analysis_id: int, 
        update_data: SkillGapAnalysisUpdateRequest
    ) -> Dict[str, Any]:
        """Update a skill gap analysis."""
        try:
            user_id = self.get_current_user_id()
            
            analysis = self.verify_analysis_ownership(analysis_id, user_id)
            if not analysis:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Skill gap analysis not found"
                )
            
            # Update allowed fields
            update_dict = update_data.dict(exclude_unset=True)
            for field, value in update_dict.items():
                if hasattr(analysis, field):
                    setattr(analysis, field, value)
            
            self.db.commit()
            self.db.refresh(analysis)
            
            return {
                "message": "Skill gap analysis updated successfully",
                "analysis_id": analysis.id
            }
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating skill gap analysis: {str(e)}"
            )
    
    def delete_analysis(self, analysis_id: int) -> Dict[str, Any]:
        """Delete a skill gap analysis."""
        try:
            user_id = self.get_current_user_id()
            
            analysis = self.verify_analysis_ownership(analysis_id, user_id)
            if not analysis:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Skill gap analysis not found"
                )
            
            self.db.delete(analysis)
            self.db.commit()
            
            return {
                "message": "Skill gap analysis deleted successfully"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting skill gap analysis: {str(e)}"
            )


# Create service dependency
def get_skill_gap_service(db: Session = Depends(get_db)) -> SkillGapAnalysisService:
    """Dependency to get skill gap analysis service."""
    return SkillGapAnalysisService(db)


# API endpoints
@router.post("/analyze", response_model=SkillGapAnalysisResponse)
async def analyze_skill_gaps(
    request: SkillGapAnalysisRequest,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Perform skill gap analysis between resume and multiple job descriptions."""
    return service.create_analysis(request)


@router.get("/")
async def get_skill_gap_analyses(
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get all skill gap analyses for the current user."""
    return service.get_analyses()


@router.get("/{analysis_id}")
async def get_skill_gap_analysis(
    analysis_id: int,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get a specific skill gap analysis by ID."""
    return service.get_analysis(analysis_id)


@router.put("/{analysis_id}")
async def update_skill_gap_analysis(
    analysis_id: int,
    update_data: SkillGapAnalysisUpdateRequest,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Update a skill gap analysis."""
    return service.update_analysis(analysis_id, update_data)


@router.delete("/{analysis_id}")
async def delete_skill_gap_analysis(
    analysis_id: int,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Delete a skill gap analysis."""
    return service.delete_analysis(analysis_id)


@router.get("/{analysis_id}/summary", response_model=SkillGapAnalysisSummaryResponse)
async def get_analysis_summary(
    analysis_id: int,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get a summary of the skill gap analysis."""
    try:
        user_id = service.get_current_user_id()
        
        from app.models.skill_gap_analysis import SkillGapAnalysis
        analysis = service.db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        # Update last accessed time
        service.update_last_accessed(analysis)
        
        return SkillGapAnalysisSummaryResponse(
            analysis_name=analysis.analysis_name,
            job_count=len(analysis.job_description_ids),
            skill_coverage_score=analysis.skill_coverage_score,
            analysis_summary=analysis.analysis_summary,
            missing_skills_count=len(analysis.missing_skills.get("gap_summary", {}).get("total_missing_skills", 0)),
            repeated_gaps_count=len(analysis.repeated_gaps.get("high_frequency_gaps", [])),
            critical_gaps_count=len(analysis.repeated_gaps.get("critical_gaps", [])),
            learning_recommendations_count=len(analysis.learning_recommendations or []),
            project_suggestions_count=len(analysis.project_suggestions or []),
            action_items_count=len(analysis.action_items or []),
            created_at=str(analysis.created_at),
            updated_at=str(analysis.updated_at) if analysis.updated_at else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching analysis summary: {str(e)}"
        )


@router.get("/{analysis_id}/missing-skills", response_model=MissingSkillsResponse)
async def get_missing_skills(
    analysis_id: int,
    category: Optional[str] = Query(None, description="Filter by skill category"),
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get missing skills from the analysis."""
    try:
        user_id = service.get_current_user_id()
        
        from app.models.skill_gap_analysis import SkillGapAnalysis
        analysis = service.db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        missing_skills = analysis.missing_skills or {}
        
        if category:
            category_key = f"missing_{category}"
            if category_key in missing_skills:
                return {
                    "missing_skills": {category: missing_skills[category_key]},
                    "total_missing": len(missing_skills[category_key]),
                    "categories": {category: len(missing_skills[category_key])}
                }
            else:
                return {
                    "missing_skills": {category: []},
                    "total_missing": 0,
                    "categories": {category: 0}
                }
        
        return MissingSkillsResponse(
            missing_skills=missing_skills,
            total_missing=missing_skills.get("gap_summary", {}).get("total_missing_skills", 0),
            categories={
                category: len(missing_skills.get(f"missing_{category}", []))
                for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]
                if f"missing_{category}" in missing_skills
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching missing skills: {str(e)}"
        )


@router.get("/{analysis_id}/repeated-gaps", response_model=RepeatedGapsResponse)
async def get_repeated_gaps(
    analysis_id: int,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get repeated skill gaps from the analysis."""
    try:
        user_id = service.get_current_user_id()
        
        from app.models.skill_gap_analysis import SkillGapAnalysis
        analysis = service.db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return RepeatedGapsResponse(
            high_frequency_gaps=analysis.repeated_gaps.get("high_frequency_gaps", []),
            critical_gaps=analysis.repeated_gaps.get("critical_gaps", []),
            category_gaps=analysis.repeated_gaps.get("category_gaps", {}),
            gap_analysis=analysis.repeated_gaps.get("gap_analysis", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching repeated gaps: {str(e)}"
        )


@router.get("/{analysis_id}/learning-recommendations", response_model=LearningRecommendationsResponse)
async def get_learning_recommendations(
    analysis_id: int,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get learning recommendations from the analysis."""
    try:
        user_id = service.get_current_user_id()
        
        from app.models.skill_gap_analysis import SkillGapAnalysis
        analysis = service.db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return LearningRecommendationsResponse(
            learning_recommendations=analysis.learning_recommendations or [],
            total_count=len(analysis.learning_recommendations or [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching learning recommendations: {str(e)}"
        )


@router.get("/{analysis_id}/project-suggestions", response_model=ProjectSuggestionsResponse)
async def get_project_suggestions(
    analysis_id: int,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get project suggestions from the analysis."""
    try:
        user_id = service.get_current_user_id()
        
        from app.models.skill_gap_analysis import SkillGapAnalysis
        analysis = service.db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return ProjectSuggestionsResponse(
            project_suggestions=analysis.project_suggestions or [],
            total_count=len(analysis.project_suggestions or [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching project suggestions: {str(e)}"
        )


@router.get("/{analysis_id}/action-items", response_model=ActionItemsResponse)
async def get_action_items(
    analysis_id: int,
    service: SkillGapAnalysisService = Depends(get_skill_gap_service)
):
    """Get action items from the analysis."""
    try:
        user_id = service.get_current_user_id()
        
        from app.models.skill_gap_analysis import SkillGapAnalysis
        analysis = service.db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return ActionItemsResponse(
            action_items=analysis.action_items or [],
            total_count=len(analysis.action_items or [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching action items: {str(e)}"
        )


@router.get("/analysis-options", response_model=AnalysisOptionsResponse)
async def get_analysis_options():
    """Get available analysis options and configurations."""
    return AnalysisOptionsResponse(
        analysis_options={
            "include_soft_skills": {
                "type": "boolean",
                "default": True,
                "description": "Include soft skills in the analysis"
            },
            "include_technical_skills": {
                "type": "boolean",
                "default": True,
                "description": "Include technical skills in the analysis"
            },
            "min_gap_frequency": {
                "type": "integer",
                "default": 2,
                "min": 1,
                "max": 10,
                "description": "Minimum frequency for a skill to be considered a repeated gap"
            },
            "project_suggestion_count": {
                "type": "integer",
                "default": 5,
                "min": 1,
                "max": 10,
                "description": "Number of project suggestions to generate"
            },
            "learning_recommendation_count": {
                "type": "integer",
                "default": 8,
                "min": 1,
                "max": 15,
                "description": "Number of learning recommendations to generate"
            },
            "priority_threshold": {
                "type": "number",
                "default": 0.3,
                "min": 0.1,
                "max": 1.0,
                "description": "Minimum priority score for recommendations"
            }
        },
        skill_categories=[
            {
                "value": "technical",
                "label": "Technical Skills",
                "description": "Programming languages, frameworks, and technical tools"
            },
            {
                "value": "soft_skills",
                "label": "Soft Skills",
                "description": "Communication, leadership, teamwork, and interpersonal skills"
            },
            {
                "value": "tools",
                "label": "Tools",
                "description": "Development tools, IDEs, and productivity software"
            },
            {
                "value": "languages",
                "label": "Programming Languages",
                "description": "Programming and scripting languages"
            },
            {
                "value": "frameworks",
                "label": "Frameworks",
                "description": "Application frameworks and libraries"
            },
            {
                "value": "databases",
                "label": "Databases",
                "description": "Database systems and data storage"
            },
            {
                "value": "platforms",
                "label": "Platforms",
                "description": "Cloud platforms and deployment environments"
            }
        ]
    )
