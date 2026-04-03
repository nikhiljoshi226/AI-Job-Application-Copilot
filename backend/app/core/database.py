from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the declarative base
Base = declarative_base()

# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    """
    # Import all models to ensure they are registered with Base
    from app.models import (
        user, resume, job_description, fit_report,
        tailored_resume, application, cover_letter,
        outreach_draft, interview_prep, skill_gap_report
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
