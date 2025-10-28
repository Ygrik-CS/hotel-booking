from core.lazy import lazy_offers, load_data
def test_price_filter():
    hotels, rooms, rates, prices = load_data()
    offers = list(lazy_offers(hotels, rooms, rates, prices, None, lambda o: o[3] > 20000))
    assert all(price > 20000 for _, _, _, price in offers)

def test_star_filter():
    hotels, rooms, rates, prices = load_data()
    offers = list(lazy_offers(hotels, rooms, rates, prices, None, lambda o: o[0]['stars'] == 5))
    assert all(h['stars'] == 5 for h, _, _, _ in offers)

def test_yield_type():
    hotels, rooms, rates, prices = load_data()
    offers = lazy_offers(hotels, rooms, rates, prices, None, lambda o: True)
    assert hasattr(offers, '__iter__')

def test_limit_output():
    hotels, rooms, rates, prices = load_data()
    offers = lazy_offers(hotels, rooms, rates, prices, None, lambda o: True)
    k = 2
    limited = [next(offers) for _ in range(k)]
    assert len(limited) == k

def test_combined_filter():
    hotels, rooms, rates, prices = load_data()
    offers = list(lazy_offers(hotels, rooms, rates, prices, None, lambda o: o[0]['stars'] >= 4 and o[3] < 25000))
    for h, _, _, p in offers:
        assert h['stars'] >= 4 and p < 25000
