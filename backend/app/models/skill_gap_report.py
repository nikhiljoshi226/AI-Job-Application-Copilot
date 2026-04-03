from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class SkillGapReport(Base):
    __tablename__ = "skill_gap_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    required_skills = Column(JSON, nullable=True)  # Skills required by JD
    user_skills = Column(JSON, nullable=True)  # User's current skills
    missing_skills = Column(JSON, nullable=True)  # Skills user needs to acquire
    existing_skills = Column(JSON, nullable=True)  # Skills user already has
    skill_gaps = Column(JSON, nullable=True)  # Detailed gap analysis
    learning_recommendations = Column(JSON, nullable=True)  # Learning resources and paths
    priority_skills = Column(JSON, nullable=True)  # High-priority skills to learn
    time_to_complete = Column(JSON, nullable=True)  # Estimated time to fill gaps
    difficulty_level = Column(String(50), nullable=True)  # Overall difficulty level
    completion_percentage = Column(Float, nullable=True)  # How complete user's skill set is
    processing_time_ms = Column(Integer, nullable=True)
    truthfulness_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")
    resume = relationship("Resume", back_populates="skill_gap_reports")
    job_description = relationship("JobDescription")

    def __repr__(self):
        return f"<SkillGapReport(id={self.id}, completion={self.completion_percentage})>"
