from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(JSON, nullable=True)  # Structured cover letter content
    raw_text = Column(Text, nullable=True)  # Plain text version
    generation_options = Column(JSON, nullable=True)  # Generation parameters used
    truthfulness_score = Column(Float, nullable=True)
    grammar_score = Column(Float, nullable=True)
    personalization_score = Column(Float, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    status = Column(String(50), default="draft")  # draft, approved, sent, archived
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")
    application = relationship("Application", back_populates="cover_letters")
    job_description = relationship("JobDescription", back_populates="cover_letters")

    def __repr__(self):
        return f"<CoverLetter(id={self.id}, title={self.title}, status={self.status})>"
