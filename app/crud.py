# Операции с БД: create/read для гостиниц, комнат, бронирований
from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas

# HOTELS
def create_hotel(db: Session, hotel: schemas.HotelCreate):
    db_hotel = models.Hotel(name=hotel.name, city=hotel.city, stars=hotel.stars)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).offset(skip).limit(limit).all()

# ROOMS
def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(
        hotel_id=room.hotel_id,
        number=room.number,
        capacity=room.capacity,
        price=room.price,
        description=room.description,
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_rooms_by_hotel(db: Session, hotel_id: int):
    return db.query(models.Room).filter(models.Room.hotel_id == hotel_id).all()

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

# BOOKINGS
def create_booking(db: Session, booking: schemas.BookingCreate):
    # Проверяем диапазон и конфликты
    if booking.date_from > booking.date_to:
        raise ValueError("date_from cannot be after date_to")

    # Проверить пересечения с существующими бронированиями для комнаты
    conflicts = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        models.Booking.date_from <= booking.date_to,
        models.Booking.date_to >= booking.date_from,
    ).all()

    if conflicts:
        raise ValueError("Booking conflict: room is already booked for these dates")

    db_booking = models.Booking(
        room_id=booking.room_id,
        guest_name=booking.guest_name,
        date_from=booking.date_from,
        date_to=booking.date_to,
        paid=False
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_bookings_for_room(db: Session, room_id: int):
    return db.query(models.Booking).filter(models.Booking.room_id == room_id).all()

def get_all_bookings(db: Session):
    return db.query(models.Booking).all()
