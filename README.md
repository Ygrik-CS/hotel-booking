# Hotel Booking — Lab 1 (Functional, immutable core)

This repository contains a minimal implementation of **Lab 1** for the "Hotel booking" project.
It focuses on **pure functions**, **immutability**, and **HOFs** required for the first attestation.

Menu in Streamlit (app/main.py):
- Overview · Data · Functional Core

Main implemented functions (core/transforms.py):
- `load_seed(path: str)` -> (hotels, room_types, rates, prices, availability, guests)
- `hold_item(cart: tuple[CartItem,...], item: CartItem)` -> tuple[CartItem,...]
- `remove_hold(cart: tuple[CartItem,...], item_id: str)` -> tuple[CartItem,...]
- `nightly_sum(prices: tuple[Price,...], checkin: str, checkout: str, rate_id: str)` -> int (sum of amounts in cents)

Run locally:
```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
pytest -q
ruff check .
black --check .
```

Notes:
- Domain models are `@dataclass(frozen=True)` in `core/domain.py` to guarantee immutability.
- All collections are returned as tuples; functions do not mutate inputs and return new tuples.
- Tests are in `tests/` and cover the Lab #1 acceptance criteria (>=5 tests).


---
## Pull Request Template (Lab #1)

- **Что реализовано:**
  - Иммутабельные модели (core/domain.py)
  - Чистые функции load_seed, hold_item, remove_hold, nightly_sum (core/transforms.py)
  - Streamlit UI с меню: Overview, Data, Functional Core
  - Seed с отелями, номерами, тарифами, ценами, доступностью и гостями
  - ≥5 тестов (pytest, все зелёные)

- **Где нажимать в UI:**
  - Открыть `streamlit run app/main.py`
  - В боковом меню выбрать **Overview** → проверить агрегаты
  - Выбрать **Data** → увидеть примеры отелей и гостей
  - Выбрать **Functional Core** → посмотреть работу функции nightly_sum
