# Pydantic схемы для валидации входящих/исходящих данных
from pydantic import BaseModel
from datetime import date
from typing import Optional

class HotelCreate(BaseModel):
    name: str
    city: str
    stars: Optional[int] = 3

class HotelOut(BaseModel):
    id: int
    name: str
    city: str
    stars: int

    class Config:
        orm_mode = True

class RoomCreate(BaseModel):
    hotel_id: int
    number: str
    capacity: int
    price: float
    description: Optional[str] = ""

class RoomOut(BaseModel):
    id: int
    hotel_id: int
    number: str
    capacity: int
    price: float
    description: str

    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    room_id: int
    guest_name: str
    date_from: date
    date_to: date

class BookingOut(BaseModel):
    id: int
    room_id: int
    guest_name: str
    date_from: date
    date_to: date
    paid: bool

    class Config:
        orm_mode = True
