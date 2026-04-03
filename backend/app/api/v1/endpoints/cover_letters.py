from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.models.cover_letter import CoverLetter
from app.models.tailored_resume import TailoredResume
from app.models.job_description import JobDescription
from app.models.application import Application
from app.services.cover_letter_generator import CoverLetterGenerator

router = APIRouter()


class CoverLetterRequest(BaseModel):
    tailored_resume_id: int
    job_description_id: int
    application_id: Optional[int] = None
    generation_options: Optional[Dict[str, Any]] = None


class CoverLetterResponse(BaseModel):
    success: bool
    cover_letter_id: Optional[int] = None
    cover_letter: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    validation_errors: list = []


@router.post("/generate")
async def generate_cover_letter(
    request: CoverLetterRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a cover letter based on tailored resume and job description.
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
        
        # Generate cover letter
        generator = CoverLetterGenerator()
        
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
        
        # Generate cover letter
        result = generator.generate_cover_letter(
            tailored_resume_data,
            job_description_data,
            request.generation_options
        )
        
        # Check for validation errors
        if not result["validation"]["is_valid"]:
            return CoverLetterResponse(
                success=False,
                error="Cover letter validation failed",
                validation_errors=result["validation"]["errors"] + result["validation"]["warnings"]
            )
        
        # Create cover letter record
        cover_letter = CoverLetter(
            user_id=current_user_id,
            application_id=request.application_id,
            job_description_id=request.job_description_id,
            title=f"Cover Letter for {job_description.job_title} at {job_description.company}",
            content=result["cover_letter"],
            raw_text=result["cover_letter"]["full_text"],
            generation_options=request.generation_options or {},
            truthfulness_score=result["metadata"]["truthfulness_score"],
            grammar_score=result["metadata"]["grammar_score"],
            personalization_score=result["metadata"]["personalization_score"],
            processing_time_ms=result["metadata"]["processing_time_ms"],
            status="draft"
        )
        
        db.add(cover_letter)
        db.commit()
        db.refresh(cover_letter)
        
        return CoverLetterResponse(
            success=True,
            cover_letter_id=cover_letter.id,
            cover_letter=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating cover letter: {str(e)}"
        )


@router.get("/")
async def get_cover_letters(
    db: Session = Depends(get_db)
):
    """
    Get all cover letters for the current user.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        cover_letters = db.query(CoverLetter).filter(
            CoverLetter.user_id == current_user_id
        ).order_by(CoverLetter.created_at.desc()).all()
        
        return {
            "cover_letters": [
                {
                    "id": cl.id,
                    "title": cl.title,
                    "application_id": cl.application_id,
                    "job_description_id": cl.job_description_id,
                    "status": cl.status,
                    "truthfulness_score": cl.truthfulness_score,
                    "grammar_score": cl.grammar_score,
                    "personalization_score": cl.personalization_score,
                    "word_count": cl.content.get("metadata", {}).get("word_count", 0) if cl.content else 0,
                    "created_at": cl.created_at,
                    "updated_at": cl.updated_at
                }
                for cl in cover_letters
            ],
            "total": len(cover_letters)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cover letters: {str(e)}"
        )


@router.get("/{cover_letter_id}")
async def get_cover_letter(
    cover_letter_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific cover letter by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        cover_letter = db.query(CoverLetter).filter(
            CoverLetter.id == cover_letter_id,
            CoverLetter.user_id == current_user_id
        ).first()
        
        if not cover_letter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover letter not found"
            )
        
        # Get related information
        job_description = db.query(JobDescription).filter(
            JobDescription.id == cover_letter.job_description_id
        ).first()
        
        application = None
        if cover_letter.application_id:
            application = db.query(Application).filter(
                Application.id == cover_letter.application_id
            ).first()
        
        return {
            "id": cover_letter.id,
            "title": cover_letter.title,
            "content": cover_letter.content,
            "raw_text": cover_letter.raw_text,
            "generation_options": cover_letter.generation_options,
            "scores": {
                "truthfulness_score": cover_letter.truthfulness_score,
                "grammar_score": cover_letter.grammar_score,
                "personalization_score": cover_letter.personalization_score
            },
            "metadata": {
                "processing_time_ms": cover_letter.processing_time_ms,
                "word_count": cover_letter.content.get("metadata", {}).get("word_count", 0) if cover_letter.content else 0,
                "paragraph_count": cover_letter.content.get("metadata", {}).get("paragraph_count", 0) if cover_letter.content else 0,
                "tone": cover_letter.content.get("metadata", {}).get("tone", "professional") if cover_letter.content else "professional"
            },
            "validation": {
                "is_valid": True,  # Would be stored separately if needed
                "warnings": [],
                "errors": []
            },
            "status": cover_letter.status,
            "created_at": cover_letter.created_at,
            "updated_at": cover_letter.updated_at,
            "job_description": {
                "id": job_description.id,
                "job_title": job_description.job_title,
                "company": job_description.company
            } if job_description else None,
            "application": {
                "id": application.id,
                "status": application.status
            } if application else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cover letter: {str(e)}"
        )


@router.put("/{cover_letter_id}")
async def update_cover_letter(
    cover_letter_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Update a cover letter.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        cover_letter = db.query(CoverLetter).filter(
            CoverLetter.id == cover_letter_id,
            CoverLetter.user_id == current_user_id
        ).first()
        
        if not cover_letter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover letter not found"
            )
        
        # Update allowed fields
        if "title" in update_data:
            cover_letter.title = update_data["title"]
        
        if "content" in update_data:
            cover_letter.content = update_data["content"]
            cover_letter.raw_text = update_data["content"].get("full_text", "")
        
        if "status" in update_data:
            valid_statuses = ["draft", "approved", "sent", "archived"]
            if update_data["status"] not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                )
            cover_letter.status = update_data["status"]
        
        if "generation_options" in update_data:
            cover_letter.generation_options = update_data["generation_options"]
        
        db.commit()
        db.refresh(cover_letter)
        
        return {
            "message": "Cover letter updated successfully",
            "cover_letter_id": cover_letter.id,
            "status": cover_letter.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating cover letter: {str(e)}"
        )


@router.delete("/{cover_letter_id}")
async def delete_cover_letter(
    cover_letter_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a cover letter.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        cover_letter = db.query(CoverLetter).filter(
            CoverLetter.id == cover_letter_id,
            CoverLetter.user_id == current_user_id
        ).first()
        
        if not cover_letter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover letter not found"
            )
        
        db.delete(cover_letter)
        db.commit()
        
        return {
            "message": "Cover letter deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting cover letter: {str(e)}"
        )


@router.post("/{cover_letter_id}/regenerate")
async def regenerate_cover_letter(
    cover_letter_id: int,
    regeneration_options: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """
    Regenerate a cover letter with new options.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        cover_letter = db.query(CoverLetter).filter(
            CoverLetter.id == cover_letter_id,
            CoverLetter.user_id == current_user_id
        ).first()
        
        if not cover_letter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover letter not found"
            )
        
        # Get related data
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == cover_letter.application_id if cover_letter.application_id else None,
            TailoredResume.user_id == current_user_id
        ).first()
        
        job_description = db.query(JobDescription).filter(
            JobDescription.id == cover_letter.job_description_id
        ).first()
        
        if not tailored_resume or not job_description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Required data not found for regeneration"
            )
        
        # Regenerate cover letter
        generator = CoverLetterGenerator()
        
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
        
        # Generate new cover letter
        result = generator.generate_cover_letter(
            tailored_resume_data,
            job_description_data,
            regeneration_options
        )
        
        # Check for validation errors
        if not result["validation"]["is_valid"]:
            return {
                "success": False,
                "error": "Cover letter validation failed",
                "validation_errors": result["validation"]["errors"] + result["validation"]["warnings"]
            }
        
        # Update cover letter
        cover_letter.content = result["cover_letter"]
        cover_letter.raw_text = result["cover_letter"]["full_text"]
        cover_letter.generation_options = regeneration_options or {}
        cover_letter.truthfulness_score = result["metadata"]["truthfulness_score"]
        cover_letter.grammar_score = result["metadata"]["grammar_score"]
        cover_letter.personalization_score = result["metadata"]["personalization_score"]
        cover_letter.processing_time_ms = result["metadata"]["processing_time_ms"]
        
        db.commit()
        db.refresh(cover_letter)
        
        return {
            "success": True,
            "cover_letter_id": cover_letter.id,
            "cover_letter": result,
            "message": "Cover letter regenerated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error regenerating cover letter: {str(e)}"
        )


@router.get("/{cover_letter_id}/preview")
async def get_cover_letter_preview(
    cover_letter_id: int,
    format_type: str = "text",
    db: Session = Depends(get_db)
):
    """
    Get a formatted preview of the cover letter.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        cover_letter = db.query(CoverLetter).filter(
            CoverLetter.id == cover_letter_id,
            CoverLetter.user_id == current_user_id
        ).first()
        
        if not cover_letter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover letter not found"
            )
        
        if format_type == "text":
            return {
                "format": "text",
                "content": cover_letter.raw_text,
                "metadata": {
                    "word_count": len(cover_letter.raw_text.split()),
                    "paragraph_count": len([p for p in cover_letter.raw_text.split('\n\n') if p.strip()]),
                    "character_count": len(cover_letter.raw_text)
                }
            }
        
        elif format_type == "structured":
            return {
                "format": "structured",
                "content": cover_letter.content,
                "metadata": {
                    "truthfulness_score": cover_letter.truthfulness_score,
                    "grammar_score": cover_letter.grammar_score,
                    "personalization_score": cover_letter.personalization_score
                }
            }
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid format type. Must be 'text' or 'structured'"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting cover letter preview: {str(e)}"
        )
