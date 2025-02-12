from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from .authentication.oauth2 import get_current_user
from ..repository import found_repo

router = APIRouter()

@router.post("/", response_model=schemas.FoundItem)
async def report_found_item(
    background_tasks: BackgroundTasks,
    description: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db) ,
    image: UploadFile = File(None),
    current_user: schemas.User = Depends(get_current_user)
):

    try:
        return await found_repo.report_found_item(background_tasks, description, location, date, db, image, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving item: {str(e)}")


@router.get("/", response_model=List[schemas.FoundItem])
async def get_all_found_items(db: Session = Depends(get_db)):

    return await found_repo.get_all_found_items(db)


@router.delete("/{id}")
async def remove_found_item(
    id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):

    try:
        return await found_repo.remove_found_item(id, db, current_user)
    except Exception as e:
        raise e


@router.get("/images/{item_id}", response_model=schemas.FoundItem)
async def get_found_item_image(item_id: int, request: Request, db: Session = Depends(get_db)):

    try: 
        return await found_repo.get_found_item_image(item_id, request, db)
    except Exception as e:
        raise e


@router.get("/nearby-found-items", response_model=List[schemas.FoundItem])
async def get_nearby_found_items(location: str, db: Session = Depends(get_db)):
    
    return await found_repo.get_nearby_found_items(location, db)