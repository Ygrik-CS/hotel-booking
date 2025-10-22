from core.filters import filter_city, filter_capacity, filter_features, filter_price
from core.recursion import split_date_range


# проверяем фильтр по городу
def test_filter_city():
    hotels = [{"city": "Almaty"}, {"city": "Astana"}]
    city_filter = filter_city("Almaty")  # создаём фильтр-замыкание
    result = list(filter(city_filter, hotels))  # применяем фильтр
    assert result == [{"city": "Almaty"}]  # остаётся только Алматы


# проверяем фильтр по вместимости
def test_filter_capacity():
    hotels = [{"capacity": 2}, {"capacity": 5}]
    capacity_filter = filter_capacity(4)  # минимум 4 места
    result = list(filter(capacity_filter, hotels))
    assert result == [{"capacity": 5}]  # подходит только номер на 5 человек


# проверяем фильтр по фичам
def test_filter_features():
    hotels = [{"features": ["wifi", "pool"]}]
    feature_filter = filter_features(["wifi"])  # ищем где есть WiFi
    result = list(filter(feature_filter, hotels))
    assert len(result) == 1  # отель подходит


# проверяем фильтр по цене
def test_filter_price():
    hotels = [
        {"price": 200, "currency": "USD"},
        {"price": 80, "currency": "USD"},
    ]
    price_filter = filter_price(100, 300, "USD")  # фильтр по диапазону
    result = list(filter(price_filter, hotels))
    assert result == [{"price": 200, "currency": "USD"}]  # остаётся отель с 200 USD


# проверяем рекурсивную функцию split_date_range
def test_split_date_range():
    dates = split_date_range("2025-10-01", "2025-10-03")
    assert dates == ("2025-10-01", "2025-10-02")  # две ночи: 1 и 2 октября
