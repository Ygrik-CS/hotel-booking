from core.filters import filter_city, filter_capacity, filter_features, filter_price
from core.recursion import split_date_range
from core.domain import RatePlan, Rule

def test_filter_city():
    hotels = [{"city": "Almaty"}, {"city": "Astana"}]
    city_filter = filter_city("Almaty")
    result = list(filter(city_filter, hotels))
    assert result == [{"city": "Almaty"}]

def test_filter_capacity():
    hotels = [{"capacity": 2}, {"capacity": 5}]
    capacity_filter = filter_capacity(4)
    result = list(filter(capacity_filter, hotels))
    assert result == [{"capacity": 5}]

def test_filter_features():
    hotels = [{"features": ["wifi", "pool"]}]
    feature_filter = filter_features(["wifi"])
    result = list(filter(feature_filter, hotels))
    assert len(result) == 1

def test_filter_price():
    hotels = [
        {"price": 200, "currency": "USD"},
        {"price": 80, "currency": "USD"},
    ]
    price_filter = filter_price(100, 300, "USD")
    result = list(filter(price_filter, hotels))
    assert result == [{"price": 200, "currency": "USD"}]

def test_split_date_range():
    dates = split_date_range("2025-10-01", "2025-10-03")
    assert dates == ("2025-10-01", "2025-10-02")