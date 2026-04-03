import os
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.models.tailored_resume import TailoredResume
from app.services.docx_exporter import DocxExporter
from app.core.config import settings

router = APIRouter()


class ExportRequest(BaseModel):
    tailored_resume_id: int
    template: str = "professional"
    filename: Optional[str] = None


class ExportResponse(BaseModel):
    success: bool
    file_metadata: Optional[Dict[str, Any]]
    error: Optional[str] = None
    validation_errors: list = []


@router.post("/docx/export", response_model=ExportResponse)
async def export_tailored_resume_to_docx(
    request: ExportRequest,
    db: Session = Depends(get_db)
):
    """
    Export a tailored resume to DOCX format.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Get tailored resume
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == request.tailored_resume_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Validate template
        valid_templates = ["professional", "modern", "technical", "creative"]
        if request.template not in valid_templates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid template. Must be one of: {', '.join(valid_templates)}"
            )
        
        # Export to DOCX
        exporter = DocxExporter()
        
        # Validate export data
        is_valid, validation_errors = exporter.validate_export_data(tailored_resume.tailored_content)
        if not is_valid:
            return ExportResponse(
                success=False,
                file_metadata=None,
                error="Validation failed",
                validation_errors=validation_errors
            )
        
        # Perform export
        export_result = exporter.export_tailored_resume_to_docx(
            tailored_resume.tailored_content,
            request.template,
            request.filename
        )
        
        if not export_result["success"]:
            return ExportResponse(
                success=False,
                file_metadata=None,
                error=export_result.get("error", "Export failed"),
                validation_errors=export_result.get("validation_errors", [])
            )
        
        # Store file metadata in database (optional - could add a separate table for exports)
        file_metadata = export_result["file_metadata"]
        
        return ExportResponse(
            success=True,
            file_metadata=file_metadata,
            validation_errors=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting to DOCX: {str(e)}"
        )


@router.get("/docx/download/{filename}")
async def download_docx_file(
    filename: str,
    db: Session = Depends(get_db)
):
    """
    Download a DOCX export file.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Validate filename
        if not filename.endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type"
            )
        
        # Construct file path
        exporter = DocxExporter()
        file_path = exporter.export_dir / filename
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Export file not found"
            )
        
        # TODO: Add user authorization check here
        # For now, we'll allow any authenticated user to download
        
        # Return file
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading file: {str(e)}"
        )


@router.get("/docx/statistics/{filename}")
async def get_docx_file_statistics(
    filename: str,
    db: Session = Depends(get_db)
):
    """
    Get statistics about a DOCX export file.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Validate filename
        if not filename.endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type"
            )
        
        # Get file statistics
        exporter = DocxExporter()
        file_path = exporter.export_dir / filename
        
        statistics = exporter.get_export_statistics(str(file_path))
        
        if "error" in statistics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=statistics["error"]
            )
        
        return {
            "filename": filename,
            "statistics": statistics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting file statistics: {str(e)}"
        )


@router.get("/docx/exports/{tailored_resume_id}")
async def get_resume_exports(
    tailored_resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all DOCX exports for a specific tailored resume.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Verify tailored resume exists and belongs to user
        tailored_resume = db.query(TailoredResume).filter(
            TailoredResume.id == tailored_resume_id,
            TailoredResume.user_id == current_user_id
        ).first()
        
        if not tailored_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tailored resume not found"
            )
        
        # Get export files for this resume
        exporter = DocxExporter()
        export_files = []
        
        # Scan export directory for files related to this resume
        if exporter.export_dir.exists():
            for file_path in exporter.export_dir.glob("*.docx"):
                # Check if file is related to this resume (basic check by timestamp)
                file_stat = file_path.stat()
                resume_created = tailored_resume.created_at.timestamp()
                
                # If file was created after the resume, it might be related
                if file_stat.st_ctime >= resume_created:
                    statistics = exporter.get_export_statistics(str(file_path))
                    if "error" not in statistics:
                        export_files.append({
                            "filename": file_path.name,
                            "download_url": f"/api/v1/exports/docx/download/{file_path.name}",
                            "statistics": statistics
                        })
        
        # Sort by creation time (newest first)
        export_files.sort(key=lambda x: x["statistics"]["created_at"], reverse=True)
        
        return {
            "tailored_resume_id": tailored_resume_id,
            "tailored_resume_title": tailored_resume.title,
            "exports": export_files,
            "total_exports": len(export_files)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting exports: {str(e)}"
        )


@router.delete("/docx/delete/{filename}")
async def delete_docx_export(
    filename: str,
    db: Session = Depends(get_db)
):
    """
    Delete a DOCX export file.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Validate filename
        if not filename.endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type"
            )
        
        # Construct file path
        exporter = DocxExporter()
        file_path = exporter.export_dir / filename
        
        # Check if file exists
        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Export file not found"
            )
        
        # Delete file
        file_path.unlink()
        
        return {
            "message": f"Export file {filename} deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}"
        )


@router.post("/docx/cleanup")
async def cleanup_old_exports(
    days_old: int = 30,
    db: Session = Depends(get_db)
):
    """
    Clean up old export files.
    """
    try:
        # TODO: Add admin authentication check
        # For now, we'll allow any authenticated user
        
        if days_old < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="days_old must be at least 1"
            )
        
        exporter = DocxExporter()
        exporter.cleanup_old_exports(days_old)
        
        return {
            "message": f"Cleaned up export files older than {days_old} days"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cleaning up exports: {str(e)}"
        )


@router.get("/templates")
async def get_available_templates():
    """
    Get list of available DOCX templates.
    """
    try:
        templates = [
            {
                "name": "professional",
                "display_name": "Professional",
                "description": "Clean, traditional format suitable for most industries",
                "features": ["Standard layout", "Conservative styling", "Clear sections"]
            },
            {
                "name": "modern",
                "display_name": "Modern",
                "description": "Contemporary design with clean lines and good spacing",
                "features": ["Modern typography", "Enhanced spacing", "Stylish headers"]
            },
            {
                "name": "technical",
                "display_name": "Technical",
                "description": "Optimized for technical and engineering roles",
                "features": ["Compact layout", "Technical focus", "Skills prominence"]
            },
            {
                "name": "creative",
                "display_name": "Creative",
                "description": "More expressive design for creative industries",
                "features": ["Creative styling", "Enhanced typography", "Visual appeal"]
            }
        ]
        
        return {
            "templates": templates,
            "default": "professional"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting templates: {str(e)}"
        )
