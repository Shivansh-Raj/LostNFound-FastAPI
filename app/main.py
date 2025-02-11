from fastapi import FastAPI
from app import app  
from .database import engine, Base
from .routes import lost, found, match, users
from .routes.authentication import authentication

Base.metadata.create_all(bind=engine)

app.include_router(lost.router, prefix="/lost-items", tags=["Lost Items"])
app.include_router(found.router, prefix="/found-items", tags=["Found Items"])
app.include_router(match.router, prefix="/match-items", tags=["Matching"])
app.include_router(users.router, prefix="/user", tags=["Users"])
app.include_router(authentication.router, prefix="/authentication", tags=["Authentication"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Lost & Found API!"}
