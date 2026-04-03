from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import time

from app.core.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.tailored_resume import TailoredResume
from app.services.tailoring_suggester import TailoringSuggester
from app.services.tailored_resume_builder import TailoredResumeBuilder


class TailoringRequest(BaseModel):
    resume_id: int
    job_description_id: int


router = APIRouter()


@router.post("/generate-suggestions")
async def generate_tailoring_suggestions(
    request: TailoringRequest,
    db: Session = Depends(get_db)
):
    """
    Generate tailoring suggestions for a resume based on job description.
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
        
        # Check if both have parsed data
        if not resume.parsed_json:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume has not been parsed yet"
            )
        
        if not job_description.parsed_json:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Job description has not been parsed yet"
            )
        
        # Create truth bank for resume
        from app.services.truth_bank import TruthBank
        truth_bank_service = TruthBank()
        truth_bank = truth_bank_service.create_truth_bank(resume.parsed_json)
        
        # Generate tailoring suggestions
        start_time = time.time()
        suggester = TailoringSuggester()
        suggestions = suggester.generate_suggestions(
            resume.parsed_json,
            truth_bank,
            job_description.parsed_json
        )
        processing_time = int((time.time() - start_time) * 1000)
        
        # Update metadata
        suggestions["metadata"]["processing_time_ms"] = processing_time
        
        # Check for guardrail violations
        if suggestions.get("guardrail_violations"):
            # Add warnings for guardrail violations
            suggestions["warnings"] = [
                {
                    "type": "guardrail_violations",
                    "message": f"Found {len(suggestions['guardrail_violations'])} guardrail violations. Please review suggestions carefully.",
                    "violations": suggestions["guardrail_violations"]
                }
            ]
        
        # Check for unsupported requirements
        if suggestions.get("unsupported_requirements"):
            if not suggestions.get("warnings"):
                suggestions["warnings"] = []
            
            suggestions["warnings"].append({
                "type": "unsupported_requirements",
                "message": f"{len(suggestions['unsupported_requirements'])} JD requirements cannot be supported by your resume.",
                "unsupported": suggestions["unsupported_requirements"]
            })
        
        return {
            "message": "Tailoring suggestions generated successfully",
            "suggestions": suggestions,
            "resume_title": resume.title,
            "job_title": job_description.job_title,
            "company": job_description.company,
            "processing_time_ms": processing_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating tailoring suggestions: {str(e)}"
        )


@router.post("/apply-suggestions")
async def apply_tailoring_suggestions(
    request: TailoringRequest,
    suggestions: dict,
    db: Session = Depends(get_db)
):
    """
    Apply tailoring suggestions and create a tailored resume.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Verify resume and job description exist
        resume = db.query(Resume).filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user_id
        ).first()
        
        job_description = db.query(JobDescription).filter(
            JobDescription.id == request.job_description_id,
            JobDescription.user_id == current_user_id
        ).first()
        
        if not resume or not job_description:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume or job description not found"
            )
        
        # Check if tailored resume already exists
        existing_tailored = db.query(TailoredResume).filter(
            TailoredResume.user_id == current_user_id,
            TailoredResume.original_resume_id == request.resume_id,
            TailoredResume.job_description_id == request.job_description_id
        ).first()
        
        if existing_tailored:
            return {
                "message": "Tailored resume already exists",
                "tailored_resume_id": existing_tailored.id
            }
        
        # Build the tailored resume
        builder = TailoredResumeBuilder()
        
        # Filter approved suggestions
        approved_suggestions = {}
        for section, section_suggestions in suggestions.get("suggestions", {}).items():
            approved_suggestions[section] = [
                s for s in section_suggestions if s.get('approved', False)
            ]
        
        # Create truth bank for validation
        from app.services.truth_bank import TruthBank
        truth_bank_service = TruthBank()
        truth_bank = truth_bank_service.create_truth_bank(resume.parsed_json)
        
        # Build the tailored resume
        start_time = time.time()
        tailored_result = builder.build_tailored_resume(
            resume.parsed_json,
            approved_suggestions,
            truth_bank
        )
        
        # Validate the result
        is_valid, validation_errors = builder.validate_tailored_resume(
            tailored_result["tailored_resume"],
            resume.parsed_json
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tailored resume validation failed: {', '.join(validation_errors)}"
            )
        
        # Prepare for rendering
        rendering_data = builder.prepare_for_rendering(tailored_result["tailored_resume"])
        
        # Calculate alignment score
        final_alignment_score = int(tailored_result["metadata"]["truthfulness_score"] * 100)
        
        # Create tailored resume record
        tailored_resume = TailoredResume(
            user_id=current_user_id,
            original_resume_id=request.resume_id,
            job_description_id=request.job_description_id,
            title=f"Tailored: {resume.title} for {job_description.job_title}",
            tailored_content=tailored_result,
            suggestions=suggestions.get("suggestions", {}),
            applied_suggestions=tailored_result["applied_changes"],
            final_alignment_score=final_alignment_score,
            truthfulness_score=tailored_result["metadata"]["truthfulness_score"],
            processing_time_ms=tailored_result["metadata"]["processing_time_ms"],
            status="draft"
        )
        
        db.add(tailored_resume)
        db.commit()
        db.refresh(tailored_resume)
        
        return {
            "message": "Tailored resume created successfully",
            "tailored_resume_id": tailored_resume.id,
            "title": tailored_resume.title,
            "status": tailored_resume.status,
            "metadata": tailored_result["metadata"],
            "change_summary": tailored_result["change_summary"],
            "validation_errors": validation_errors if not is_valid else [],
            "rendering_data": rendering_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error applying tailoring suggestions: {str(e)}"
        )


