from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import time

from app.core.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.fit_report import FitReport
from app.services.fit_analyzer import FitAnalyzer


class FitAnalysisRequest(BaseModel):
    resume_id: int
    job_description_id: int


router = APIRouter()


@router.post("/analyze")
async def analyze_fit(
    request: FitAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze fit between resume and job description.
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
        
        # Check if fit analysis already exists
        existing_report = db.query(FitReport).filter(
            FitReport.resume_id == request.resume_id,
            FitReport.job_description_id == request.job_description_id
        ).first()
        
        if existing_report:
            return {
                "id": existing_report.id,
                "message": "Fit analysis already exists",
                "fit_analysis": existing_report.role_alignment
            }
        
        # Perform fit analysis
        start_time = time.time()
        analyzer = FitAnalyzer()
        analysis = analyzer.analyze_fit(resume.parsed_json, job_description.parsed_json)
        processing_time = int((time.time() - start_time) * 1000)
        
        # Create fit report
        fit_report = FitReport(
            user_id=current_user_id,
            resume_id=request.resume_id,
            job_description_id=request.job_description_id,
            overall_fit_score=analysis["fit_score"],
            skills_match_score=_calculate_skills_score(analysis["skills_analysis"]),
            experience_match_score=_calculate_experience_score(analysis["experience_analysis"]),
            education_match_score=_calculate_education_score(analysis["education_analysis"]),
            responsibilities_alignment=_calculate_responsibilities_score(analysis["experience_analysis"]),
            matched_skills=analysis["skills_analysis"]["matched_skills"],
            missing_skills=analysis["skills_analysis"]["missing_skills"],
            partial_matches=analysis["skills_analysis"]["partial_matches"],
            role_alignment=analysis["role_alignment"],
            recommendations=analysis["role_alignment"]["recommendations"],
            processing_time_ms=processing_time,
            truthfulness_score=analysis["metadata"]["confidence_score"]
        )
        
        db.add(fit_report)
        db.commit()
        db.refresh(fit_report)
        
        return {
            "id": fit_report.id,
            "message": "Fit analysis completed successfully",
            "fit_analysis": analysis,
            "processing_time_ms": processing_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing fit: {str(e)}"
        )


@router.get("/reports")
async def get_fit_reports(db: Session = Depends(get_db)):
    """
    Get all fit reports for current user.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        fit_reports = db.query(FitReport).filter(
            FitReport.user_id == current_user_id
        ).order_by(FitReport.created_at.desc()).all()
        
        return {
            "fit_reports": [
                {
                    "id": report.id,
                    "resume_id": report.resume_id,
                    "job_description_id": report.job_description_id,
                    "overall_fit_score": report.overall_fit_score,
                    "skills_match_score": report.skills_match_score,
                    "experience_match_score": report.experience_match_score,
                    "education_match_score": report.education_match_score,
                    "created_at": report.created_at,
                    "processing_time_ms": report.processing_time_ms
                }
                for report in fit_reports
            ],
            "total": len(fit_reports)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching fit reports: {str(e)}"
        )


@router.get("/reports/{report_id}")
async def get_fit_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific fit report by ID.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        fit_report = db.query(FitReport).filter(
            FitReport.id == report_id,
            FitReport.user_id == current_user_id
        ).first()
        
        if not fit_report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fit report not found"
            )
        
        # Get related resume and job description info
        resume = db.query(Resume).filter(Resume.id == fit_report.resume_id).first()
        job_description = db.query(JobDescription).filter(JobDescription.id == fit_report.job_description_id).first()
        
        return {
            "id": fit_report.id,
            "resume": {
                "id": resume.id,
                "title": resume.title
            } if resume else None,
            "job_description": {
                "id": job_description.id,
                "job_title": job_description.job_title,
                "company": job_description.company
            } if job_description else None,
            "overall_fit_score": fit_report.overall_fit_score,
            "skills_match_score": fit_report.skills_match_score,
            "experience_match_score": fit_report.experience_match_score,
            "education_match_score": fit_report.education_match_score,
            "responsibilities_alignment": fit_report.responsibilities_alignment,
            "matched_skills": fit_report.matched_skills,
            "missing_skills": fit_report.missing_skills,
            "partial_matches": fit_report.partial_matches,
            "role_alignment": fit_report.role_alignment,
            "recommendations": fit_report.recommendations,
            "processing_time_ms": fit_report.processing_time_ms,
            "truthfulness_score": fit_report.truthfulness_score,
            "created_at": fit_report.created_at,
            "updated_at": fit_report.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching fit report: {str(e)}"
        )


@router.delete("/reports/{report_id}")
async def delete_fit_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a fit report.
    """
    try:
        # TODO: Get current user from authentication
        current_user_id = 1  # Placeholder for now
        
        fit_report = db.query(FitReport).filter(
            FitReport.id == report_id,
            FitReport.user_id == current_user_id
        ).first()
        
        if not fit_report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fit report not found"
            )
        
        db.delete(fit_report)
        db.commit()
        
        return {
            "message": "Fit report deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting fit report: {str(e)}"
        )


def _calculate_skills_score(skills_analysis: Dict[str, Any]) -> float:
    """Calculate skills match score."""
    total_skills = len(skills_analysis["matched_skills"]) + len(skills_analysis["missing_skills"])
    if total_skills == 0:
        return 0.0
    
    matched_count = len(skills_analysis["matched_skills"])
    partial_count = len(skills_analysis["partial_matches"])
    
    # Weight exact matches higher than partial matches
    score = (matched_count * 1.0 + partial_count * 0.5) / total_skills * 100
    return round(score, 2)


def _calculate_experience_score(experience_analysis: Dict[str, Any]) -> float:
    """Calculate experience match score."""
    score = 0.0
    
    # Level alignment
    if experience_analysis["level_alignment"] == "aligned":
        score += 40
    elif experience_analysis["level_alignment"] == "close":
        score += 25
    elif experience_analysis["level_alignment"] == "misaligned":
        score += 10
    
    # Years experience
    if experience_analysis["years_experience_match"] == "sufficient":
        score += 30
    elif experience_analysis["years_experience_match"] == "insufficient":
        score += 15
    elif experience_analysis["years_experience_match"] == "not_specified":
        score += 20
    
    # Relevant experience highlights
    highlights = experience_analysis.get("relevant_experience_highlights", [])
    if highlights:
        avg_relevance = sum(h["relevance_score"] for h in highlights) / len(highlights)
        score += avg_relevance * 30
    
    return round(score, 2)


def _calculate_education_score(education_analysis: Dict[str, Any]) -> float:
    """Calculate education match score."""
    score = 0.0
    
    if education_analysis["education_match"] == "meets_requirements":
        score += 50
    elif education_analysis["education_match"] == "below_requirements":
        score += 20
    else:
        score += 35
    
    # Field relevance
    field_relevance = education_analysis.get("field_relevance", "medium")
    if field_relevance == "high":
        score += 30
    elif field_relevance == "medium":
        score += 20
    else:
        score += 10
    
    # Additional education needed
    if not education_analysis.get("additional_education_needed"):
        score += 20
    
    return round(score, 2)


def _calculate_responsibilities_score(experience_analysis: Dict[str, Any]) -> float:
    """Calculate responsibilities alignment score."""
    score = 0.0
    
    # Experience gaps impact
    gaps = experience_analysis.get("experience_gaps", [])
    if not gaps:
        score += 100
    elif len(gaps) <= 2:
        score += 70
    elif len(gaps) <= 4:
        score += 40
    else:
        score += 20
    
    return round(score, 2)
