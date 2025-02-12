from fastapi import APIRouter, Depends, UploadFile, File, Form, Request , BackgroundTasks
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .authentication.oauth2 import get_current_user
from typing import List
from ..repository import lost_repo


router = APIRouter()

@router.post("/", response_model=schemas.LostItem, summary="Report a lost item")
async def report_lost_item(
    background_tasks: BackgroundTasks,
    description: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db),
    image: UploadFile = File(None),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    Report a lost item with a `description`, `location`, and `optional image`.
    """
    try:
        return await lost_repo.report_lost_item(background_tasks, description, location, date, db, image, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving item: {str(e)}")

@router.get("/", response_model=List[schemas.LostItem], summary="Retrieve all lost items")
async def get_lost_items(db: Session = Depends(get_db)):
    """
    Fetch a list of `all reported lost items`.
    """
    return await lost_repo.get_lost_items(db)

@router.delete("/{id}", response_model=schemas.LostItem, summary="Delete a lost item")
async def delete_lost_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    Remove a lost item by its `ID` (only accessible by the owner).
    """
    try:
        return await lost_repo.delete_lost_item(id, db, current_user)
    except Exception as e:
        raise e

@router.get("/images/{item_id}", response_model=schemas.LostItem, summary="Get lost item image")
async def get_lost_item_image(item_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Retrieve the image of a specific lost item.
    """
    return await lost_repo.get_lost_item_image(item_id, request, db)

@router.post("/lost-items/claim/{id}", summary="Claim a lost item")
async def claim_lost_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    `Claim ownership` of a lost item.
    """
    return await lost_repo.claim_lost_item(id, db, current_user)

@router.get("/lost-items/history", summary="Retrieve lost items history")
async def get_lost_items_history(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    Get a user's `history of lost items`.
    """
    return await lost_repo.get_lost_items_history(db, current_user)

@router.get("/nearby-lost-items", response_model=List[schemas.LostItem], summary="Find lost items nearby")
async def get_nearby_lost_items(location: str, db: Session = Depends(get_db)):
    """
    Fetch lost items near a given `location`.
    """
    try:
        return await lost_repo.get_nearby_lost_items(location, db)
    except Exception as e:
        raise e