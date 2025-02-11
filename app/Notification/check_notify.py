from fastapi import Depends
from app.database import get_db, SessionLocal
from .. import models
from sqlalchemy.orm import Session
from thefuzz import fuzz
from . import send_mail

async def check_among_found_and_notify(
    description: str,
    location: str
):
    db: Session = SessionLocal()
    items = db.query(models.FoundItem).all()  
    for item in items:
        
        description_match = fuzz.token_set_ratio(description, item.description) > 80  
        location_match = fuzz.token_set_ratio(location, item.location) > 80  

        if description_match and location_match:
            item_user = db.query(models.User).filter(models.User.id == item.finder_id).first()
            if item_user:
                subject = "Potential Match Found"
                body = f"Hello {item_user.name},\n\nA found item matching your lost item '{item.description}' has been reported. Please check the matching items list for more details."
                await send_mail.send_email(subject, body, item_user.email)


async def check_among_lost_and_notify(
    description: str,
    location: str
):
    db: Session = SessionLocal()
    items = db.query(models.LostItem).all()  
    for item in items:
        
        description_match = fuzz.token_set_ratio(description, item.description) > 80  
        location_match = fuzz.token_set_ratio(location, item.location) > 80  

        if description_match and location_match:
            item_user = db.query(models.User).filter(models.User.id == item.owner_id).first()
            if item_user:
                subject = "Potential Match Found"
                body = f"Hello {item_user.name},\n\nA lost item matching your found item '{item.description}' has been reported. Please check matching items list for more details. Matching to {description} and nearby location {location}"
                await send_mail.send_email(subject, body, item_user.email)