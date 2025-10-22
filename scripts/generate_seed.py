from datetime import date, timedelta
import json
import random

# Список отелей (5 штук в разных городах)
hotels = [
    {"id": "h1", "name": "Hotel 1", "city": "Almaty", "stars": 3.9},
    {"id": "h2", "name": "Hotel 2", "city": "Aktau", "stars": 5},
    {"id": "h3", "name": "Hotel 3", "city": "Astana", "stars": 3.7},
    {"id": "h4", "name": "Hotel 4", "city": "Astana", "stars": 4.9},
    {"id": "h5", "name": "Hotel 5", "city": "Almaty", "stars": 4.1},
]

# Списки куда будем собирать данные
room_types = []  # типы номеров
rates = []  # тарифы
prices = []  # цены
availability = []  # доступность номеров

# Начальная дата для генерации цен и доступности
start_date = date(2025, 10, 1)
days_count = 60  # создаём данные на 60 дней

room_type_counter = 1
rate_counter = 1

# Проходим по каждому отелю
for hotel in hotels:
    # в каждом отеле создаём по 4 типа номеров
    for j in range(4):
        room_type_id = f"room_type{room_type_counter}"
        room_types.append(
            {"id": room_type_id, "hotel_id": hotel["id"], "name": f"Type-{j + 1}"}
        )

        # для каждого типа номера создаём 3 тарифа
        for tariff in ["Standard", "Non-refundable", "Breakfast included"]:
            rate_id = f"rate-{rate_counter}"
            rates.append({"id": rate_id, "room_type_id": room_type_id, "name": tariff})

            # генерируем цены на 60 дней вперёд
            for day in range(days_count):
                current_date = start_date + timedelta(days=day)
                price = random.randint(10000, 30000)  # рандомная цена
                prices.append(
                    {
                        "rate_id": rate_id,
                        "date": current_date.isoformat(),
                        "price": price,
                    }
                )

            rate_counter += 1
        room_type_counter += 1

# Генерация доступности для каждого типа комнаты на каждый день
for room_type in room_types:
    for day in range(days_count):
        current_date = start_date + timedelta(days=day)
        availability.append(
            {
                "room_type_id": room_type["id"],
                "date": current_date.isoformat(),
                "available": random.randint(1, 10),  # от 1 до 10 свободных номеров
            }
        )

# Создаём список гостей (50 человек)
guests = []
for i in range(1, 51):
    guest = {"id": "guest_" + str(i), "name": "Guest_№" + str(i)}
    guests.append(guest)

# Собираем всё в одну структуру
seed = {
    "hotels": hotels,
    "room_types": room_types,
    "rates": rates,
    "prices": prices,
    "availability": availability,
    "guests": guests,
}

# Сохраняем всё в JSON файл
with open("./data/seed.json", "w", encoding="utf-8") as f:
    json.dump(seed, f, indent=4)

print("seed.json создан!")  # проверка
