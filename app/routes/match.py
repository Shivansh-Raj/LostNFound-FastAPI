from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from thefuzz import fuzz
from ..database import get_db
from ..models import LostItem, FoundItem
from .. import schemas
from .authentication.oauth2 import get_current_user
from typing import List
from ..repository import match_repo


router = APIRouter()


@router.get("/", response_model=List[schemas.MatchResponse], summary="Get matched lost and found items")
async def match_items(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Retrieve `matched lost and found items` for the current user."""
    try:
        return await match_repo.match_items(db, current_user)
    except Exception as e:
        raise e