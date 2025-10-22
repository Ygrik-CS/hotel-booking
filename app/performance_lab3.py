import time
import random
from datetime import date
from functools import lru_cache

@lru_cache(maxsize=None)
def quote_offer(hotel_id, room_type, checkin, checkout, guests):
    base = {"Стандарт": 18000, "Люкс": 29000, "Семейный": 24000}
    tax, markup = 0.12, 0.05
    days = (date.fromisoformat(checkout) - date.fromisoformat(checkin)).days
    total = int(base.get(room_type, 18000) * days * (1 + tax + markup))
    available = room_type != "Люкс"    
    return total, available

runs = int(input("Введите количество запросов: "))

t1 = time.perf_counter()
for _ in range(runs):
    quote_offer(str(random.randint(1, 5)),
                random.choice(["Стандарт", "Люкс", "Семейный"]),
                "2025-10-01", "2025-10-05", random.randint(1, 4))
t2 = time.perf_counter()

t3 = time.perf_counter()
for _ in range(runs):
    quote_offer("1", "Стандарт", "2025-10-01", "2025-10-05", 2)
t4 = time.perf_counter()


print(f"Без кэша: {(t2 - t1)*1000:.2f} мс")
print(f"С кэшем:  {(t4 - t3)*1000:.2f} мс")
