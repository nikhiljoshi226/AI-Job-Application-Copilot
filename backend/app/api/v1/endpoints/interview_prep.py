from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.models.interview_prep import InterviewPrep
from app.models.tailored_resume import TailoredResume
from app.models.job_description import JobDescription
from app.models.application import Application

router = APIRouter()


class InterviewPrepRequest(BaseModel):
    tailored_resume_id: int
    job_description_id: int
    application_id: Optional[int] = None
    generation_options: Optional[Dict[str, Any]] = None


class InterviewPrepResponse(BaseModel):
    success: bool
    interview_prep_id: Optional[int] = None
    interview_prep: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    validation_errors: list = []


@router.post("/generate")
async def generate_interview_prep(
    request: InterviewPrepRequest,
    db: Session = Depends(get_db)
):
    """
    Generate interview preparation materials.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Verify tailored resume exists and belongs to user
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == request.tailored_resume_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Verify job description exists and belongs to user
        job_description = db.query(JobDescription).filter(
            JobDescription.id == request.job_description_id,
            JobDescription.user_id == current_user_id
        ).first()
        
        if not job_description:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job description not found"
            )
        
        # Verify application if provided
        if request.application_id:
            application = db.query(Application).filter(
                Application.id == request.application_id,
                Application.user_id == current_user_id
            ).first()
            
            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Application not found"
                )
        
        # Generate interview prep
        from app.services.interview_prep_generator import InterviewPrepGenerator
        generator = InterviewPrepGenerator()
        
        # Prepare data for generation
        tailored_resume_data = {
            "rendering_data": tailored_resume.tailored_content.get("tailored_resume", {})
        }
        
        job_description_data = {
            "parsed_content": job_description.parsed_json,
            "raw_text": job_description.raw_text,
            "job_title": job_description.job_title,
            "company": job_description.company
        }
        
        # Generate interview prep
        result = generator.generate_interview_prep(
            tailored_resume_data,
            job_description_data,
            request.generation_options
        )
        
        # Check for validation errors
        if not result["validation"]["is_valid"]:
            return InterviewPrepResponse(
                success=False,
                error="Interview prep validation failed",
                validation_errors=result["validation"]["errors"] + result["validation"]["warnings"]
            )
        
        # Create interview prep record
        interview_prep = InterviewPrep(
            user_id=current_user_id,
            application_id=request.application_id,
            job_description_id=request.job_description_id,
            interview_context=result["interview_prep"]["interview_context"],
            questions=result["interview_prep"]["questions"],
            star_stories=result["interview_prep"]["star_stories"],
            preparation_guide=result["interview_prep"]["preparation_guide"],
            content_summary=result["interview_prep"]["content_summary"],
            metadata=result["metadata"],
            truthfulness_score=result["metadata"]["truthfulness_score"],
            content_quality_score=result["metadata"]["content_quality_score"],
            personalization_score=result["metadata"]["personalization_score"],
            processing_time_ms=result["metadata"]["processing_time_ms"]
        )
        
        db.add(interview_prep)
        db.commit()
        db.refresh(interview_prep)
        
        return InterviewPrepResponse(
            success=True,
            interview_prep_id=interview_prep.id,
            interview_prep=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating interview prep: {str(e)}"
        )


@router.get("/")
async def get_interview_preps(
    db: Session = Depends(get_db)
):
    """
    Get all interview prep materials for the current user.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_preps = db.query(InterviewPrep).filter(
            InterviewPrep.user_id == current_user_id
        ).order_by(InterviewPrep.created_at.desc()).all()
        
        return {
            "interview_preps": [
                {
                    "id": ip.id,
                    "application_id": ip.application_id,
                    "job_description_id": ip.job_description_id,
                    "interview_context": ip.interview_context,
                    "content_summary": ip.content_summary,
                    "truthfulness_score": ip.truthfulness_score,
                    "content_quality_score": ip.content_quality_score,
                    "personalization_score": ip.personalization_score,
                    "created_at": ip.created_at,
                    "updated_at": ip.updated_at,
                    "last_accessed_at": ip.last_accessed_at
                }
                for ip in interview_preps
            ],
            "total": len(interview_preps)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching interview preps: {str(e)}"
        )


