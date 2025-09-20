from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RoomOut)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    # проверка существования гостиницы опционально
    return crud.create_room(db, room)

@router.get("/hotel/{hotel_id}", response_model=List[schemas.RoomOut])
def rooms_by_hotel(hotel_id: int, db: Session = Depends(get_db)):
    return crud.get_rooms_by_hotel(db, hotel_id)
