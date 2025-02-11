from fastapi import APIRouter, Depends, Form
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session 
from fastapi import FastAPI, Depends, status, Response, HTTPException
from .. import hashing
from .authentication.oauth2 import custom_login

router = APIRouter()

get_db = database.get_db

@router.post('/register')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name = request.username,
        email = request.email,
        password = hashing.Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    return custom_login(username, password, db)

@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    # all_blogs = db.query(models.Blog).filter(models.Blog.user_id == id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


