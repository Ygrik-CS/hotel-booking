import json
from datetime import datetime, timedelta
from typing import Tuple

from core.domain import (
    Hotel, RoomType, RatePlan, Price, Availability, Guest, CartItem
)



def load_seed(path: str) -> Tuple[
    Tuple[Hotel, ...],
    Tuple[RoomType, ...],
    Tuple[RatePlan, ...],
    Tuple[Price, ...],
    Tuple[Availability, ...],
    Tuple[Guest, ...]
]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)


    #Отели
    hotels = tuple(
        map(lambda h: Hotel(
            h.get("id"),
            h.get("name"),
            h.get("city"),
            float(h.get("stars", [])),
            tuple(h.get("features", []))
        ), data.get("hotels", []))
    )


    #Типы комнат
    room_types = tuple(
        map(lambda rt: RoomType(
            rt.get("id"),
            rt.get("hotel_id"),
            rt.get("name"),
            int(rt.get("capacity") or 0),
            tuple(rt.get("beds", [])),
            tuple(rt.get("features", []))
        ), data.get("room_types", []))
    )


    #Тарифные планы
    rate_plans = tuple(
        map(lambda rp: RatePlan(
            rp.get("id"),
            rp.get("hotel_id") or "",
            rp.get("room_type_id") or "",
            rp.get("name") or "",
            rp.get("meal") or "",
            bool(rp.get("refundable", False)),
            rp.get("cancel_before_days")
        ), data.get("rates", []))
    )


    #Цены
    prices_data = data.get("prices", [])
    prices = []
    counter = 1
    for i in prices_data:
        pid = i.get("id", f"price_{counter}")
        rate_id = i.get("rate_id", "")
        date_str = i.get("date", "")
        amount = int(i.get("price", i.get("amount", 0)))
        currency = i.get("currency", "KZT")
        prices.append(Price(pid, rate_id, date_str, amount, currency))
        counter += 1
    prices = tuple(prices)


    #Доступность
    availability_data = data.get("availability", [])
    availability = []
    counter = 1
    for i in availability_data:
        aid = i.get("id", f"av_{counter}")
        room_type_id = i.get("room_type_id", "")
        date_str = i.get("date", "")
        available = int(i.get("available", 0))
        availability.append(Availability(aid, room_type_id, date_str, available))
        counter += 1
    availability = tuple(availability)


    #Гости
    guests = tuple(
        map(lambda g: Guest(
            g.get("id"),
            g.get("name"),
            g.get("email") or ""
        ), data.get("guests", []))
    )

    return hotels, room_types, rate_plans, prices, availability, guests



#Корзина
def hold_item(cart: tuple[CartItem, ...], item: CartItem) -> tuple[CartItem, ...]:
    return cart + (item, )



def remove_hold(cart: tuple[CartItem, ...], item_id: str) -> tuple[CartItem, ...]:
    return tuple(filter(lambda x: x.id != item_id, cart))



#Подсчёт цены
def nightly_sum(prices: tuple[Price, ...], checkin: str, checkout: str, rate_id: str) -> int:
    if not checkin or not checkout:
        return 0

    try:
        start = datetime.fromisoformat(checkin)
        end = datetime.fromisoformat(checkout)
    except:  # noqa: E722
        return 0

    total = 0
    cur = start
    while cur < end:
        cur_str = cur.date().isoformat()
        for p in prices:
            if p.rate_id == rate_id and p.date == cur_str:
                total += int(p.amount)
        cur += timedelta(days=1)
    return total
