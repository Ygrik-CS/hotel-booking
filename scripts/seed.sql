DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS room_types;
DROP TABLE IF EXISTS rate_plans;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS availability;
DROP TABLE IF EXISTS guests;
DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS rules;

CREATE TABLE hotels (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    stars REAL NOT NULL
);

CREATE TABLE room_types (
    id TEXT PRIMARY KEY,
    hotel_id TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id)
);

CREATE TABLE rate_plans (
    id TEXT PRIMARY KEY,
    room_type_id TEXT NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
);

CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rate_id TEXT NOT NULL,
    date TEXT NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (rate_id) REFERENCES rate_plans(id)
);

CREATE TABLE availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_id TEXT NOT NULL,
    date TEXT NOT NULL,
    available INTEGER NOT NULL,
    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
);

CREATE TABLE guests (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);

CREATE TABLE cart_items (
    id TEXT PRIMARY KEY,
    hotel_id TEXT,
    room_type_id TEXT,
    rate_id TEXT,
    checkin TEXT,
    checkout TEXT,
    guests INTEGER
);

CREATE TABLE bookings (
    id TEXT PRIMARY KEY,
    guest_id TEXT,
    total INTEGER,
    status TEXT,
    FOREIGN KEY (guest_id) REFERENCES guests(id)
);

CREATE TABLE payments (
    id TEXT PRIMARY KEY,
    booking_id TEXT,
    amount INTEGER,
    ts TEXT,
    method TEXT,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

CREATE TABLE events (
    id TEXT PRIMARY KEY,
    ts TEXT,
    name TEXT,
    payload TEXT
);

CREATE TABLE rules (
    id TEXT PRIMARY KEY,
    kind TEXT,
    payload TEXT
);

INSERT INTO hotels VALUES
('h1','Hotel 1','Almaty',3.9),
('h2','Hotel 2','Aktau',5.0),
('h3','Hotel 3','Astana',3.7),
('h4','Hotel 4','Astana',4.9),
('h5','Hotel 5','Almaty',4.1);

INSERT INTO room_types VALUES
('room_type1','h1','Type-1'),
('room_type2','h1','Type-2'),
('room_type3','h1','Type-3'),
('room_type4','h1','Type-4'),
('room_type5','h2','Type-1'),
('room_type6','h2','Type-2'),
('room_type7','h2','Type-3'),
('room_type8','h2','Type-4'),
('room_type9','h3','Type-1'),
('room_type10','h3','Type-2'),
('room_type11','h3','Type-3'),
('room_type12','h3','Type-4'),
('room_type13','h4','Type-1'),
('room_type14','h4','Type-2'),
('room_type15','h4','Type-3'),
('room_type16','h4','Type-4'),
('room_type17','h5','Type-1'),
('room_type18','h5','Type-2'),
('room_type19','h5','Type-3'),
('room_type20','h5','Type-4');

INSERT INTO rate_plans VALUES
('rate-1','room_type1','Standard'),
('rate-2','room_type1','Non-refundable'),
('rate-3','room_type1','Breakfast included'),
('rate-4','room_type2','Standard'),
('rate-5','room_type2','Non-refundable'),
('rate-6','room_type2','Breakfast included'),
('rate-7','room_type3','Standard'),
('rate-8','room_type3','Non-refundable'),
('rate-9','room_type3','Breakfast included'),
('rate-10','room_type4','Standard'),
('rate-11','room_type4','Non-refundable'),
('rate-12','room_type4','Breakfast included');



INSERT INTO guests VALUES
('guest_1','Guest_№1',NULL),
('guest_2','Guest_№2',NULL),
('guest_3','Guest_№3',NULL),
('guest_4','Guest_№4',NULL),
('guest_5','Guest_№5',NULL);
