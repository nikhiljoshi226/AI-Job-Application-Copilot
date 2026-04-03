"""Base service class with common functionality."""

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.user import User
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.models.skill_gap_analysis import SkillGapAnalysis


class BaseService:
    """Base service class with common database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_current_user_id(self) -> int:
        """Get current user ID (placeholder for now)."""
        # TODO: Get current user from authentication
        return 1
    
    def verify_resume_ownership(self, resume_id: int, user_id: int) -> Optional[Resume]:
        """Verify that resume exists and belongs to user."""
        return self.db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == user_id
        ).first()
    
    def verify_job_descriptions_ownership(
        self, 
        job_description_ids: List[int], 
        user_id: int
    ) -> List[JobDescription]:
        """Verify that all job descriptions exist and belong to user."""
        return self.db.query(JobDescription).filter(
            JobDescription.id.in_(job_description_ids),
            JobDescription.user_id == user_id
        ).all()
    
    def verify_analysis_ownership(self, analysis_id: int, user_id: int) -> Optional[SkillGapAnalysis]:
        """Verify that analysis exists and belongs to user."""
        return self.db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id,
            SkillGapAnalysis.user_id == user_id
        ).first()
    
    def update_last_accessed(self, analysis: SkillGapAnalysis) -> None:
        """Update last accessed timestamp for analysis."""
        analysis.last_accessed_at = datetime.now(timezone.utc)
        self.db.commit()
    
    def prepare_job_descriptions_data(self, job_descriptions: List[JobDescription]) -> List[Dict[str, Any]]:
        """Prepare job descriptions data for analysis."""
        return [
            {
                "id": jd.id,
                "job_title": jd.job_title,
                "company": jd.company,
                "raw_text": jd.raw_text,
                "parsed_content": jd.parsed_json
            }
            for jd in job_descriptions
        ]
    
    def create_analysis_record(
        self,
        user_id: int,
        resume_id: int,
        analysis_name: str,
        job_description_ids: List[int],
        analysis_result: Dict[str, Any]
    ) -> SkillGapAnalysis:
        """Create a new skill gap analysis record."""
        analysis = SkillGapAnalysis(
            user_id=user_id,
            resume_id=resume_id,
            analysis_name=analysis_name,
            job_description_ids=job_description_ids,
            analysis_summary=analysis_result["skill_gap_analysis"]["analysis_summary"],
            missing_skills=analysis_result["skill_gap_analysis"]["missing_skills"],
            repeated_gaps=analysis_result["skill_gap_analysis"]["repeated_gaps"],
            role_expectations=analysis_result["skill_gap_analysis"]["role_expectations"],
            learning_recommendations=analysis_result["skill_gap_analysis"]["learning_recommendations"],
            project_suggestions=analysis_result["skill_gap_analysis"]["project_suggestions"],
            skill_coverage_score=analysis_result["skill_gap_analysis"]["skill_coverage_score"],
            action_items=analysis_result["skill_gap_analysis"]["action_items"],
            metadata=analysis_result["metadata"]
        )
        
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        
        return analysis
