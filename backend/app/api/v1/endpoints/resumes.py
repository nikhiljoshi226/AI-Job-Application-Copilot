from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.resume import Resume

router = APIRouter()


@router.get("/")
async def get_resumes(db: Session = Depends(get_db)):
    """
    Get all resumes for current user.
    """
    # TODO: Implement authentication and user filtering
    return {"message": "Resumes endpoint - authentication needed"}
