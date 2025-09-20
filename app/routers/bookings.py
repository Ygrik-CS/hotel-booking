from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/api/bookings", tags=["bookings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_booking(db, booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/room/{room_id}", response_model=List[schemas.BookingOut])
def room_bookings(room_id: int, db: Session = Depends(get_db)):
    return crud.get_bookings_for_room(db, room_id)

@router.get("/", response_model=List[schemas.BookingOut])
def all_bookings(db: Session = Depends(get_db)):
    return crud.get_all_bookings(db)
