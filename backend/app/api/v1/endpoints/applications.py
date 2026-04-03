from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.application import Application

router = APIRouter()


@router.get("/")
async def get_applications(db: Session = Depends(get_db)):
    """
    Get all applications for current user.
    """
    # TODO: Implement authentication and user filtering
    return {"message": "Applications endpoint - authentication needed"}
