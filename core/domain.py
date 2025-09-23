from dataclasses import dataclass
from typing import Tuple, Optional, Dict

@dataclass(frozen=True)
class Hotel:
    id: str
    name: str
    stars: int
    city: str
    features: Tuple[str, ...]

@dataclass(frozen=True)
class RoomType:
    id: str
    hotel_id: str
    name: str
    capacity: int
    beds: Tuple[str, ...]
    features: Tuple[str, ...]

@dataclass(frozen=True)
class RatePlan:
    id: str
    hotel_id: str
    room_type_id: str
    title: str
    meal: str
    refundable: bool
    cancel_before_days: Optional[int]

@dataclass(frozen=True)
class Price:
    id: str
    rate_id: str
    date: str  # ISO YYYY-MM-DD
    amount: int  # integer (cents / tiyin)
    currency: str

@dataclass(frozen=True)
class Availability:
    id: str
    room_type_id: str
    date: str  # ISO date
    available: int

@dataclass(frozen=True)
class Guest:
    id: str
    name: str
    email: str

@dataclass(frozen=True)
class CartItem:
    id: str
    hotel_id: str
    room_type_id: str
    rate_id: str
    checkin: str
    checkout: str
    guests: int

@dataclass(frozen=True)
class Booking:
    id: str
    guest_id: str
    items: Tuple[CartItem, ...]
    total: int
    status: str

@dataclass(frozen=True)
class Payment:
    id: str
    booking_id: str
    amount: int
    ts: str
    method: str

@dataclass(frozen=True)
class Event:
    id: str
    ts: str
    name: str
    payload: Dict

@dataclass(frozen=True)
class Rule:
    id: str
    kind: str
    payload: Dict
