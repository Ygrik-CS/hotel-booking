from typing import Tuple, Iterable
from functools import reduce
from datetime import datetime, timedelta
import json

from core.domain import (
    Hotel,
    RoomType,
    RatePlan,
    Price,
    Availability,
    Guest,
    CartItem,
)

def _date_range(checkin: str, checkout: str) -> Tuple[str, ...]:
    """Return tuple of date strings for nights from checkin (inclusive) to checkout (exclusive)."""
    fmt = "%Y-%m-%d"
    a = datetime.fromisoformat(checkin)
    b = datetime.fromisoformat(checkout)
    if a >= b:
        return tuple()
    cur = a
    out = []
    while cur < b:
        out.append(cur.date().isoformat())
        cur = cur + timedelta(days=1)
    return tuple(out)

def load_seed(path: str) -> Tuple[Tuple[Hotel, ...], Tuple[RoomType, ...], Tuple[RatePlan, ...], Tuple[Price, ...], Tuple[Availability, ...], Tuple[Guest, ...]]:
    """
    Load seed.json and return typed, immutable tuples of domain models.
    Returns a tuple: (hotels, room_types, rates, prices, availability, guests)
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    hotels = tuple(Hotel(**h) for h in data.get("hotels", []))
    room_types = tuple(RoomType(**rt) for rt in data.get("room_types", []))
    rates = tuple(RatePlan(**r) for r in data.get("rates", []))
    prices = tuple(Price(**p) for p in data.get("prices", []))
    availability = tuple(Availability(**a) for a in data.get("availability", []))
    guests = tuple(Guest(**g) for g in data.get("guests", []))
    return hotels, room_types, rates, prices, availability, guests

def hold_item(cart: Tuple[CartItem, ...], item: CartItem) -> Tuple[CartItem, ...]:
    """
    Return a new tuple with the CartItem added (if not already present).
    Pure function: does not mutate input.
    """
    # use filter/map/reduce style minimally to satisfy HOF usage requirements
    exists = any(map(lambda ci: ci.id == item.id, cart))
    if exists:
        return cart
    return cart + (item,)

def remove_hold(cart: Tuple[CartItem, ...], item_id: str) -> Tuple[CartItem, ...]:
    """
    Return a new tuple with items whose id != item_id
    """
    filtered = tuple(filter(lambda ci: ci.id != item_id, cart))
    return filtered

def nightly_sum(prices: Tuple[Price, ...], checkin: str, checkout: str, rate_id: str) -> int:
    """
    Sum nightly prices for given rate_id between checkin (inclusive) and checkout (exclusive).
    Uses filter/map/reduce to operate over immutable tuples.
    """
    nights = set(_date_range(checkin, checkout))
    # select prices matching rate_id and in desired nights
    selected = tuple(filter(lambda p: p.rate_id == rate_id and p.date in nights, prices))
    # map to amounts
    amounts = tuple(map(lambda p: p.amount, selected))
    # reduce to sum
    total = reduce(lambda a, b: a + b, amounts, 0)
    return total
