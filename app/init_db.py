# Скрипт для создания таблиц и заполнения тестовыми данными
from .database import engine, Base, SessionLocal
from . import models, crud, schemas
from datetime import date

def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Если нет отелей — создаём пример
        hotels = db.query(models.Hotel).all()
        if not hotels:
            h1 = crud.create_hotel(db, schemas.HotelCreate(name="Astana Hotel", city="Astana", stars=5))
            h2 = crud.create_hotel(db, schemas.HotelCreate(name="Almaty Plaza", city="Almaty", stars=4))

            crud.create_room(db, schemas.RoomCreate(hotel_id=h1.id, number="101", capacity=2, price=50.0, description="Double room"))
            crud.create_room(db, schemas.RoomCreate(hotel_id=h1.id, number="102", capacity=3, price=70.0, description="Triple room"))
            crud.create_room(db, schemas.RoomCreate(hotel_id=h2.id, number="201", capacity=2, price=45.0, description="Comfort"))

            # Пример брони
            try:
                crud.create_booking(db, schemas.BookingCreate(room_id=1, guest_name="Иван", date_from=date(2025,9,25), date_to=date(2025,9,27)))
            except Exception:
                pass
    finally:
        db.close()

if __name__ == "__main__":
    init()
    print("DB initialized")