@router.get("/tailored-resumes")
async def get_tailored_resumes(db: Session = Depends(get_db)):
    """
    Get all tailored resumes for current user.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        tailored_resumes = db.query(TailoredResume).filter(
            TailoredResume.user_id == current_user_id
        ).order_by(TailoredResume.created_at.desc()).all()
        
        return {
            "tailored_resumes": [
                {
                    "id": tr.id,
                    "title": tr.title,
                    "original_resume_id": tr.original_resume_id,
                    "job_description_id": tr.job_description_id,
                    "final_alignment_score": tr.final_alignment_score,
                    "truthfulness_score": tr.truthfulness_score,
                    "status": tr.status,
                    "created_at": tr.created_at,
                    "processing_time_ms": tr.processing_time_ms
                }
                for tr in tailored_resumes
            ],
            "total": len(tailored_resumes)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tailored resumes: {str(e)}"
        )


@router.get("/tailored-resumes/{tailored_id}")
async def get_tailored_resume(
    tailored_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific tailored resume by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Get related resume and job description info
        resume = db.query(Resume).filter(Resume.id == tailored_resume.original_resume_id).first()
        job_description = db.query(JobDescription).filter(JobDescription.id == tailored_resume.job_description_id).first()
        
        return {
            "id": tailored_resume.id,
            "title": tailored_resume.title,
            "original_resume": {
                "id": resume.id,
                "title": resume.title
            } if resume else None,
            "job_description": {
                "id": job_description.id,
                "job_title": job_description.job_title,
                "company": job_description.company
            } if job_description else None,
            "tailored_content": tailored_resume.tailored_content,
            "suggestions": tailored_resume.suggestions,
            "final_alignment_score": tailored_resume.final_alignment_score,
            "truthfulness_score": tailored_resume.truthfulness_score,
            "status": tailored_resume.status,
            "created_at": tailored_resume.created_at,
            "updated_at": tailored_resume.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tailored resume: {str(e)}"
        )


@router.put("/tailored-resumes/{tailored_id}")
async def update_tailored_resume(
    tailored_id: int,
    updates: dict,
    db: Session = Depends(get_db)
):
    """
    Update a tailored resume.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Update allowed fields
        if "title" in updates:
            tailored_resume.title = updates["title"]
        
        if "tailored_content" in updates:
            tailored_resume.tailored_content = updates["tailored_content"]
        
        if "suggestions" in updates:
            tailored_resume.suggestions = updates["suggestions"]
        
        if "status" in updates:
            tailored_resume.status = updates["status"]
        
        if "applied_suggestions" in updates:
            tailored_resume.applied_suggestions = updates["applied_suggestions"]
        
        db.commit()
        db.refresh(tailored_resume)
        
        return {
            "message": "Tailored resume updated successfully",
            "tailored_resume_id": tailored_resume.id,
            "status": tailored_resume.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating tailored resume: {str(e)}"
        )


@router.delete("/tailored-resumes/{tailored_id}")
async def delete_tailored_resume(
    tailored_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a tailored resume.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        db.delete(tailored_resume)
        db.commit()
        
        return {
            "message": "Tailored resume deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting tailored resume: {str(e)}"
        )
