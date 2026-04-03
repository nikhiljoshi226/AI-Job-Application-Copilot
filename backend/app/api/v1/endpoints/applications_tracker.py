from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.user import User
from app.models.application import Application, ApplicationStatus
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.tailored_resume import TailoredResume
from app.models.cover_letter import CoverLetter
from app.models.outreach_draft import OutreachDraft

router = APIRouter()


class ApplicationCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=255)
    position_title: str = Field(..., min_length=1, max_length=255)
    position_level: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=50)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    currency: str = Field("USD", max_length=3)
    location: Optional[str] = Field(None, max_length=255)
    remote_policy: Optional[str] = Field(None, max_length=50)
    priority: str = Field("medium", regex="^(high|medium|low)$")
    source: Optional[str] = Field(None, max_length=50)
    source_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=2000)
    tags: Optional[List[str]] = Field(None)
    planned_date: Optional[datetime] = None
    # Linked resources
    job_description_id: int
    resume_id: Optional[int] = None
    tailored_resume_id: Optional[int] = None
    cover_letter_id: Optional[int] = None
    outreach_draft_id: Optional[int] = None


class ApplicationUpdate(BaseModel):
    company: Optional[str] = Field(None, min_length=1, max_length=255)
    position_title: Optional[str] = Field(None, min_length=1, max_length=255)
    position_level: Optional[str] = Field(None, max_length=50)
    department: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=50)
    salary_min: Optional[int] = Field(None, ge=0)
    salary_max: Optional[int] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    location: Optional[str] = Field(None, max_length=255)
    remote_policy: Optional[str] = Field(None, max_length=50)
    status: Optional[ApplicationStatus] = None
    priority: Optional[str] = Field(None, regex="^(high|medium|low)$")
    source: Optional[str] = Field(None, max_length=50)
    source_url: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = Field(None, max_length=2000)
    tags: Optional[List[str]] = Field(None)
    planned_date: Optional[datetime] = None
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    final_status: Optional[str] = Field(None, max_length=50)
    rejection_reason: Optional[str] = Field(None, max_length=255)
    feedback: Optional[str] = Field(None, max_length=2000)
    # Linked resources
    resume_id: Optional[int] = None
    tailored_resume_id: Optional[int] = None
    cover_letter_id: Optional[int] = None
    outreach_draft_id: Optional[int] = None


class ApplicationResponse(BaseModel):
    id: int
    company: str
    position_title: str
    position_level: Optional[str]
    department: Optional[str]
    employment_type: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    currency: str
    location: Optional[str]
    remote_policy: Optional[str]
    status: ApplicationStatus
    priority: str
    source: Optional[str]
    source_url: Optional[str]
    notes: Optional[str]
    tags: Optional[List[str]]
    created_at: datetime
    planned_date: Optional[datetime]
    applied_date: Optional[datetime]
    interview_date: Optional[datetime]
    status_updated_at: Optional[datetime]
    final_status: Optional[str]
    rejection_reason: Optional[str]
    feedback: Optional[str]
    # Linked resources
    job_description_id: int
    resume_id: Optional[int]
    tailored_resume_id: Optional[int]
    cover_letter_id: Optional[int]
    outreach_draft_id: Optional[int]

    class Config:
        from_attributes = True


class ApplicationSummary(BaseModel):
    id: int
    company: str
    position_title: str
    status: ApplicationStatus
    priority: str
    location: Optional[str]
    created_at: datetime
    applied_date: Optional[datetime]
    interview_date: Optional[datetime]
    final_status: Optional[str]

    class Config:
        from_attributes = True


class ApplicationDashboard(BaseModel):
    applications: List[ApplicationSummary]
    total_count: int
    status_counts: Dict[str, int]
    priority_counts: Dict[str, int]
    recent_activity: List[ApplicationSummary]


