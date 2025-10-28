import sqlite3
import os

from typing import Iterator, Tuple, Callable

def iter_available_days(avail: tuple[tuple[str, int], ...], room_type_id: str) -> Iterator[tuple[str, int]]:
    """Лениво перебирает дни доступности для данного типа номера"""
    for day, available_room_id in avail:
        if available_room_id == room_type_id:
            yield (day, available_room_id)

def lazy_offers(hotels, room_types, rates, prices, avail, predicate: Callable) -> Iterator[tuple]:
    for h in hotels:
        for r in room_types:
            if r['hotel_id'] != h['id']:
                continue
            for rt in rates:
                for p in prices:
                    if p['hotel_id'] == h['id'] and p['room_id'] == r['id'] and p['tariff_id'] == rt['id']:
                        offer = (h, r, rt, p['price'])
                        if predicate(offer):
                            yield offer

# Пример работы
def load_data():
    # Путь к базе в папке database
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'hotel.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    hotels = cur.execute('SELECT * FROM hotels').fetchall()
    room_types = cur.execute('SELECT * FROM rooms').fetchall()
    rates = cur.execute('SELECT * FROM tariffs').fetchall()
    prices = cur.execute('SELECT * FROM prices').fetchall()
    conn.close()
    return hotels, room_types, rates, prices

def example_predicate(offer):
    """фильтр: отели 4* и дороже 20000"""
    hotel, room, rate, price = offer
    return hotel['stars'] >= 4 and price > 20000

if __name__ == '__main__':
    hotels, rooms, rates, prices = load_data()
    avail = (('2025-10-25', 1), ('2025-10-26', 2))  

    offers = lazy_offers(hotels, rooms, rates, prices, avail, example_predicate)

    print("Первые 3 подходящих предложения:")
    for i, o in enumerate(offers):
        if i >= 3:  
            break
        hotel, room, rate, price = o
        print(f"{hotel['name']} | {room['room_type']} | {rate['name']} | {price} ₸")
