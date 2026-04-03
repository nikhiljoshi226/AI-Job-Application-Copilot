from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.models.outreach_draft import OutreachDraft
from app.models.resume import Resume
from app.models.job_description import JobDescription

router = APIRouter()


class OutreachDraftRequest(BaseModel):
    resume_id: int
    job_description_id: int
    outreach_type: str = "email_intro"
    generation_options: Optional[Dict[str, Any]] = None


class OutreachDraftResponse(BaseModel):
    success: bool
    outreach_draft_id: Optional[int] = None
    draft: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    validation_errors: list = []


@router.post("/generate")
async def generate_outreach_draft(
    request: OutreachDraftRequest,
    db: Session = Depends(get_db)
):
    """
    Generate an outreach draft based on resume and job description.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Validate outreach type
        valid_types = ["email_intro", "linkedin_note", "formal_message"]
        if request.outreach_type not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid outreach_type. Must be one of: {', '.join(valid_types)}"
            )
        
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
        
        # Generate outreach draft
        from app.services.outreach_draft_generator import OutreachDraftGenerator
        generator = OutreachDraftGenerator()
        
        # Prepare data for generation
        resume_data = resume.parsed_json or {}
        job_description_data = {
            "job_title": job_description.job_title,
            "company": job_description.company,
            "raw_text": job_description.raw_text,
            "parsed_content": job_description.parsed_json
        }
        
        # Generate draft
        result = generator.generate_outreach_draft(
            resume_data,
            job_description_data,
            request.outreach_type,
            request.generation_options
        )
        
        # Check for validation errors
        if not result["validation"]["is_valid"]:
            return OutreachDraftResponse(
                success=False,
                error="Outreach draft validation failed",
                validation_errors=result["validation"]["errors"] + result["validation"]["warnings"]
            )
        
        # Create outreach draft record
        outreach_draft = OutreachDraft(
            user_id=current_user_id,
            resume_id=request.resume_id,
            job_description_id=request.job_description_id,
            title=f"{request.outreach_type.replace('_', ' ').title()} for {job_description.job_title}",
            draft_type=request.outreach_type,
            content=result["draft"],
            raw_text=result["draft"]["full_text"],
            generation_options=request.generation_options or {},
            truthfulness_score=result["metadata"]["truthfulness_score"],
            conciseness_score=result["metadata"]["conciseness_score"],
            professionalism_score=result["metadata"]["professionalism_score"],
            processing_time_ms=result["metadata"]["processing_time_ms"],
            status="draft"
        )
        
        db.add(outreach_draft)
        db.commit()
        db.refresh(outreach_draft)
        
        return OutreachDraftResponse(
            success=True,
            outreach_draft_id=outreach_draft.id,
            draft=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating outreach draft: {str(e)}"
        )


@router.get("/")
async def get_outreach_drafts(
    db: Session = Depends(get_db)
):
    """
    Get all outreach drafts for the current user.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        outreach_drafts = db.query(OutreachDraft).filter(
            OutreachDraft.user_id == current_user_id
        ).order_by(OutreachDraft.created_at.desc()).all()
        
        return {
            "outreach_drafts": [
                {
                    "id": od.id,
                    "title": od.title,
                    "draft_type": od.draft_type,
                    "resume_id": od.resume_id,
                    "job_description_id": od.job_description_id,
                    "status": od.status,
                    "truthfulness_score": od.truthfulness_score,
                    "conciseness_score": od.conciseness_score,
                    "professionalism_score": od.professionalism_score,
                    "word_count": od.content.get("metadata", {}).get("word_count", 0) if od.content else 0,
                    "created_at": od.created_at,
                    "updated_at": od.updated_at
                }
                for od in outreach_drafts
            ],
            "total": len(outreach_drafts)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching outreach drafts: {str(e)}"
        )


@router.get("/{outreach_draft_id}")
async def get_outreach_draft(
    outreach_draft_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific outreach draft by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        outreach_draft = db.query(OutreachDraft).filter(
            OutreachDraft.id == outreach_draft_id,
            OutreachDraft.user_id == current_user_id
        ).first()
        
        if not outreach_draft:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outreach draft not found"
            )
        
        # Get related information
        resume = db.query(Resume).filter(
            Resume.id == outreach_draft.resume_id
        ).first()
        
        job_description = db.query(JobDescription).filter(
            JobDescription.id == outreach_draft.job_description_id
        ).first()
        
        return {
            "id": outreach_draft.id,
            "title": outreach_draft.title,
            "draft_type": outreach_draft.draft_type,
            "content": outreach_draft.content,
            "raw_text": outreach_draft.raw_text,
            "generation_options": outreach_draft.generation_options,
            "scores": {
                "truthfulness_score": outreach_draft.truthfulness_score,
                "conciseness_score": outreach_draft.conciseness_score,
                "professionalism_score": outreach_draft.professionalism_score
            },
            "metadata": {
                "processing_time_ms": outreach_draft.processing_time_ms,
                "word_count": outreach_draft.content.get("metadata", {}).get("word_count", 0) if outreach_draft.content else 0,
                "paragraph_count": outreach_draft.content.get("metadata", {}).get("paragraph_count", 0) if outreach_draft.content else 0,
                "tone": outreach_draft.content.get("metadata", {}).get("tone", "professional") if outreach_draft.content else "professional"
            },
            "validation": {
                "is_valid": True,  # Would be stored separately if needed
                "warnings": [],
                "errors": []
            },
            "status": outreach_draft.status,
            "created_at": outreach_draft.created_at,
            "updated_at": outreach_draft.updated_at,
            "resume": {
                "id": resume.id,
                "title": resume.title
            } if resume else None,
            "job_description": {
                "id": job_description.id,
                "job_title": job_description.job_title,
                "company": job_description.company
            } if job_description else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching outreach draft: {str(e)}"
        )