@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new job application.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Verify job description exists and belongs to user
        job_description = db.query(JobDescription).filter(
            JobDescription.id == application_data.job_description_id,
            JobDescription.user_id == current_user_id
        ).first()
        
        if not job_description:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job description not found"
            )
        
        # Verify optional linked resources belong to user
        if application_data.resume_id:
            resume = db.query(Resume).filter(
                Resume.id == application_data.resume_id,
                Resume.user_id == current_user_id
            ).first()
            if not resume:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Resume not found"
                )
        
        if application_data.tailored_resume_id:
            tailored_resume = db.query(TailoredResume).filter(
                TailoredResume.id == application_data.tailored_resume_id,
                TailoredResume.user_id == current_user_id
            ).first()
            if not tailored_resume:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tailored resume not found"
                )
        
        if application_data.cover_letter_id:
            cover_letter = db.query(CoverLetter).filter(
                CoverLetter.id == application_data.cover_letter_id,
                CoverLetter.user_id == current_user_id
            ).first()
            if not cover_letter:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cover letter not found"
                )
        
        if application_data.outreach_draft_id:
            outreach_draft = db.query(OutreachDraft).filter(
                OutreachDraft.id == application_data.outreach_draft_id,
                OutreachDraft.user_id == current_user_id
            ).first()
            if not outreach_draft:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Outreach draft not found"
                )
        
        # Create application
        application = Application(
            user_id=current_user_id,
            **application_data.dict(exclude_unset=True)
        )
        
        db.add(application)
        db.commit()
        db.refresh(application)
        
        return application
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating application: {str(e)}"
        )


