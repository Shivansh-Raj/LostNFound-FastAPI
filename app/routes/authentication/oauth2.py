from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from . import tokens
from ... import models
from ...hashing import Hash
from sqlalchemy.orm import Session

# here tokenUrl is gonna define where token is going to be fetched
# in this case at /login token is going to be get fetched
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/login")

def get_current_user(request: Request, token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return tokens.verify_token(token, credentials_exception)

def custom_login(username: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.name == username).first()
    if not user:
        raise HTTPException(detail="Invalid Credentials", status_code=status.HTTP_404_NOT_FOUND)
    
    if not Hash.verify(password, user.password):
        raise HTTPException(detail="Incorrect Password", status_code=status.HTTP_400_BAD_REQUEST)
    
    access_token = tokens.create_access_token(data={"sub": user.name, "id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}