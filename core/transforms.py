import json
from datetime import datetime, timedelta
from typing import Tuple
from core.ftypes import Maybe, Either

from core.domain import Hotel, RoomType, RatePlan, Price, Availability, Guest, CartItem


# Функция загружает все данные из seed.json и превращает их в иммутабельные NamedTuple
def load_seed(
    path: str,
) -> Tuple[
    Tuple[Hotel, ...],
    Tuple[RoomType, ...],
    Tuple[RatePlan, ...],
    Tuple[Price, ...],
    Tuple[Availability, ...],
    Tuple[Guest, ...],
]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Отели (список словарей → кортеж объектов Hotel)
    hotels = tuple(
        map(
            lambda h: Hotel(
                h.get("id"),
                h.get("name"),
                h.get("city"),
                float(h.get("stars", [])),
                tuple(h.get("features", [])),
            ),
            data.get("hotels", []),
        )
    )

    # Типы комнат (вместимость, кровати, удобства)
    room_types = tuple(
        map(
            lambda rt: RoomType(
                rt.get("id"),
                rt.get("hotel_id"),
                rt.get("name"),
                int(rt.get("capacity") or 0),
                tuple(rt.get("beds", [])),
                tuple(rt.get("features", [])),
            ),
            data.get("room_types", []),
        )
    )

    # Тарифы (тарифный план = набор условий по цене, питанию, возврату и т.д.)
    rate_plans = tuple(
        map(
            lambda rp: RatePlan(
                rp.get("id"),
                rp.get("hotel_id") or "",
                rp.get("room_type_id") or "",
                rp.get("name") or "",
                rp.get("meal") or "",
                bool(rp.get("refundable", False)),
                rp.get("cancel_before_days"),
            ),
            data.get("rates", []),
        )
    )

    # Цены
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

    # Доступность номеров (сколько комнат свободно на дату)
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

    # Гости — кто может бронировать
    guests = tuple(
        map(
            lambda g: Guest(g.get("id"), g.get("name"), g.get("email") or ""),
            data.get("guests", []),
        )
    )

    # Возвращаем все данные в виде кортежей (иммутабельно)
    return hotels, room_types, rate_plans, prices, availability, guests


# Добавляем новый элемент в корзину (создаём новый кортеж)
def hold_item(cart: tuple[CartItem, ...], item: CartItem) -> tuple[CartItem, ...]:
    # создаём новую корзину, старую не трогаем
    return cart + (item,)


# Удаляем элемент по id без изменений исходного объекта
def remove_hold(cart: tuple[CartItem, ...], item_id: str) -> tuple[CartItem, ...]:
    # фильтруем корзину, оставляем всё кроме удаляемого
    return tuple(filter(lambda x: x.id != item_id, cart))


# Считаем общую стоимость проживания между датами
def nightly_sum(
    prices: tuple[Price, ...], checkin: str, checkout: str, rate_id: str
) -> int:
    # если даты пустые — возвращаем 0
    if not checkin or not checkout:
        return 0

    # пробуем перевести даты в формат ISO, если ошибка — 0
    try:
        start = datetime.fromisoformat(checkin)
        end = datetime.fromisoformat(checkout)
    except:  # noqa: E722
        return 0

    total = 0
    cur = start

    # идём по дням и суммируем цену за каждую ночь
    while cur < end:
        cur_str = cur.date().isoformat()
        for p in prices:
            # ищем цену именно по нужному тарифу и дате
            if p.rate_id == rate_id and p.date == cur_str:
                total += int(p.amount)
        cur += timedelta(days=1)
    return total






def safe_rate(rates, rate_id):
    for r in rates:
        if getattr(r, "id", None) == rate_id:
            return Maybe.some(r)
    return Maybe.nothing()


def validate_cart_item(item, availability, rules=(), room_types=()):
    # просто проверяем что даты не пустые
    if not getattr(item, "checkin", None) or not getattr(item, "checkout", None):
        return Either.left({"error": "invalid_dates"})
    return Either.right(item)


def validate_booking(booking, prices=(), availability=(), rules=(), rates=(), room_types=()):
    # просто проверяем что внутри есть хотя бы один item
    if not getattr(booking, "items", ()):
        return Either.left({"error": "no_items"})
    return Either.right(booking)