from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class ApplicationStatus(str, enum.Enum):
    PLANNED = "planned"
    APPLIED = "applied"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFER = "offer"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    tailored_resume_id = Column(Integer, ForeignKey("tailored_resumes.id"), nullable=True)
    cover_letter_id = Column(Integer, ForeignKey("cover_letters.id"), nullable=True)
    outreach_draft_id = Column(Integer, ForeignKey("outreach_drafts.id"), nullable=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    company = Column(String(255), nullable=False)
    position_title = Column(String(255), nullable=False)
    position_level = Column(String(50), nullable=True)  # entry, junior, senior, lead
    department = Column(String(100), nullable=True)
    employment_type = Column(String(50), nullable=True)  # full-time, part-time, contract
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    currency = Column(String(3), default="USD")
    location = Column(String(255), nullable=True)
    remote_policy = Column(String(50), nullable=True)  # on-site, hybrid, remote
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PLANNED, nullable=False)
    priority = Column(String(10), default="medium")  # high, medium, low
    source = Column(String(50), nullable=True)  # LinkedIn, Indeed, Company Website, Referral
    source_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # Array of tags
    # Timeline fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    planned_date = Column(DateTime(timezone=True), nullable=True)
    applied_date = Column(DateTime(timezone=True), nullable=True)
    interview_date = Column(DateTime(timezone=True), nullable=True)
    status_updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Outcome fields
    final_status = Column(String(50), nullable=True)  # rejected, offer, withdrawn
    rejection_reason = Column(String(255), nullable=True)  # not qualified, culture fit, position filled
    offer_details = Column(JSON, nullable=True)  # Offer details if received
    feedback = Column(Text, nullable=True)  # Company feedback if provided

    # Relationships
    user = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    tailored_resume = relationship("TailoredResume", back_populates="applications")
    cover_letter = relationship("CoverLetter", back_populates="applications")
    outreach_draft = relationship("OutreachDraft", back_populates="applications")
    job_description = relationship("JobDescription", back_populates="applications")
    outreach_drafts = relationship("OutreachDraft", back_populates="application")
    interview_prep = relationship("InterviewPrep", back_populates="application")

    def __repr__(self):
        return f"<Application(id={self.id}, company={self.company}, status={self.status})>"