@router.get("/{interview_prep_id}")
async def get_interview_prep(
    interview_prep_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific interview prep by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_prep = db.query(InterviewPrep).filter(
            InterviewPrep.id == interview_prep_id,
            InterviewPrep.user_id == current_user_id
        ).first()
        
        if not interview_prep:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview prep not found"
            )
        
        # Update last accessed time
        from datetime import datetime, timezone
        interview_prep.last_accessed_at = datetime.now(timezone.utc)
        db.commit()
        
        # Get related information
        job_description = db.query(JobDescription).filter(
            JobDescription.id == interview_prep.job_description_id
        ).first()
        
        application = None
        if interview_prep.application_id:
            application = db.query(Application).filter(
                Application.id == interview_prep.application_id
            ).first()
        
        return {
            "id": interview_prep.id,
            "application_id": interview_prep.application_id,
            "job_description_id": interview_prep.job_description_id,
            "interview_context": interview_prep.interview_context,
            "questions": interview_prep.questions,
            "star_stories": interview_prep.star_stories,
            "preparation_guide": interview_prep.preparation_guide,
            "content_summary": interview_prep.content_summary,
            "metadata": interview_prep.metadata,
            "scores": {
                "truthfulness_score": interview_prep.truthfulness_score,
                "content_quality_score": interview_prep.content_quality_score,
                "personalization_score": interview_prep.personalization_score
            },
            "created_at": interview_prep.created_at,
            "updated_at": interview_prep.updated_at,
            "last_accessed_at": interview_prep.last_accessed_at,
            "job_description": {
                "id": job_description.id,
                "job_title": job_description.job_title,
                "company": job_description.company
            } if job_description else None,
            "application": {
                "id": application.id,
                "company": application.company,
                "position_title": application.position_title,
                "status": application.status
            } if application else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching interview prep: {str(e)}"
        )


@router.put("/{interview_prep_id}")
async def update_interview_prep(
    interview_prep_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Update an interview prep.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_prep = db.query(InterviewPrep).filter(
            InterviewPrep.id == interview_prep_id,
            InterviewPrep.user_id == current_user_id
        ).first()
        
        if not interview_prep:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview prep not found"
            )
        
        # Update allowed fields
        if "interview_context" in update_data:
            interview_prep.interview_context = update_data["interview_context"]
        
        if "questions" in update_data:
            interview_prep.questions = update_data["questions"]
        
        if "star_stories" in update_data:
            interview_prep.star_stories = update_data["star_stories"]
        
        if "preparation_guide" in update_data:
            interview_prep.preparation_guide = update_data["preparation_guide"]
        
        if "content_summary" in update_data:
            interview_prep.content_summary = update_data["content_summary"]
        
        if "metadata" in update_data:
            interview_prep.metadata = update_data["metadata"]
        
        db.commit()
        db.refresh(interview_prep)
        
        return {
            "message": "Interview prep updated successfully",
            "interview_prep_id": interview_prep.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating interview prep: {str(e)}"
        )


@router.delete("/{interview_prep_id}")
async def delete_interview_prep(
    interview_prep_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an interview prep.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_prep = db.query(InterviewPrep).filter(
            InterviewPrep.id == interview_prep_id,
            InterviewPrep.user_id == current_user_id
        ).first()
        
        if not interview_prep:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview prep not found"
            )
        
        db.delete(interview_prep)
        db.commit()
        
        return {
            "message": "Interview prep deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting interview prep: {str(e)}"
        )


