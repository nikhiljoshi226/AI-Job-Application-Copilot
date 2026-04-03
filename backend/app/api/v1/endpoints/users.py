from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

router = APIRouter()


@router.get("/me")
async def get_current_user():
    """
    Get current user information.
    """
    # TODO: Implement authentication
    return {"message": "User endpoint - authentication needed"}
