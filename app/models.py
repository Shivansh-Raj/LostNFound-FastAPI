from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)   
    name =  Column(String)
    password =  Column(String)
    email =  Column(String)
    found_items = relationship("FoundItem", back_populates="finder")
    lost_items = relationship("LostItem", back_populates="owner")
    

class LostItem(Base):
    __tablename__ = "lost_items"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    location = Column(String, index=True)
    date = Column(Date)
    image_url = Column(String, nullable=True)  
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="lost_items")
    matches = relationship("Match", back_populates="lost_item")


class FoundItem(Base):
    __tablename__ = "found_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    location = Column(String)
    date = Column(Date)
    image_url = Column(String, nullable=True)
    finder_id = Column(Integer, ForeignKey("users.id"))
    finder = relationship("User", back_populates = "found_items")
    matches = relationship("Match", back_populates="found_item")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    lost_id = Column(Integer, ForeignKey("lost_items.id"))
    found_id = Column(Integer, ForeignKey("found_items.id"))
    similarity_score = Column(Integer)  
    lost_item = relationship("LostItem", back_populates="matches")
    found_item = relationship("FoundItem", back_populates="matches")