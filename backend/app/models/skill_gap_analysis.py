from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class SkillGapAnalysis(Base):
    __tablename__ = "skill_gap_analysis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    analysis_name = Column(String(255), nullable=False)
    job_description_ids = Column(JSON, nullable=False)  # Array of JD IDs analyzed
    analysis_summary = Column(JSON, nullable=True)  # Summary of findings
    missing_skills = Column(JSON, nullable=True)  # Missing skills with frequency and importance
    repeated_gaps = Column(JSON, nullable=True)  # Repeated skill gaps across jobs
    role_expectations = Column(JSON, nullable=True)  # Common role expectations
    learning_recommendations = Column(JSON, nullable=True)  # Suggested learning areas
    project_suggestions = Column(JSON, nullable=True)  # Portfolio project ideas
    skill_coverage_score = Column(Float, nullable=True)  # Overall skill coverage percentage
    action_items = Column(JSON, nullable=True)  # Actionable recommendations
    metadata = Column(JSON, nullable=True)  # Generation metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User")
    resume = relationship("Resume")

    def __repr__(self):
        return f"<SkillGapAnalysis(id={self.id}, name={self.analysis_name})>"
