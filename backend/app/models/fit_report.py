from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class FitReport(Base):
    __tablename__ = "fit_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    overall_fit_score = Column(Float, nullable=False)  # 0-100
    skills_match_score = Column(Float, nullable=False)
    experience_match_score = Column(Float, nullable=False)
    education_match_score = Column(Float, nullable=False)
    responsibilities_alignment = Column(Float, nullable=False)
    matched_skills = Column(JSON, nullable=True)  # Array of matched skills
    missing_skills = Column(JSON, nullable=True)  # Array of missing skills
    partial_matches = Column(JSON, nullable=True)  # Array of partial matches
    role_alignment = Column(JSON, nullable=True)  # Role alignment details
    recommendations = Column(JSON, nullable=True)  # Array of recommendations
    processing_time_ms = Column(Integer, nullable=True)
    truthfulness_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")
    resume = relationship("Resume", back_populates="skill_gap_reports")
    job_description = relationship("JobDescription", back_populates="fit_reports")

    def __repr__(self):
        return f"<FitReport(id={self.id}, fit_score={self.overall_fit_score})>"
