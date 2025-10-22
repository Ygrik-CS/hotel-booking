# База данных бронирования отелей

# Таблица отелей
CREATE TABLE hotels (
    id TEXT PRIMARY KEY,
    name TEXT,
    city TEXT,
    stars INTEGER,
    features TEXT  # перечисление через запятую для простоты
);

# Таблица типов номеров
CREATE TABLE room_types (
    id TEXT PRIMARY KEY,
    hotel_id TEXT,
    name TEXT,
    capacity INTEGER,
    beds TEXT,      # список через запятую
    features TEXT,  # список через запятую
    FOREIGN KEY(hotel_id) REFERENCES hotels(id)
);

# Таблица тарифов
CREATE TABLE rate_plans (
    id TEXT PRIMARY KEY,
    hotel_id TEXT,
    room_type_id TEXT,
    title TEXT,
    meal TEXT,
    refundable INTEGER,
    cancel_before_days INTEGER,
    FOREIGN KEY(hotel_id) REFERENCES hotels(id),
    FOREIGN KEY(room_type_id) REFERENCES room_types(id)
);

# Таблица цен
CREATE TABLE prices (
    id TEXT PRIMARY KEY,
    rate_id TEXT,
    date TEXT,
    amount INTEGER,
    currency TEXT,
    FOREIGN KEY(rate_id) REFERENCES rate_plans(id)
);

# Таблица доступности
CREATE TABLE availability (
    id TEXT PRIMARY KEY,
    room_type_id TEXT,
    date TEXT,
    available INTEGER,
    FOREIGN KEY(room_type_id) REFERENCES room_types(id)
);

# Таблица гостей
CREATE TABLE guests (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT
);

# Таблица корзины брони (hold)
CREATE TABLE cart_items (
    id TEXT PRIMARY KEY,
    hotel_id TEXT,
    room_type_id TEXT,
    rate_id TEXT,
    checkin TEXT,
    checkout TEXT,
    guests INTEGER,
    FOREIGN KEY(hotel_id) REFERENCES hotels(id),
    FOREIGN KEY(room_type_id) REFERENCES room_types(id),
    FOREIGN KEY(rate_id) REFERENCES rate_plans(id)
);

# Таблица подтверждённых бронирований
CREATE TABLE bookings (
    id TEXT PRIMARY KEY,
    guest_id TEXT,
    items TEXT,   # список id CartItem через запятую
    total INTEGER,
    status TEXT,  # held / confirmed / cancelled
    FOREIGN KEY(guest_id) REFERENCES guests(id)
);

# Таблица платежей
CREATE TABLE payments (
    id TEXT PRIMARY KEY,
    booking_id TEXT,
    amount INTEGER,
    ts TEXT,
    method TEXT,
    FOREIGN KEY(booking_id) REFERENCES bookings(id)
);

# Таблица правил
CREATE TABLE rules (
    id TEXT PRIMARY KEY,
    kind TEXT,    # min_stay, max_stay, weekend_markup, city_tax...
    payload TEXT  # JSON-строка с параметрами
);

# Таблица событий
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    ts TEXT,
    name TEXT,    # SEARCH, HOLD, BOOKED, CANCELLED, PRICE_CHANGED
    payload TEXT  # JSON-строка с данными события
);