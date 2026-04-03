from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class OutreachDraft(Base):
    __tablename__ = "outreach_drafts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    draft_type = Column(String(50), nullable=False)  # email_intro, linkedin_note, formal_message
    title = Column(String(255), nullable=False)
    subject_line = Column(String(255), nullable=True)  # For email drafts
    content = Column(JSON, nullable=True)  # Structured content with sections
    raw_text = Column(Text, nullable=True)  # Plain text version
    recipient_info = Column(JSON, nullable=True)  # Recipient details
    generation_options = Column(JSON, nullable=True)  # Generation parameters
    truthfulness_score = Column(Float, nullable=True)
    conciseness_score = Column(Float, nullable=True)
    professionalism_score = Column(Float, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    status = Column(String(50), default="draft")  # draft, approved, sent, archived
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sent_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User")
    resume = relationship("Resume")
    application = relationship("Application", back_populates="outreach_drafts")
    job_description = relationship("JobDescription", back_populates="outreach_drafts")

    def __repr__(self):
        return f"<OutreachDraft(id={self.id}, type={self.draft_type}, status={self.status})>"
