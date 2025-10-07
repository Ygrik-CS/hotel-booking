def filter_city(city_name: str):
    def in_city(h):
        city = h.get("city")
        if city is None:
            return False
        if city == city_name:
            return True
        else:
            return False
    return in_city



def filter_capacity(min_guests: int):
    def enough_space(h):
        cap = h.get("capacity", 0)
        if cap >= min_guests:
            return True
        else:
            return False
    return enough_space



def filter_features(required):
    def check_features(hotel):
        features = hotel.get("features", [])
        for item in required:
            if item not in features:
                return False
        return True
    return check_features



def filter_price(min_price, max_price, currency):
    def check_price(hotel):
        hotel_currency = hotel.get("currency", "")
        price = hotel.get("price", 0)

        if hotel_currency != currency:
            return False

        if price < min_price:
            return False

        if price > max_price:
            return False

        return True
    return check_price