@router.post("/{interview_prep_id}/regenerate")
async def regenerate_interview_prep(
    interview_prep_id: int,
    regeneration_options: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """
    Regenerate interview prep with new options.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_prep = db.query(InterviewPrep).filter(
            InterviewPrep.id == interview_prep_id,
            InterviewPrep.user_id == current_user_id
        ).first()
        
        if not interview_prep:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview prep not found"
            )
        
        # Get related data
        job_description = db.query(JobDescription).filter(
            JobDescription.id == interview_prep.job_description_id
        ).first()
        
        if not job_description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Required data not found for regeneration"
            )
        
        # Regenerate interview prep
        from app.services.interview_prep_generator import InterviewPrepGenerator
        generator = InterviewPrepGenerator()
        
        # Prepare data for generation
        job_description_data = {
            "parsed_content": job_description.parsed_json,
            "raw_text": job_description.raw_text,
            "job_title": job_description.job_title,
            "company": job_description.company
        }
        
        # We need the tailored resume data - for now, use a placeholder
        tailored_resume_data = {
            "rendering_data": {}
        }
        
        # Generate new interview prep
        result = generator.generate_interview_prep(
            tailored_resume_data,
            job_description_data,
            regeneration_options
        )
        
        # Check for validation errors
        if not result["validation"]["is_valid"]:
            return {
                "success": False,
                "error": "Interview prep validation failed",
                "validation_errors": result["validation"]["errors"] + result["validation"]["warnings"]
            }
        
        # Update interview prep
        interview_prep.interview_context = result["interview_prep"]["interview_context"]
        interview_prep.questions = result["interview_prep"]["questions"]
        interview_prep.star_stories = result["interview_prep"]["star_stories"]
        interview_prep.preparation_guide = result["interview_prep"]["preparation_guide"]
        interview_prep.content_summary = result["interview_prep"]["content_summary"]
        interview_prep.metadata = result["metadata"]
        interview_prep.truthfulness_score = result["metadata"]["truthfulness_score"]
        interview_prep.content_quality_score = result["metadata"]["content_quality_score"]
        interview_prep.personalization_score = result["metadata"]["personalization_score"]
        interview_prep.processing_time_ms = result["metadata"]["processing_time_ms"]
        
        db.commit()
        db.refresh(interview_prep)
        
        return {
            "success": True,
            "interview_prep_id": interview_prep.id,
            "interview_prep": result,
            "message": "Interview prep regenerated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error regenerating interview prep: {str(e)}"
        )


@router.get("/{interview_prep_id}/questions")
async def get_interview_questions(
    interview_prep_id: int,
    question_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get interview questions from an interview prep.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_prep = db.query(InterviewPrep).filter(
            InterviewPrep.id == interview_prep_id,
            InterviewPrep.user_id == current_user_id
        ).first()
        
        if not interview_prep:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview prep not found"
            )
        
        questions = interview_prep.questions or []
        
        # Filter by question type if specified
        if question_type:
            questions = [q for q in questions if q.get("type") == question_type]
        
        return {
            "questions": questions,
            "total_count": len(questions),
            "question_types": list(set(q.get("type") for q in interview_prep.questions or []))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting interview questions: {str(e)}"
        )


@router.get("/{interview_prep_id}/star_stories")
async def get_star_stories(
    interview_prep_id: int,
    db: Session = Depends(get_db)
):
    """
    Get STAR stories from an interview prep.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_prep = db.query(InterviewPrep).filter(
            InterviewPrep.id == interview_prep_id,
            InterviewPrep.user_id == current_user_id
        ).first()
        
        if not interview_prep:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview prep not found"
            )
        
        return {
            "star_stories": interview_prep.star_stories or [],
            "total_count": len(interview_prep.star_stories or [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting STAR stories: {str(e)}"
        )


@router.get("/{interview_prep_id}/preparation_guide")
async def get_preparation_guide(
    interview_prep_id: int,
    db: Session = Depends(get_db)
):
    """
    Get preparation guide from an interview prep.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        interview_prep = db.query(InterviewPrep).filter(
            InterviewPrep.id == interview_prep_id,
            InterviewPrep.user_id == current_user_id
        ).first()
        
        if not interview_prep:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview prep not found"
            )
        
        return {
            "preparation_guide": interview_prep.preparation_guide or {}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting preparation guide: {str(e)}"
        )


@router.get("/types")
async def get_interview_types():
    """
    Get available interview types and options.
    """
    return {
        "interview_types": [
            {
                "value": "behavioral",
                "label": "Behavioral",
                "description": "Questions about past experiences and behaviors"
            },
            {
                "value": "technical",
                "label": "Technical",
                "description": "Questions about technical skills and knowledge"
            },
            {
                "value": "situational",
                "label": "Situational",
                "description": "Hypothetical scenarios and how you would handle them"
            },
            {
                "value": "mixed",
                "label": "Mixed",
                "description": "Combination of all interview types"
            }
        ],
        "difficulty_levels": [
            {
                "value": "easy",
                "label": "Easy",
                "description": "Basic questions for entry-level positions"
            },
            {
                "value": "medium",
                "label": "Medium",
                "description": "Standard questions for most positions"
            },
            {
                "value": "hard",
                "label": "Hard",
                "description": "Challenging questions for senior positions"
            }
        ],
        "generation_options": {
            "interview_type": {
                "type": "string",
                "default": "mixed",
                "description": "Type of interview to prepare for"
            },
            "question_count": {
                "type": "integer",
                "default": 15,
                "min": 5,
                "max": 30,
                "description": "Number of questions to generate"
            },
            "include_behavioral": {
                "type": "boolean",
                "default": True,
                "description": "Include behavioral questions"
            },
            "include_technical": {
                "type": "boolean",
                "default": True,
                "description": "Include technical questions"
            },
            "include_situational": {
                "type": "boolean",
                "default": True,
                "description": "Include situational questions"
            },
            "star_story_count": {
                "type": "integer",
                "default": 8,
                "min": 3,
                "max": 15,
                "description": "Number of STAR stories to generate"
            },
            "difficulty_level": {
                "type": "string",
                "default": "medium",
                "description": "Difficulty level of questions"
            }
        }
    }
