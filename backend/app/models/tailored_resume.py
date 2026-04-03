from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TailoredResume(Base):
    __tablename__ = "tailored_resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    title = Column(String(255), nullable=False)
    tailored_content = Column(JSON, nullable=True)  # Full tailored resume content
    suggestions = Column(JSON, nullable=True)  # Array of tailoring suggestions
    applied_suggestions = Column(JSON, nullable=True)  # Array of applied changes
    final_alignment_score = Column(Integer, nullable=False)  # 0-100
    improvement_percentage = Column(Integer, nullable=True)
    truthfulness_score = Column(Float, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    version = Column(Integer, default=1)
    status = Column(String(50), default="draft")  # draft, approved, archived
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")
    original_resume = relationship("Resume", back_populates="tailored_resumes")
    job_description = relationship("JobDescription", back_populates="tailored_resumes")
    applications = relationship("Application", back_populates="tailored_resume")

    def __repr__(self):
        return f"<TailoredResume(id={self.id}, title={self.title}, status={self.status})>"
