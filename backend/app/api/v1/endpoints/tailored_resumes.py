from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.user import User
from app.models.tailored_resume import TailoredResume
from app.services.tailored_resume_builder import TailoredResumeBuilder

router = APIRouter()


@router.get("/{tailored_id}/rendering-data")
async def get_tailored_resume_rendering_data(
    tailored_id: int,
    db: Session = Depends(get_db)
):
    """
    Get tailored resume data formatted for document rendering.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Get tailored resume
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Prepare for rendering
        builder = TailoredResumeBuilder()
        rendering_data = builder.prepare_for_rendering(tailored_resume.tailored_content["tailored_resume"])
        
        return {
            "tailored_resume_id": tailored_id,
            "title": tailored_resume.title,
            "rendering_data": rendering_data,
            "metadata": {
                "final_alignment_score": tailored_resume.final_alignment_score,
                "truthfulness_score": tailored_resume.truthfulness_score,
                "processing_time_ms": tailored_resume.processing_time_ms,
                "total_changes_applied": len(tailored_resume.applied_suggestions) if tailored_resume.applied_suggestions else 0,
                "created_at": tailored_resume.created_at,
                "updated_at": tailored_resume.updated_at,
                "status": tailored_resume.status
            },
            "change_summary": tailored_resume.tailored_content.get("change_summary", {}),
            "applied_changes": tailored_resume.applied_suggestions or []
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting rendering data: {str(e)}"
        )


@router.get("/{tailored_id}/diff-comparison")
async def get_tailored_resume_diff_comparison(
    tailored_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed comparison between original and tailored resume.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Get tailored resume with relationships
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Get original resume
        original_resume = tailored_resume.original_resume
        
        # Build comparison data
        comparison = {
            "tailored_resume_id": tailored_id,
            "title": tailored_resume.title,
            "original_resume": {
                "id": original_resume.id,
                "title": original_resume.title,
                "content": original_resume.parsed_json
            },
            "tailored_content": tailored_resume.tailored_content["tailored_resume"],
            "applied_changes": tailored_resume.applied_suggestions or [],
            "change_summary": tailored_resume.tailored_content.get("change_summary", {}),
            "metadata": {
                "final_alignment_score": tailored_resume.final_alignment_score,
                "truthfulness_score": tailored_resume.truthfulness_score,
                "total_changes_applied": len(tailored_resume.applied_suggestions) if tailored_resume.applied_suggestions else 0,
                "processing_time_ms": tailored_resume.processing_time_ms
            }
        }
        
        return comparison
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting diff comparison: {str(e)}"
        )


@router.put("/{tailored_id}/status")
async def update_tailored_resume_status(
    tailored_id: int,
    status_update: dict,
    db: Session = Depends(get_db)
):
    """
    Update the status of a tailored resume.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Validate status
        new_status = status_update.get("status")
        valid_statuses = ["draft", "approved", "archived"]
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # Get and update tailored resume
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Update status
        tailored_resume.status = new_status
        db.commit()
        db.refresh(tailored_resume)
        
        return {
            "message": f"Tailored resume status updated to {new_status}",
            "tailored_resume_id": tailored_id,
            "status": new_status,
            "updated_at": tailored_resume.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating status: {str(e)}"
        )


@router.get("/{tailored_id}/audit-trail")
async def get_tailored_resume_audit_trail(
    tailored_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the complete audit trail of changes made to create the tailored resume.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Get tailored resume
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Build audit trail
        audit_trail = {
            "tailored_resume_id": tailored_id,
            "title": tailored_resume.title,
            "created_at": tailored_resume.created_at,
            "updated_at": tailored_resume.updated_at,
            "metadata": {
                "final_alignment_score": tailored_resume.final_alignment_score,
                "truthfulness_score": tailored_resume.truthfulness_score,
                "processing_time_ms": tailored_resume.processing_time_ms,
                "version": tailored_resume.version
            },
            "change_summary": tailored_resume.tailored_content.get("change_summary", {}),
            "applied_changes": tailored_resume.applied_suggestions or [],
            "original_suggestions": tailored_resume.suggestions or {},
            "validation_status": "validated" if tailored_resume.truthfulness_score >= 0.7 else "low_confidence"
        }
        
        return audit_trail
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting audit trail: {str(e)}"
        )


@router.post("/{tailored_id}/duplicate")
async def duplicate_tailored_resume(
    tailored_id: int,
    duplication_request: dict,
    db: Session = Depends(get_db)
):
    """
    Create a new version of the tailored resume (for further editing).
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Get original tailored resume
        original_tailored = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not original_tailored:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Create new version
        new_title = duplication_request.get("title", f"{original_tailored.title} (Copy)")
        new_version = (original_tailored.version or 1) + 1
        
        new_tailored = TailoredResume(
            user_id=current_user_id,
            original_resume_id=original_tailored.original_resume_id,
            job_description_id=original_tailored.job_description_id,
            title=new_title,
            tailored_content=original_tailored.tailored_content,
            suggestions=original_tailored.suggestions,
            applied_suggestions=original_tailored.applied_suggestions,
            final_alignment_score=original_tailored.final_alignment_score,
            truthfulness_score=original_tailored.truthfulness_score,
            processing_time_ms=original_tailored.processing_time_ms,
            version=new_version,
            status="draft"
        )
        
        db.add(new_tailored)
        db.commit()
        db.refresh(new_tailored)
        
        return {
            "message": "Tailored resume duplicated successfully",
            "original_id": tailored_id,
            "new_tailored_resume_id": new_tailored.id,
            "new_title": new_title,
            "new_version": new_version,
            "status": new_tailored.status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error duplicating tailored resume: {str(e)}"
        )
