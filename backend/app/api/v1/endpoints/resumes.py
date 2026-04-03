from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import os
import docx
import PyPDF2
from io import BytesIO

from app.core.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.core.config import settings
from app.services.resume_parser import ResumeParser
from app.services.truth_bank import TruthBank

router = APIRouter()


def extract_text_from_file(file: UploadFile, file_type: str) -> str:
    """Extract text from uploaded file based on type."""
    try:
        if file_type == 'application/pdf':
            # Read PDF file
            pdf_content = BytesIO(file.file.read())
            pdf_reader = PyPDF2.PdfReader(pdf_content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            # Read DOCX file
            doc = docx.Document(BytesIO(file.file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file_type == 'text/plain':
            # Read text file
            return file.file.read().decode('utf-8')
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting text from file: {str(e)}"
        )


def get_file_type(filename: str) -> str:
    """Get MIME type based on file extension."""
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    mime_types = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'txt': 'text/plain'
    }
    return mime_types.get(ext, '')


@router.post("/upload")
async def upload_resume(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload a resume file or paste text.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        resume_text = ""
        file_name = ""
        file_type = ""
        
        if file:
            # File upload
            if not file.filename:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No file selected"
                )
            
            # Validate file size
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            if file_size > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes"
                )
            
            # Validate file type
            file_type = get_file_type(file.filename)
            allowed_types = [
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/plain'
            ]
            if file_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unsupported file type. Only PDF, DOCX, and TXT files are allowed."
                )
            
            # Extract text from file
            resume_text = extract_text_from_file(file, file_type)
            file_name = file.filename
            file_type = file.filename.split('.')[-1].lower()
            
        elif text:
            # Text paste
            if not text.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Resume text cannot be empty"
                )
            resume_text = text.strip()
            file_name = "pasted_resume.txt"
            file_type = "txt"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either file or text must be provided"
            )
        
        # Generate title if not provided
        if not title:
            title = file_name or "Uploaded Resume"
        
        # Parse resume text into structured JSON
        parser = ResumeParser()
        parsed_json = parser.parse_resume(resume_text)
        
        # Create truth bank
        truth_bank_service = TruthBank()
        truth_bank = truth_bank_service.create_truth_bank(parsed_json)
        
        # Create resume record
        resume = Resume(
            user_id=current_user_id,
            title=title,
            raw_text=resume_text,
            parsed_json=parsed_json,
            file_name=file_name,
            file_type=file_type,
            is_active="draft"
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return {
            "id": resume.id,
            "title": resume.title,
            "file_name": resume.file_name,
            "file_type": resume.file_type,
            "is_active": resume.is_active,
            "created_at": resume.created_at,
            "message": "Resume uploaded successfully",
            "text_length": len(resume_text),
            "parsed_data": {
                "sections_found": list(parsed_json.keys()),
                "skills_count": len(parsed_json.get("skills", {}).get("technical", [])),
                "experience_count": len(parsed_json.get("experience", [])),
                "education_count": len(parsed_json.get("education", [])),
                "projects_count": len(parsed_json.get("projects", [])),
                "certifications_count": len(parsed_json.get("certifications", []))
            },
            "truth_bank_summary": {
                "total_facts": truth_bank.get("metadata", {}).get("total_facts", 0),
                "confidence_score": truth_bank.get("metadata", {}).get("confidence_score", 0),
                "verification_status": truth_bank.get("metadata", {}).get("verification_status", "unknown")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading resume: {str(e)}"
        )


@router.post("/{resume_id}/parse")
async def parse_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Parse an existing resume to extract structured data.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == current_user_id
        ).first()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        # Parse resume text into structured JSON
        parser = ResumeParser()
        parsed_json = parser.parse_resume(resume.raw_text)
        
        # Create truth bank
        truth_bank_service = TruthBank()
        truth_bank = truth_bank_service.create_truth_bank(parsed_json)
        
        # Update resume with parsed data
        resume.parsed_json = parsed_json
        db.commit()
        db.refresh(resume)
        
        return {
            "id": resume.id,
            "title": resume.title,
            "message": "Resume parsed successfully",
            "parsed_data": {
                "sections_found": list(parsed_json.keys()),
                "skills_count": len(parsed_json.get("skills", {}).get("technical", [])),
                "experience_count": len(parsed_json.get("experience", [])),
                "education_count": len(parsed_json.get("education", [])),
                "projects_count": len(parsed_json.get("projects", [])),
                "certifications_count": len(parsed_json.get("certifications", []))
            },
            "truth_bank_summary": {
                "total_facts": truth_bank.get("metadata", {}).get("total_facts", 0),
                "confidence_score": truth_bank.get("metadata", {}).get("confidence_score", 0),
                "verification_status": truth_bank.get("metadata", {}).get("verification_status", "unknown")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing resume: {str(e)}"
        )


@router.get("/{resume_id}/parsed")
async def get_parsed_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    Get parsed resume data.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == current_user_id
        ).first()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        if not resume.parsed_json:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume has not been parsed yet"
            )
        
        return {
            "id": resume.id,
            "title": resume.title,
            "parsed_json": resume.parsed_json,
            "last_updated": resume.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching parsed resume: {str(e)}"
        )
