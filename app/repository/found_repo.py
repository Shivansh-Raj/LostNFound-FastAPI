from fastapi import HTTPException, UploadFile, File, Request, BackgroundTasks, status
from sqlalchemy.orm import Session
from app import models, schemas
from ..routes.authentication.oauth2 import get_current_user
import os, datetime
from thefuzz import process,fuzz
from ..Notification import send_mail, check_notify



async def report_found_item(
    background_tasks: BackgroundTasks,
    description: str ,
    location: str ,
    date: str,
    db: Session  ,
    image: UploadFile ,
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
    db_found_item = models.FoundItem(
        description=description,
        location=location,
        date=date_object,
        image_url=image_url,
        finder_id = current_user.id  
    )
    db.add(db_found_item)
    db.commit()
    db.refresh(db_found_item)

    background_tasks.add_task(check_notify.check_among_lost_and_notify, description, location )

    return db_found_item



async def get_all_found_items(db: Session):
    found_items = db.query(models.FoundItem).all()
    return found_items



async def remove_found_item(
    id: int, 
    db: Session,
    current_user: schemas.User
):

    found_item = db.query(models.FoundItem).filter(models.FoundItem.id == id).first()

    if not found_item:
        raise HTTPException(status_code=404, detail="Found item not found")

    db.delete(found_item)
    db.commit()
    return {"message": "Found item removed successfully"}


async def get_found_item_image(item_id: int, request: Request, db: Session):

    item = db.query(models.FoundItem).filter(models.FoundItem.id == item_id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Found item not found!!")
    if not item.image_url:
        raise HTTPException(status_code=404, detail="No image for this item have been uploaded!!")

    return FileResponse(item.image_url)


async def get_nearby_found_items(location: str, db: Session):
    found_items = db.query(models.FoundItem).all()

    if not found_items:
        raise HTTPException(status_code=404, detail="No lost items found")

    locations = [item.location for item in found_items]
    best_matches = process.extract(location, locations, limit=5, scorer=process.fuzz.partial_ratio)

    matched_items = []
    for item in found_items:
        if item.location in [match[0] for match in best_matches if match[1] >= 60]:
            matched_items.append(item)
            
    if not matched_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No found items were reported nearby.")

    return matched_items