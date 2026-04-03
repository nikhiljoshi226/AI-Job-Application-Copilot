from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)
    parsed_json = Column(JSON, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=False)  # pdf, docx, txt
    is_active = Column(String(50), default="draft")  # draft, active, archived
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="resumes")
    tailored_resumes = relationship("TailoredResume", back_populates="original_resume")
    applications = relationship("Application", back_populates="resume")
    skill_gap_reports = relationship("SkillGapReport", back_populates="resume")

    def __repr__(self):
        return f"<Resume(id={self.id}, title={self.title}, user_id={self.user_id})>"
