from fastapi import APIRouter, Depends, Form
from .. import schemas, database
from sqlalchemy.orm import Session 
from fastapi import FastAPI, Depends, status, Response, HTTPException
from ..repository import user_repo

router = APIRouter()

get_db = database.get_db


@router.post('/register', summary="Register a new user")
async def create_user(
    request: schemas.User, 
    db: Session = Depends(get_db)
):
    """Create a `new user account`."""
    try:
        return await user_repo.create_user(request, db)
    except Exception as e:
        raise e


@router.post("/login", summary="Authenticate and log in a user")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Authenticate a user and `generate an access token`."""
    return await user_repo.login(username, password, db)


@router.get('/{id}', response_model=schemas.ShowUser, summary="Get user details by ID")
async def get_user(id: int, db: Session = Depends(get_db)):
    """Retrieve user details based on their `ID`."""
    try:
        return await user_repo.get_user(id, db)
    except Exception as e:
        raise e


