from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job_description import JobDescription

router = APIRouter()


@router.get("/")
async def get_job_descriptions(db: Session = Depends(get_db)):
    """
    Get all job descriptions for current user.
    """
    # TODO: Implement authentication and user filtering
    return {"message": "Job descriptions endpoint - authentication needed"}
