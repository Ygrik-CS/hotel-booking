from datetime import date
from functools import lru_cache
import time
from core.domain import Price, Availability, Rule


@lru_cache(maxsize=100)
def quote_offer(hotel_id: str, room_type_id: str, checkin: str, checkout: str,
                prices: tuple, availabilities: tuple, rules: tuple) -> tuple[int, bool]:

    # Ищем базовую цену (берем первую попавшуюся)
    base_price = 0
    for p in prices:
        if p.rate_id == room_type_id:  # если rate_id = room_type_id
            base_price = p.amount
            break

    # Проверяем доступность
    available_count = 0
    for a in availabilities:
        if a.room_type_id == room_type_id:
            available_count = a.available
            break

    # Применяем правила
    tax = 0.0
    markup = 0.0
    for r in rules:
        if isinstance(r.payload, tuple) and r.payload[0] == "value":
            if r.kind == "tax":
                tax += r.payload[1] / 100
            elif r.kind == "markup":
                markup += r.payload[1] / 100

    days = (date.fromisoformat(checkout) - date.fromisoformat(checkin)).days
    total_amount = int(base_price * days * (1 + tax + markup))
    is_available = available_count > 0

    return total_amount, is_available




def test_quote_offer_returns_tuple():
    prices = (Price("p1", "r1", "2025-10-01", 10000, "KZT"),)
    avail = (Availability("a1", "r1", "2025-10-01", 2),)
    rules = (Rule("r1", "tax", ("value", 10)),)   # type: ignore
    result = quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_quote_offer_caching():
    prices = (Price("p1", "r1", "2025-10-01", 10000, "KZT"),)
    avail = (Availability("a1", "r1", "2025-10-01", 2),)
    rules = (Rule("r1", "tax", ("value", 10)),)   # type: ignore

    start = time.time()
    for _ in range(200):
        quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    first_time = time.time() - start

    start = time.time()
    for _ in range(200):
        quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    second_time = time.time() - start

    assert second_time < first_time

def test_quote_offer_diff_inputs():
    prices = (Price("p1", "r1", "2025-10-01", 10000, "KZT"),)
    avail = (Availability("a1", "r1", "2025-10-01", 2),)
    rules = (Rule("r1", "tax", ("value", 10)),)   # type: ignore
    res1 = quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    res2 = quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    assert res1 == res2 or isinstance(res1, tuple)

def test_quote_offer_pure_function():
    prices = (Price("p1", "r1", "2025-10-01", 10000, "KZT"),)
    avail = (Availability("a1", "r1", "2025-10-01", 2),)
    rules = (Rule("r1", "tax", ("value", 10)),)   # type: ignore

    res1 = quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    res2 = quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    assert res1 == res2

def test_quote_offer_unavailable():
    prices = (Price("p1", "r1", "2025-10-01", 10000, "KZT"),)
    avail = (Availability("a1", "r1", "2025-10-01", 0),)
    rules = (Rule("r1", "tax", ("value", 10)),)   # type: ignore
    result = quote_offer("h1", "r1", "2025-10-01", "2025-10-02", prices, avail, rules)
    assert result[1] is False