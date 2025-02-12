from fastapi import APIRouter, Depends, Form
from .. import schemas, database
from sqlalchemy.orm import Session 
from fastapi import FastAPI, Depends, status, Response, HTTPException
from ..repository import user_repo

router = APIRouter()

get_db = database.get_db


@router.post('/register')
async def create_user(
    request: schemas.User, 
    db: Session = Depends(get_db)
):
    try:
        return await user_repo.create_user(request, db)
    except Exception as e:
        raise e


@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    return await user_repo.login(username, password, db)

@router.get('/{id}', response_model=schemas.ShowUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    
    try:
        return await user_repo.get_user(id, db)
    except Exception as e:
        raise e


