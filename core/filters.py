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
        cap = h.get("capacity")
        if cap >= min_guests:
            return True
        else:
            return False
    return enough_space



def filter_features(required):
    def check_features(hotel):
        features = hotel.get("features")
        for item in required:
            if item not in features:
                return False
        return True
    return check_features



def filter_price(min_price, max_price, currency):
    def check_price(hotel):
        hotel_currency = hotel.get("currency")
        price = hotel.get("price")

        if hotel_currency != currency:
            return False

        if price < min_price:
            return False

        if price > max_price:
            return False

        return True
    return check_price\
    






#hotels = [
#    {"city": "New York", "capacity": 2, "features": ["WiFi"], "price": 100, "currency": "USD"},
#    {"city": "Paris", "capacity": 4, "features": ["Pool"], "price": 150, "currency": "EUR"}
#]

#city_filter = filter_city("New York")
#capacity_filter = filter_capacity(2)
#features_filter = filter_features(["WiFi"])
#price_filter = filter_price(50, 200, "USD")

#filtered = [h for h in hotels if city_filter(h) and capacity_filter(h) and features_filter(h) and price_filter(h)] 