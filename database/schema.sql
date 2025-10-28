PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS generation_logs;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS tariffs;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS countries;

PRAGMA foreign_keys = ON;

CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    code TEXT UNIQUE
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    country_id INTEGER,
    registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

CREATE TABLE hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT,
    country_id INTEGER,
    stars INTEGER CHECK(stars BETWEEN 1 AND 5),
    description TEXT,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL,
    room_type TEXT,
    capacity INTEGER,
    base_price REAL,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id)
);

CREATE TABLE tariffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER,
    room_id INTEGER,
    tariff_id INTEGER,
    start_date TEXT,
    end_date TEXT,
    price REAL,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (tariff_id) REFERENCES tariffs(id)
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    room_id INTEGER,
    tariff_id INTEGER,
    check_in TEXT,
    check_out TEXT,
    total_price REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (tariff_id) REFERENCES tariffs(id)
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

CREATE TABLE generation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_table TEXT,
    record_id INTEGER,
    generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    condition TEXT,
    action TEXT
);

INSERT INTO countries (name, code) VALUES
('Kazakhstan', 'KZ'),
('Russia', 'RU'),
('Uzbekistan', 'UZ');

INSERT INTO customers (full_name, email, phone, country_id)
VALUES
('Ali Serik', 'ali@example.com', '+77001234567', 1),
('Dana Nurtas', 'dana@example.com', '+77007654321', 1),
('Ivan Petrov', 'ivan@example.com', '+79998887766', 2);

INSERT INTO hotels (name, city, country_id, stars, description)
VALUES
('Hotel Almaty Grand', 'Almaty', 1, 5, 'Luxury hotel with mountain view'),
('Astana Comfort', 'Astana', 1, 4, 'Modern city hotel'),
('Tashkent Plaza', 'Tashkent', 3, 4, 'Elegant hotel in the heart of the city');

INSERT INTO rooms (hotel_id, room_type, capacity, base_price)
VALUES
(1, 'Standard', 2, 18000),
(1, 'Luxe', 3, 25000),
(2, 'Family', 2, 15000),

INSERT INTO tariffs (name, description)
VALUES
('BB', 'Bed & Breakfast'),
('HB', 'Half Board'),
('AI', 'All Inclusive');

INSERT INTO prices (hotel_id, room_id, tariff_id, start_date, end_date, price)
VALUES
(1, 1, 1, '2025-01-01', '2025-03-31', 18000),
(1, 2, 2, '2025-04-01', '2025-06-30', 25000),
(2, 3, 3, '2025-07-01', '2025-09-30', 15000),
(3, 4, 1, '2025-10-01', '2025-12-31', 22000);

INSERT INTO bookings (customer_id, room_id, tariff_id, check_in, check_out, total_price)
VALUES
(1, 2, 2, '2025-04-12', '2025-04-18', 150000),
(2, 3, 3, '2025-07-05', '2025-07-12', 105000),
(3, 4, 1, '2025-10-10', '2025-10-15', 110000);

INSERT INTO reviews (booking_id, rating, comment)
VALUES
(1, 5, 'Отличный сервис и чистые номера'),
(2, 4, 'Хорошее питание, но шумно ночью'),
(3, 5, 'Очень понравилось, приеду снова');
