from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class InterviewPrep(Base):
    __tablename__ = "interview_prep"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    interview_context = Column(JSON, nullable=True)  # Interview type, format, duration, interviewers
    questions = Column(JSON, nullable=True)  # Array of questions with answers
    star_stories = Column(JSON, nullable=True)  # Array of STAR format stories
    preparation_guide = Column(JSON, nullable=True)  # Focus areas, tips, recommendations
    content_summary = Column(JSON, nullable=True)  # Total questions, stories, prep time
    metadata = Column(JSON, nullable=True)  # Generation model, processing time, quality scores
    truthfulness_score = Column(Float, nullable=True)
    content_quality_score = Column(Float, nullable=True)
    personalization_score = Column(Float, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User")
    application = relationship("Application", back_populates="interview_prep")
    job_description = relationship("JobDescription", back_populates="interview_prep")

    def __repr__(self):
        return f"<InterviewPrep(id={self.id}, application_id={self.application_id})>"
