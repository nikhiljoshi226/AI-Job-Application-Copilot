from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.models.job_description import JobDescription
from app.services.job_description_parser import JobDescriptionParser


class JobDescriptionCreate(BaseModel):
    job_title: str
    company: str
    raw_text: str
    source_url: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    remote_policy: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: Optional[str] = "USD"

router = APIRouter()


@router.post("/")
async def create_job_description(
    job_data: JobDescriptionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new job description with parsing.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Parse job description
        parser = JobDescriptionParser()
        parsed_data = parser.parse_job_description(
            job_data.job_title,
            job_data.company,
            job_data.raw_text
        )
        
        # Validate parsed data
        validation_result = parser.validate_parsed_data(parsed_data)
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Validation failed: {', '.join(validation_result['errors'])}"
            )
        
        # Create job description record
        job_description = JobDescription(
            user_id=current_user_id,
            job_title=job_data.job_title,
            company=job_data.company,
            raw_text=job_data.raw_text,
            parsed_json=parsed_data,
            source_url=job_data.source_url,
            location=job_data.location,
            employment_type=job_data.employment_type,
            remote_policy=job_data.remote_policy,
            salary_min=job_data.salary_min,
            salary_max=job_data.salary_max,
            currency=job_data.currency
        )
        
        db.add(job_description)
        db.commit()
        db.refresh(job_description)
        
        return {
            "id": job_description.id,
            "job_title": job_description.job_title,
            "company": job_description.company,
            "message": "Job description created and parsed successfully",
            "parsing_summary": {
                "required_skills_count": len(parsed_data.get("parsed_content", {}).get("required_skills", [])),
                "preferred_skills_count": len(parsed_data.get("parsed_content", {}).get("preferred_skills", [])),
                "responsibilities_count": len(parsed_data.get("parsed_content", {}).get("responsibilities", [])),
                "keywords_count": len(parsed_data.get("parsed_content", {}).get("keywords", [])),
                "parsing_confidence": parsed_data.get("metadata", {}).get("parsing_confidence", 0)
            },
            "validation": validation_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating job description: {str(e)}"
        )


@router.get("/")
async def get_job_descriptions(db: Session = Depends(get_db)):
    """
    Get all job descriptions for current user.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        job_descriptions = db.query(JobDescription).filter(
            JobDescription.user_id == current_user_id
        ).order_by(JobDescription.created_at.desc()).all()
        
        return {
            "job_descriptions": [
                {
                    "id": jd.id,
                    "job_title": jd.job_title,
                    "company": jd.company,
                    "location": jd.location,
                    "employment_type": jd.employment_type,
                    "remote_policy": jd.remote_policy,
                    "salary_min": jd.salary_min,
                    "salary_max": jd.salary_max,
                    "created_at": jd.created_at,
                    "updated_at": jd.updated_at,
                    "parsing_confidence": jd.parsed_json.get("metadata", {}).get("parsing_confidence", 0) if jd.parsed_json else 0
                }
                for jd in job_descriptions
            ],
            "total": len(job_descriptions)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching job descriptions: {str(e)}"
        )


@router.get("/{job_description_id}")
async def get_job_description(
    job_description_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific job description by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        job_description = db.query(JobDescription).filter(
            JobDescription.id == job_description_id,
            JobDescription.user_id == current_user_id
        ).first()
        
        if not job_description:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job description not found"
            )
        
        return {
            "id": job_description.id,
            "job_title": job_description.job_title,
            "company": job_description.company,
            "raw_text": job_description.raw_text,
            "parsed_json": job_description.parsed_json,
            "source_url": job_description.source_url,
            "location": job_description.location,
            "employment_type": job_description.employment_type,
            "remote_policy": job_description.remote_policy,
            "salary_min": job_description.salary_min,
            "salary_max": job_description.salary_max,
            "currency": job_description.currency,
            "created_at": job_description.created_at,
            "updated_at": job_description.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching job description: {str(e)}"
        )


@router.put("/{job_description_id}")
async def update_job_description(
    job_description_id: int,
    job_data: JobDescriptionCreate,
    db: Session = Depends(get_db)
):
    """
    Update a job description with re-parsing.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        job_description = db.query(JobDescription).filter(
            JobDescription.id == job_description_id,
            JobDescription.user_id == current_user_id
        ).first()
        
        if not job_description:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job description not found"
            )
        
        # Parse updated job description
        parser = JobDescriptionParser()
        parsed_data = parser.parse_job_description(
            job_data.job_title,
            job_data.company,
            job_data.raw_text
        )
        
        # Validate parsed data
        validation_result = parser.validate_parsed_data(parsed_data)
        if not validation_result["is_valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Validation failed: {', '.join(validation_result['errors'])}"
            )
        
        # Update job description
        job_description.job_title = job_data.job_title
        job_description.company = job_data.company
        job_description.raw_text = job_data.raw_text
        job_description.parsed_json = parsed_data
        job_description.source_url = job_data.source_url
        job_description.location = job_data.location
        job_description.employment_type = job_data.employment_type
        job_description.remote_policy = job_data.remote_policy
        job_description.salary_min = job_data.salary_min
        job_description.salary_max = job_data.salary_max
        job_description.currency = job_data.currency
        
        db.commit()
        db.refresh(job_description)
        
        return {
            "id": job_description.id,
            "job_title": job_description.job_title,
            "company": job_description.company,
            "message": "Job description updated and re-parsed successfully",
            "parsing_summary": {
                "required_skills_count": len(parsed_data.get("parsed_content", {}).get("required_skills", [])),
                "preferred_skills_count": len(parsed_data.get("parsed_content", {}).get("preferred_skills", [])),
                "responsibilities_count": len(parsed_data.get("parsed_content", {}).get("responsibilities", [])),
                "keywords_count": len(parsed_data.get("parsed_content", {}).get("keywords", [])),
                "parsing_confidence": parsed_data.get("metadata", {}).get("parsing_confidence", 0)
            },
            "validation": validation_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating job description: {str(e)}"
        )


@router.delete("/{job_description_id}")
async def delete_job_description(
    job_description_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a job description.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        job_description = db.query(JobDescription).filter(
            JobDescription.id == job_description_id,
            JobDescription.user_id == current_user_id
        ).first()
        
        if not job_description:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job description not found"
            )
        
        db.delete(job_description)
        db.commit()
        
        return {
            "message": "Job description deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting job description: {str(e)}"
        )