@router.put("/{outreach_draft_id}")
async def update_outreach_draft(
    outreach_draft_id: int,
    update_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Update an outreach draft.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        outreach_draft = db.query(OutreachDraft).filter(
            OutreachDraft.id == outreach_draft_id,
            OutreachDraft.user_id == current_user_id
        ).first()
        
        if not outreach_draft:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outreach draft not found"
            )
        
        # Update allowed fields
        if "title" in update_data:
            outreach_draft.title = update_data["title"]
        
        if "content" in update_data:
            outreach_draft.content = update_data["content"]
            outreach_draft.raw_text = update_data["content"].get("full_text", "")
        
        if "status" in update_data:
            valid_statuses = ["draft", "approved", "sent", "archived"]
            if update_data["status"] not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                )
            outreach_draft.status = update_data["status"]
        
        if "generation_options" in update_data:
            outreach_draft.generation_options = update_data["generation_options"]
        
        db.commit()
        db.refresh(outreach_draft)
        
        return {
            "message": "Outreach draft updated successfully",
            "outreach_draft_id": outreach_draft.id,
            "status": outreach_draft.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating outreach draft: {str(e)}"
        )


@router.delete("/{outreach_draft_id}")
async def delete_outreach_draft(
    outreach_draft_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an outreach draft.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        outreach_draft = db.query(OutreachDraft).filter(
            OutreachDraft.id == outreach_draft_id,
            OutreachDraft.user_id == current_user_id
        ).first()
        
        if not outreach_draft:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outreach draft not found"
            )
        
        db.delete(outreach_draft)
        db.commit()
        
        return {
            "message": "Outreach draft deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting outreach draft: {str(e)}"
        )


@router.post("/{outreach_draft_id}/regenerate")
async def regenerate_outreach_draft(
    outreach_draft_id: int,
    regeneration_options: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
):
    """
    Regenerate an outreach draft with new options.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        outreach_draft = db.query(OutreachDraft).filter(
            OutreachDraft.id == outreach_draft_id,
            OutreachDraft.user_id == current_user_id
        ).first()
        
        if not outreach_draft:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outreach draft not found"
            )
        
        # Get related data
        resume = db.query(Resume).filter(
            Resume.id == outreach_draft.resume_id
        ).first()
        
        job_description = db.query(JobDescription).filter(
            JobDescription.id == outreach_draft.job_description_id
        ).first()
        
        if not resume or not job_description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Required data not found for regeneration"
            )
        
        # Regenerate draft
        from app.services.outreach_draft_generator import OutreachDraftGenerator
        generator = OutreachDraftGenerator()
        
        # Prepare data for generation
        resume_data = resume.parsed_json or {}
        job_description_data = {
            "job_title": job_description.job_title,
            "company": job_description.company,
            "raw_text": job_description.raw_text,
            "parsed_content": job_description.parsed_json
        }
        
        # Generate new draft
        result = generator.generate_outreach_draft(
            resume_data,
            job_description_data,
            outreach_draft.draft_type,
            regeneration_options
        )
        
        # Check for validation errors
        if not result["validation"]["is_valid"]:
            return {
                "success": False,
                "error": "Outreach draft validation failed",
                "validation_errors": result["validation"]["errors"] + result["validation"]["warnings"]
            }
        
        # Update outreach draft
        outreach_draft.content = result["draft"]
        outreach_draft.raw_text = result["draft"]["full_text"]
        outreach_draft.generation_options = regeneration_options or {}
        outreach_draft.truthfulness_score = result["metadata"]["truthfulness_score"]
        outreach_draft.conciseness_score = result["metadata"]["conciseness_score"]
        outreach_draft.professionalism_score = result["metadata"]["professionalism_score"]
        outreach_draft.processing_time_ms = result["metadata"]["processing_time_ms"]
        
        db.commit()
        db.refresh(outreach_draft)
        
        return {
            "success": True,
            "outreach_draft_id": outreach_draft.id,
            "draft": result,
            "message": "Outreach draft regenerated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error regenerating outreach draft: {str(e)}"
        )


@router.get("/{outreach_draft_id}/preview")
async def get_outreach_draft_preview(
    outreach_draft_id: int,
    format_type: str = "text",
    db: Session = Depends(get_db)
):
    """
    Get a formatted preview of the outreach draft.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        outreach_draft = db.query(OutreachDraft).filter(
            OutreachDraft.id == outreach_draft_id,
            OutreachDraft.user_id == current_user_id
        ).first()
        
        if not outreach_draft:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Outreach draft not found"
            )
        
        if format_type == "text":
            return {
                "format": "text",
                "content": outreach_draft.raw_text,
                "metadata": {
                    "word_count": len(outreach_draft.raw_text.split()),
                    "paragraph_count": len([p for p in outreach_draft.raw_text.split('\n\n') if p.strip()]),
                    "character_count": len(outreach_draft.raw_text)
                }
            }
        
        elif format_type == "structured":
            return {
                "format": "structured",
                "content": outreach_draft.content,
                "metadata": {
                    "truthfulness_score": outreach_draft.truthfulness_score,
                    "conciseness_score": outreach_draft.conciseness_score,
                    "professionalism_score": outreach_draft.professionalism_score
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
            detail=f"Error getting outreach draft preview: {str(e)}"
        )


@router.get("/types")
async def get_available_outreach_types():
    """
    Get available outreach types with descriptions.
    """
    try:
        from app.services.outreach_draft_generator import OutreachDraftGenerator
        generator = OutreachDraftGenerator()
        
        return {
            "outreach_types": generator.get_available_outreach_types()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting outreach types: {str(e)}"
        )
