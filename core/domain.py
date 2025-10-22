from typing import NamedTuple, Tuple, Optional


# Класс отеля, где хранятся базовые данные
class Hotel(NamedTuple):
    id: str  # айди отеля
    name: str  # название
    city: str  # город
    stars: float  # звёзды
    features: Tuple[str, ...]  # удобства (wifi, парковка и т.д.)


# Тип номера в отеле
class RoomType(NamedTuple):
    id: str  # айди типа номера
    hotel_id: str  # айди отеля
    name: str  # название типа
    capacity: int  # вместимость
    beds: Tuple[str, ...]  # список кроватей
    features: Tuple[str, ...]  # удобства номера


# Тарифный план, описывает условия брони
class RatePlan(NamedTuple):
    id: str  # айди тарифа
    hotel_id: str  # айди отеля
    room_type_id: str  # айди типа номера
    title: str  # название тарифа
    meal: str  # тип питания
    refundable: bool  # можно ли отменить
    cancel_before_days: Optional[int]  # за сколько дней до заезда можно отменить


# Цена за ночь
class Price(NamedTuple):
    id: str  # айди записи
    rate_id: str  # айди тарифа
    date: str  # дата
    amount: int  # стоимость в копейках/тийынах
    currency: str  # валюта


# Доступность номеров
class Availability(NamedTuple):
    id: str  # айди записи
    room_type_id: str  # айди типа номера
    date: str  # дата
    available: int  # сколько номеров свободно


# Инфо о госте
class Guest(NamedTuple):
    id: str  # айди гостя
    name: str  # имя
    email: str  # почта


# Элемент корзины (предварительная бронь)
class CartItem(NamedTuple):
    id: str  # айди позиции
    hotel_id: str  # айди отеля
    room_type_id: str  # айди типа номера
    rate_id: str  # айди тарифа
    checkin: str  # дата заезда
    checkout: str  # дата выезда
    guests: int  # кол-во гостей


# Бронь (уже оформленная)
class Booking(NamedTuple):
    id: str  # айди брони
    guest_id: str  # кто забронировал
    items: Tuple[CartItem, ...]  # список позиций из корзины
    total: int  # итоговая сумма
    status: str  # статус (held, confirmed, cancelled)


# Платёж
class Payment(NamedTuple):
    id: str  # айди платежа
    booking_id: str  # айди брони
    amount: int  # сумма платежа
    ts: str  # время платежа
    method: str  # метод оплаты (карта, нал, онлайн)


# Событие (для системы или логов)
class Event(NamedTuple):
    id: str  # айди события
    ts: str  # время
    name: str  # тип события
    payload: dict  # доп инфа (например, данные по брони)


# Правило (ограничение или надбавка)
class Rule(NamedTuple):
    id: str  # айди правила
    kind: str  # тип (min_stay, max_stay и т.д.)
    payload: dict  # данные правила (например, {"min_days": 2})
