import os, datetime
from fastapi import HTTPException, UploadFile, File, Request , BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .. import models, schemas
from thefuzz import process
from ..Notification import send_mail, check_notify

async def report_lost_item(
    background_tasks: BackgroundTasks,
    description: str,
    location: str,
    date: str,
    db: Session,
    image: UploadFile,
    current_user: schemas.User
):
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


async def get_lost_items(db: Session):
    return db.query(models.LostItem).all()


async def delete_lost_item(
    id: int,
    db: Session,
    current_user: schemas.User
):
    db_lost_item = db.query(models.LostItem).filter(models.LostItem.id == id).first()
    if db_lost_item is None:
        raise HTTPException(status_code=404, detail="Lost item not found")
    
    if db_lost_item.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="You are not authorized to delete this item.")
    
    db.delete(db_lost_item)
    db.commit()
    return db_lost_item

async def get_lost_item_image(item_id: int, request: Request, db: Session):
    item = db.query(models.LostItem).filter(models.LostItem.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Lost item not found!!")
    if not item.image_url:
        raise HTTPException(status_code=404, detail="No image for this item have been uploaded!!")

    return FileResponse(item.image_url)


async def claim_lost_item(
    id: int,
    db: Session,
    current_user: schemas.User 
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

async def get_lost_items_history(
    db: Session,
    current_user: schemas.User
):
    lost_items = db.query(models.LostItem).filter(models.LostItem.owner_id == current_user.id).all()

    if not lost_items:
        return {"message": "You have reported No lost item so far!!"}

    return {"lost_items": lost_items}

async def get_nearby_lost_items(location: str, db: Session):
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