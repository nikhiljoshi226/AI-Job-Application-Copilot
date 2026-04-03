from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.models.skill_gap_analysis import SkillGapAnalysis
from app.models.resume import Resume
from app.models.job_description import JobDescription

router = APIRouter()


class SkillGapAnalysisRequest(BaseModel):
    resume_id: int
    job_description_ids: List[int]
    analysis_name: Optional[str] = None
    analysis_options: Optional[Dict[str, Any]] = None


class SkillGapAnalysisResponse(BaseModel):
    success: bool
    analysis_id: Optional[int] = None
    analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    validation_errors: list = []


@router.post("/analyze")
async def analyze_skill_gaps(
    request: SkillGapAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Perform skill gap analysis between resume and multiple job descriptions.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Verify resume exists and belongs to user
        resume = db.query(Resume).filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user_id
        ).first()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        # Verify job descriptions exist and belong to user
        job_descriptions = db.query(JobDescription).filter(
            JobDescription.id.in_(request.job_description_ids),
            JobDescription.user_id == current_user_id
        ).all()
        
        if len(job_descriptions) != len(request.job_description_ids):
            found_ids = [jd.id for jd in job_descriptions]
            missing_ids = set(request.job_description_ids) - set(found_ids)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job descriptions not found: {list(missing_ids)}"
            )
        
        # Prepare data for analysis
        resume_data = {
            "rendering_data": resume.rendering_content
        }
        
        job_descriptions_data = []
        for jd in job_descriptions:
            job_descriptions_data.append({
                "id": jd.id,
                "job_title": jd.job_title,
                "company": jd.company,
                "raw_text": jd.raw_text,
                "parsed_content": jd.parsed_json
            })
        
        # Perform skill gap analysis
        from app.services.skill_gap_analyzer import SkillGapAnalyzer
        analyzer = SkillGapAnalyzer()
        
        result = analyzer.analyze_skill_gaps(
            resume_data,
            job_descriptions_data,
            request.analysis_options
        )
        
        # Create analysis record
        analysis = SkillGapAnalysis(
            user_id=current_user_id,
            resume_id=request.resume_id,
            analysis_name=request.analysis_name or result["skill_gap_analysis"]["analysis_name"],
            job_description_ids=request.job_description_ids,
            analysis_summary=result["skill_gap_analysis"]["analysis_summary"],
            missing_skills=result["skill_gap_analysis"]["missing_skills"],
            repeated_gaps=result["skill_gap_analysis"]["repeated_gaps"],
            role_expectations=result["skill_gap_analysis"]["role_expectations"],
            learning_recommendations=result["skill_gap_analysis"]["learning_recommendations"],
            project_suggestions=result["skill_gap_analysis"]["project_suggestions"],
            skill_coverage_score=result["skill_gap_analysis"]["skill_coverage_score"],
            action_items=result["skill_gap_analysis"]["action_items"],
            metadata=result["metadata"]
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
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


@router.get("/")
async def get_skill_gap_analyses(
    db: Session = Depends(get_db)
):
    """
    Get all skill gap analyses for the current user.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analyses = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.user_id == current_user_id
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


@router.get("/{analysis_id}")
async def get_skill_gap_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific skill gap analysis by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        # Update last accessed time
        from datetime import datetime, timezone
        analysis.last_accessed_at = datetime.now(timezone.utc)
        db.commit()
        
        # Get related information
        resume = db.query(Resume).filter(
            Resume.id == analysis.resume_id
        ).first()
        
        job_descriptions = db.query(JobDescription).filter(
            JobDescription.id.in_(analysis.job_description_ids)
        ).all()
        
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


@router.put("/{analysis_id}")
async def update_skill_gap_analysis(
    analysis_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Update a skill gap analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        # Update allowed fields
        if "analysis_name" in update_data:
            analysis.analysis_name = update_data["analysis_name"]
        
        if "analysis_summary" in update_data:
            analysis.analysis_summary = update_data["analysis_summary"]
        
        if "learning_recommendations" in update_data:
            analysis.learning_recommendations = update_data["learning_recommendations"]
        
        if "project_suggestions" in update_data:
            analysis.project_suggestions = update_data["project_suggestions"]
        
        if "action_items" in update_data:
            analysis.action_items = update_data["action_items"]
        
        if "metadata" in update_data:
            analysis.metadata = update_data["metadata"]
        
        db.commit()
        db.refresh(analysis)
        
        return {
            "message": "Skill gap analysis updated successfully",
            "analysis_id": analysis.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating skill gap analysis: {str(e)}"
        )


@router.delete("/{analysis_id}")
async def delete_skill_gap_analysis(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a skill gap analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        db.delete(analysis)
        db.commit()
        
        return {
            "message": "Skill gap analysis deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting skill gap analysis: {str(e)}"
        )


@router.get("/{analysis_id}/summary")
async def get_analysis_summary(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a summary of the skill gap analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        # Update last accessed time
        from datetime import datetime, timezone
        analysis.last_accessed_at = datetime.now(timezone.utc)
        db.commit()
        
        return {
            "analysis_name": analysis.analysis_name,
            "job_count": len(analysis.job_description_ids),
            "skill_coverage_score": analysis.skill_coverage_score,
            "analysis_summary": analysis.analysis_summary,
            "missing_skills_count": len(analysis.missing_skills.get("gap_summary", {}).get("total_missing_skills", 0)),
            "repeated_gaps_count": len(analysis.repeated_gaps.get("high_frequency_gaps", [])),
            "critical_gaps_count": len(analysis.repeated_gaps.get("critical_gaps", [])),
            "learning_recommendations_count": len(analysis.learning_recommendations or []),
            "project_suggestions_count": len(analysis.project_suggestions or []),
            "action_items_count": len(analysis.action_items or []),
            "created_at": analysis.created_at,
            "updated_at": analysis.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching analysis summary: {str(e)}"
        )


@router.get("/{analysis_id}/missing-skills")
async def get_missing_skills(
    analysis_id: int,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get missing skills from the analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        missing_skills = analysis.missing_skills or {}
        
        # Filter by category if specified
        if category:
            category_key = f"missing_{category}"
            if category_key in missing_skills:
                return {
                    "category": category,
                    "skills": missing_skills[category_key],
                    "total_count": len(missing_skills[category_key])
                }
            else:
                return {
                    "category": category,
                    "skills": [],
                    "total_count": 0
                }
        
        return {
            "missing_skills": missing_skills,
            "total_missing": missing_skills.get("gap_summary", {}).get("total_missing_skills", 0),
            "categories": {
                category: len(missing_skills.get(f"missing_{category}", []))
                for category in ["technical", "soft_skills", "tools", "languages", "frameworks", "databases", "platforms"]
                if f"missing_{category}" in missing_skills
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching missing skills: {str(e)}"
        )


@router.get("/{analysis_id}/repeated-gaps")
async def get_repeated_gaps(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get repeated skill gaps from the analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return {
            "high_frequency_gaps": analysis.repeated_gaps.get("high_frequency_gaps", []),
            "critical_gaps": analysis.repeated_gaps.get("critical_gaps", []),
            "category_gaps": analysis.repeated_gaps.get("category_gaps", {}),
            "gap_analysis": analysis.repeated_gaps.get("gap_analysis", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching repeated gaps: {str(e)}"
        )


@router.get("/{analysis_id}/learning-recommendations")
async def get_learning_recommendations(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get learning recommendations from the analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return {
            "learning_recommendations": analysis.learning_recommendations or [],
            "total_count": len(analysis.learning_recommendations or [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching learning recommendations: {str(e)}"
        )


@router.get("/{analysis_id}/project-suggestions")
async def get_project_suggestions(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get project suggestions from the analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return {
            "project_suggestions": analysis.project_suggestions or [],
            "total_count": len(analysis.project_suggestions or [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching project suggestions: {str(e)}"
        )


@router.get("/{analysis_id}/action-items")
async def get_action_items(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    """
    Get action items from the analysis.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == current_user_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill gap analysis not found"
            )
        
        return {
            "action_items": analysis.action_items or [],
            "total_count": len(analysis.action_items or [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching action items: {str(e)}"
        )


@router.get("/analysis-options")
async def get_analysis_options():
    """
    Get available analysis options and configurations.
    """
    return {
        "analysis_options": {
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
        "skill_categories": [
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
    }
