from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    parsed_json = Column(JSON, nullable=True)
    source_url = Column(String(500), nullable=True)
    location = Column(String(255), nullable=True)
    employment_type = Column(String(50), nullable=True)  # full-time, part-time, contract
    remote_policy = Column(String(50), nullable=True)  # on-site, hybrid, remote
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String(3), default="USD")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    fit_reports = relationship("FitReport", back_populates="job_description")
    tailored_resumes = relationship("TailoredResume", back_populates="job_description")
    applications = relationship("Application", back_populates="job_description")
    cover_letters = relationship("CoverLetter", back_populates="job_description")
    outreach_drafts = relationship("OutreachDraft", back_populates="job_description")
    interview_prep = relationship("InterviewPrep", back_populates="job_description")

    def __repr__(self):
        return f"<JobDescription(id={self.id}, title={self.job_title}, company={self.company})>"
