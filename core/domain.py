from typing import NamedTuple, Tuple, Optional

class Hotel(NamedTuple):
    id: str
    name: str
    city: str
    stars: float
    features: Tuple[str, ...]

class RoomType(NamedTuple):
    id: str
    hotel_id: str
    name: str   
    capacity: int
    beds: Tuple[str, ...]
    features: Tuple[str, ...]

class RatePlan(NamedTuple):
    id: str
    hotel_id: str
    room_type_id: str
    title: str
    meal: str
    refundable: bool
    cancel_before_days: Optional[int]

class Price(NamedTuple):
    id: str
    rate_id: str 
    date: str
    amount: int 
    currency: str

class Availability(NamedTuple):
    id: str
    room_type_id: str 
    date: str 
    available: int

class Guest(NamedTuple):
    id: str
    name: str
    email: str 

class CartItem(NamedTuple):
    id: str
    hotel_id: str
    room_type_id: str 
    rate_id: str
    checkin: str 
    checkout: str
    guests: int

class Booking(NamedTuple):
    id: str
    guest_id: str 
    items: Tuple[CartItem,...] 
    total: int
    status: str

class Payment(NamedTuple):
    id: str
    booking_id: str
    amount: int
    ts: str
    method: str

class Event(NamedTuple):
    id: str
    ts: str
    name: str 
    payload: dict

class Rule(NamedTuple):
    id: str
    kind: str 
    payload: dict



#hotel = Hotel(id="1", name="Grand", city="Paris", stars=5, features=("WiFi", "Pool"))
#room = RoomType(id="101", hotel_id="1", name="Suite", capacity=2, beds=("King",), features=("AC",))