@router.get("/", response_model=List[ApplicationSummary])
async def get_applications(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    company: Optional[str] = Query(None, description="Filter by company"),
    search: Optional[str] = Query(None, description="Search in company, position, or notes"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get applications with filtering and pagination.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        query = db.query(Application).filter(Application.user_id == current_user_id)
        
        # Apply filters
        if status:
            query = query.filter(Application.status == ApplicationStatus(status))
        
        if priority:
            query = query.filter(Application.priority == priority)
        
        if company:
            query = query.filter(Application.company.ilike(f"%{company}%"))
        
        if search:
            search_filter = or_(
                Application.company.ilike(f"%{search}%"),
                Application.position_title.ilike(f"%{search}%"),
                Application.notes.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Order by created_at desc
        query = query.order_by(Application.created_at.desc())
        
        # Apply pagination
        applications = query.offset(skip).limit(limit).all()
        
        return applications
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching applications: {str(e)}"
        )


@router.get("/dashboard", response_model=ApplicationDashboard)
async def get_applications_dashboard(
    db: Session = Depends(get_db)
):
    """
    Get application dashboard with summary statistics.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Get all applications for user
        applications = db.query(Application).filter(Application.user_id == current_user_id).all()
        
        # Get status counts
        status_counts = {}
        for status in ApplicationStatus:
            count = db.query(Application).filter(
                and_(Application.user_id == current_user_id, Application.status == status)
            ).count()
            status_counts[status.value] = count
        
        # Get priority counts
        priority_counts = {}
        for priority in ["high", "medium", "low"]:
            count = db.query(Application).filter(
                and_(Application.user_id == current_user_id, Application.priority == priority)
            ).count()
            priority_counts[priority] = count
        
        # Get recent activity (last 10)
        recent_applications = db.query(Application).filter(
            Application.user_id == current_user_id
        ).order_by(Application.created_at.desc()).limit(10).all()
        
        return ApplicationDashboard(
            applications=recent_applications,
            total_count=len(applications),
            status_counts=status_counts,
            priority_counts=priority_counts,
            recent_activity=recent_applications
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard: {str(e)}"
        )


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific application by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        application = db.query(Application).filter(
            and_(Application.id == application_id, Application.user_id == current_user_id)
        ).first()
        
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        
        return application
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching application: {str(e)}"
        )


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing application.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        application = db.query(Application).filter(
            and_(Application.id == application_id, Application.user_id == current_user_id)
        ).first()
        
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        
        # Verify linked resources if provided
        if application_data.resume_id:
            resume = db.query(Resume).filter(
                Resume.id == application_data.resume_id,
                Resume.user_id == current_user_id
            ).first()
            if not resume:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Resume not found"
                )
        
        if application_data.tailored_resume_id:
            tailored_resume = db.query(TailoredResume).filter(
                TailoredResume.id == application_data.tailored_resume_id,
                TailoredResume.user_id == current_user_id
            ).first()
            if not tailored_resume:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tailored resume not found"
                )
        
        if application_data.cover_letter_id:
            cover_letter = db.query(CoverLetter).filter(
                CoverLetter.id == application_data.cover_letter_id,
                CoverLetter.user_id == current_user_id
            ).first()
            if not cover_letter:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cover letter not found"
                )
        
        if application_data.outreach_draft_id:
            outreach_draft = db.query(OutreachDraft).filter(
                OutreachDraft.id == application_data.outreach_draft_id,
                OutreachDraft.user_id == current_user_id
            ).first()
            if not outreach_draft:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Outreach draft not found"
                )
        
        # Update application
        update_data = application_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(application, field, value)
        
        db.commit()
        db.refresh(application)
        
        return application
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating application: {str(e)}"
        )


@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an application.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        application = db.query(Application).filter(
            and_(Application.id == application_id, Application.user_id == current_user_id)
        ).first()
        
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found"
            )
        
        db.delete(application)
        db.commit()
        
        return {"message": "Application deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting application: {str(e)}"
        )


@router.get("/statistics")
async def get_application_statistics(
    db: Session = Depends(get_db)
):
    """
    Get application statistics and insights.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        # Overall statistics
        total_applications = db.query(Application).filter(Application.user_id == current_user_id).count()
        
        # Status distribution
        status_stats = db.query(
            Application.status,
            func.count(Application.id).label('count')
        ).filter(Application.user_id == current_user_id).group_by(Application.status).all()
        
        status_distribution = {status.value: count for status, count in status_stats}
        
        # Priority distribution
        priority_stats = db.query(
            Application.priority,
            func.count(Application.id).label('count')
        ).filter(Application.user_id == current_user_id).group_by(Application.priority).all()
        
        priority_distribution = {priority: count for priority, count in priority_stats}
        
        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_applications = db.query(Application).filter(
            and_(
                Application.user_id == current_user_id,
                Application.created_at >= thirty_days_ago
            )
        ).count()
        
        # Success rate (applications with offers)
        offers_count = db.query(Application).filter(
            and_(
                Application.user_id == current_user_id,
                Application.final_status == 'offer'
            )
        ).count()
        
        success_rate = (offers_count / total_applications * 100) if total_applications > 0 else 0
        
        return {
            "total_applications": total_applications,
            "recent_applications": recent_applications,
            "success_rate": round(success_rate, 2),
            "status_distribution": status_distribution,
            "priority_distribution": priority_distribution,
            "offers_count": offers_count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )


@router.get("/statuses")
async def get_application_statuses():
    """
    Get available application statuses.
    """
    return {
        "statuses": [
            {"value": "planned", "label": "Planned", "description": "Application is planned but not yet submitted"},
            {"value": "applied", "label": "Applied", "description": "Application has been submitted"},
            {"value": "interview", "label": "Interview", "description": "Interview scheduled or completed"},
            {"value": "rejected", "label": "Rejected", "description": "Application was rejected"},
            {"value": "offer", "label": "Offer", "description": "Offer received"}
        ]
    }


@router.get("/priorities")
async def get_application_priorities():
    """
    Get available application priorities.
    """
    return {
        "priorities": [
            {"value": "high", "label": "High", "description": "High priority application"},
            {"value": "medium", "label": "Medium", "description": "Medium priority application"},
            {"value": "low", "label": "Low", "description": "Low priority application"}
        ]
    }


@router.get("/sources")
async def get_application_sources():
    """
    Get common application sources.
    """
    return {
        "sources": [
            {"value": "LinkedIn", "label": "LinkedIn", "description": "LinkedIn job posting"},
            {"value": "Indeed", "label": "Indeed", "description": "Indeed job posting"},
            {"value": "Company Website", "label": "Company Website", "description": "Company career page"},
            {"value": "Referral", "label": "Referral", "description": "Employee or network referral"},
            {"value": "Glassdoor", "label": "Glassdoor", "description": "Glassdoor job posting"},
            {"value": "AngelList", "label": "AngelList", "description": "AngelList startup platform"},
            {"value": "Other", "label": "Other", "description": "Other source"}
        ]
    }
