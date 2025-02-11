import os, datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request , BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .authentication.oauth2 import get_current_user
from thefuzz import process
from typing import List
from ..Notification import send_mail, check_notify
# # For debugging #
# import logging

# logger = logging.getLogger("uvicorn")
# logger.setLevel(logging.DEBUG)
# # ------ #

router = APIRouter()

@router.post("/", response_model=schemas.LostItem)
# @router.post("/")
async def report_lost_item(
    background_tasks: BackgroundTasks,
    description: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db),
    image: UploadFile = File(None) ,
    current_user: schemas.User = Depends(get_current_user)
):
    # logger.debug(f"Received lost item data: {description}")
    # logger.debug(f"Received image: {image}")
    try:
        # print(f"Received lost item: {lost_item}")
        # print("-----------------",current_user)
        os.makedirs("uploads", exist_ok=True)
        if image:
            upload_path = f"uploads/{image.filename}"
            with open(upload_path, "wb") as buffer:
                buffer.write(await image.read())
            image_url = upload_path  
        else:
            image_url = None
        
        date_object = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        db_lost_item = models.LostItem(
            description=description,
            location=location,
            date=date_object,
            image_url=image_url,
            owner_id = current_user.id
        )
        db.add(db_lost_item)
        db.commit()
        db.refresh(db_lost_item)

        background_tasks.add_task(check_notify.check_among_found_and_notify, description, location)

        return db_lost_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving item: {str(e)}")

@router.get("/", response_model=list[schemas.LostItem])
async def get_lost_items(db: Session = Depends(get_db)):
    return db.query(models.LostItem).all()

@router.delete("/{id}", response_model=schemas.LostItem)
async def delete_lost_item(id: int, db: Session = Depends(get_db)):
    db_lost_item = db.query(models.LostItem).filter(models.LostItem.id == id).first()
    if db_lost_item is None:
        raise HTTPException(status_code=404, detail="Lost item not found")
    
    db.delete(db_lost_item)
    db.commit()
    return db_lost_item

@router.get("/images/{item_id}", response_model=schemas.LostItem)
async def get_lost_item_image(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.query(models.LostItem).filter(models.LostItem.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Lost item not found!!")
    if not item.image_url:
        raise HTTPException(status_code=404, detail="No image for this item have been uploaded!!")

    return FileResponse(item.image_url)


@router.post("/lost-items/claim/{id}")
def claim_lost_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    lost_item = db.query(models.LostItem).filter(models.LostItem.owner_id == id).first()
    if not lost_item:
        raise HTTPException(status_code=404, detail="Lost item not found")
    if lost_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to claim this item"
        )
    db.delete(lost_item)
    db.commit()

    return {"message": "Lost item claimed and removed"}


@router.get("/lost-items/history")
def get_lost_items_history(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    lost_items = db.query(models.LostItem).filter(models.LostItem.owner_id == current_user.id).all()

    if not lost_items:
        return {"message": "You have reported No lost item so far!!"}

    return {"lost_items": lost_items}

@router.get("/nearby-lost-items", response_model=List[schemas.LostItem])
def get_nearby_lost_items(location: str, db: Session = Depends(get_db)):
    lost_items = db.query(models.LostItem).all()

    if not lost_items:
        raise HTTPException(status_code=404, detail="No lost items found")

    locations = [item.location for item in lost_items]
    best_matches = process.extract(location, locations, limit=5, scorer=process.fuzz.partial_ratio)

    matched_items = []
    for item in lost_items:
        if item.location in [match[0] for match in best_matches if match[1] >= 60]:
            matched_items.append(item)
            
    if not matched_items:
        return {"message": "No similar lost items found nearby."}

    return matched_items
