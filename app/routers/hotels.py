from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/api/hotels", tags=["hotels"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.HotelOut)
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    return crud.create_hotel(db, hotel)

@router.get("/", response_model=List[schemas.HotelOut])
def list_hotels(db: Session = Depends(get_db)):
    return crud.get_hotels(db)
