from datetime import date, timedelta
import random
import os

os.makedirs("../data", exist_ok=True)

sql = []

sql.append("""
DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS room_types;
DROP TABLE IF EXISTS rate_plans;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS availability;
DROP TABLE IF EXISTS guests;

CREATE TABLE hotels (
    id TEXT PRIMARY KEY,
    name TEXT,
    city TEXT,
    stars REAL
);

CREATE TABLE room_types (
    id TEXT PRIMARY KEY,
    hotel_id TEXT,
    name TEXT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id)
);

CREATE TABLE rate_plans (
    id TEXT PRIMARY KEY,
    room_type_id TEXT,
    name TEXT,
    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
);

CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rate_id TEXT,
    date TEXT,
    price INTEGER,
    FOREIGN KEY (rate_id) REFERENCES rate_plans(id)
);

CREATE TABLE availability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type_id TEXT,
    date TEXT,
    available INTEGER,
    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
);

CREATE TABLE guests (
    id TEXT PRIMARY KEY,
    name TEXT
);
""")

hotels = [
    {"id": "h1", "name": "Hotel 1", "city": "Almaty", "stars": 3.9},
    {"id": "h2", "name": "Hotel 2", "city": "Aktau", "stars": 5.0},
    {"id": "h3", "name": "Hotel 3", "city": "Astana", "stars": 3.7},
    {"id": "h4", "name": "Hotel 4", "city": "Astana", "stars": 4.9},
    {"id": "h5", "name": "Hotel 5", "city": "Almaty", "stars": 4.1},
]

sql.append("INSERT INTO hotels (id, name, city, stars) VALUES")
sql.append(",\n".join([f"('{h['id']}', '{h['name']}', '{h['city']}', {h['stars']})" for h in hotels]) + ";")

room_types = []
rates = []
prices = []
availability = []

start_date = date(2025, 10, 1)
days_count = 60

room_type_counter = 1
rate_counter = 1

for hotel in hotels:
    for j in range(4):
        rt_id = f"room_type{room_type_counter}"
        room_types.append((rt_id, hotel["id"], f"Type-{j+1}"))

        for tariff in ["Standard", "Non-refundable", "Breakfast included"]:
            rate_id = f"rate-{rate_counter}"
            rates.append((rate_id, rt_id, tariff))

            for day in range(days_count):
                d = start_date + timedelta(days=day)
                prices.append((rate_id, d.isoformat(), random.randint(10000, 30000)))

            rate_counter += 1
        room_type_counter += 1

for rt in room_types:
    for day in range(days_count):
        d = start_date + timedelta(days=day)
        availability.append((rt[0], d.isoformat(), random.randint(1, 10)))

sql.append("INSERT INTO room_types (id, hotel_id, name) VALUES")
sql.append(",\n".join([f"('{r[0]}', '{r[1]}', '{r[2]}')" for r in room_types]) + ";")

sql.append("INSERT INTO rate_plans (id, room_type_id, name) VALUES")
sql.append(",\n".join([f"('{r[0]}', '{r[1]}', '{r[2]}')" for r in rates]) + ";")

sql.append("INSERT INTO prices (rate_id, date, price) VALUES")
sql.append(",\n".join([f"('{p[0]}', '{p[1]}', {p[2]})" for p in prices]) + ";")

sql.append("INSERT INTO availability (room_type_id, date, available) VALUES")
sql.append(",\n".join([f"('{a[0]}', '{a[1]}', {a[2]})" for a in availability]) + ";")

guests = [(f"guest_{i}", f"Guest_{i}") for i in range(1, 51)]

sql.append("INSERT INTO guests (id, name) VALUES")
sql.append(",\n".join([f"('{g[0]}', '{g[1]}')" for g in guests]) + ";")

path = "../data/seed.sql"
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(sql))

print(f"✅ SQL seed file generated successfully at {path}")
