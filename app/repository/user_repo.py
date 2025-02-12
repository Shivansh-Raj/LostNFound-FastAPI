from .. import schemas, models
from sqlalchemy.orm import Session 
from fastapi import FastAPI, status, HTTPException
from .. import hashing
from ..routes.authentication.oauth2 import custom_login
from email_validator import validate_email, EmailNotValidError



async def create_user(request: schemas.User, db: Session):

    try:
        validate_email(request.email)
        new_user = models.User(
            name = request.username,
            email = request.email,
            password = hashing.Hash.bcrypt(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found!!!")


async def login(
    username: str,
    password: str,
    db: Session,
):

    return custom_login(username, password, db)



async def get_user(id: int, db: Session):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user