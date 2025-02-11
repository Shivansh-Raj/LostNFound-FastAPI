from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import UploadFile

# Users schema
class User(BaseModel):
    username: str
    password: str
    email: str 


class ShowUser(BaseModel):
    name: str
    email: str 
    class Config():
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    id: int 

# Lost item Schemas
class LostItemBase(BaseModel):
    description: str
    location: str
    date: date
    owner_id: int
    class Config:
        from_attributes = True

class LostItemCreate(LostItemBase):
    # image: Optional[UploadFile] = None  
    pass

class LostItem(LostItemBase):
    id: int
    image_url: Optional[str]  

    # Tells Pydantic to treat ORM models as dictionaries
    class Config:
        from_attributes = True  

# Found Item Schemas
class FoundItemBase(BaseModel):
    description: str
    location: str
    date: date
    finder_id: int
    class Config:
        from_attributes = True

class FoundItemCreate(FoundItemBase):
    pass

class FoundItem(FoundItemBase):
    id: int
    image_url: Optional[str]  
    class Config:
        from_attributes = True


# Matching items schemas
class MatchResponse(BaseModel):
    lost_id: int
    found_id: int
    lost_description: str
    found_description: str
    similarity_score: int
    lost_location: str
    found_location: str
    lost_date: date
    found_date: date

    class Config:
        from_attributes = True

