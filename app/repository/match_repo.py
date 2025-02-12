from fastapi import HTTPException
from sqlalchemy.orm import Session
from thefuzz import fuzz
from ..models import LostItem, FoundItem
from .. import schemas
from typing import List


MATCH_THRESHOLD = 65  


async def match_items(
    db: Session ,
    current_user: schemas.User 
):

    lost_items = db.query(LostItem).all()
    found_items = db.query(FoundItem).all()
    matches = []

    for lost in lost_items:
        for found in found_items:
            similarity_score = fuzz.token_set_ratio(lost.description.lower(), found.description.lower())

            if similarity_score >= MATCH_THRESHOLD:
                matches.append({
                    "lost_id": lost.id,
                    "found_id": found.id,
                    "lost_description": lost.description,
                    "found_description": found.description,
                    "similarity_score": similarity_score,
                    "lost_location": lost.location,
                    "found_location": found.location,
                    "lost_date": lost.date,
                    "found_date": found.date
                })

    if not matches:
        raise HTTPException(status_code=404, detail="No matching items found.")

    return matches
