# фильтр по городу - возвращает функцию, которая проверяет, находится ли отель в нужном городе
def filter_city(city_name: str):
    # внутренняя функция (замыкание) - проверяет каждый отель
    def in_city(h):
        city = h.get("city")
        # если у отеля нет города - сразу False
        if city is None:
            return False
        # если город совпадает с нужным - True
        if city == city_name:
            return True
        else:
            return False

    # возвращаем саму функцию - она будет использовать city_name из замыкания
    return in_city


# фильтр по вместимости - проверяет, влезает ли нужное количество гостей
def filter_capacity(min_guests: int):
    def enough_space(h):
        cap = h.get("capacity")
        # если в номере мест >= нужного количества - подходит
        if cap >= min_guests:
            return True
        else:
            return False

    return enough_space


# фильтр по удобствам - проверяет, есть ли все нужные фичи
def filter_features(required):
    def check_features(hotel):
        features = hotel.get("features")
        # идём по списку нужных удобств и проверяем, что каждое есть в отеле
        for item in required:
            if item not in features:
                return False
        # если все нашли - True
        return True

    return check_features


# фильтр по цене - проверяет входит ли цена в нужный диапазон и совпадает ли валюта
def filter_price(min_price, max_price, currency):
    def check_price(hotel):
        hotel_currency = hotel.get("currency")
        price = hotel.get("price")

        # если валюта не совпадает - не подходит
        if hotel_currency != currency:
            return False

        # если цена меньше минимума - не подходит
        if price < min_price:
            return False

        # если цена больше максимума - не подходит
        if price > max_price:
            return False

        # если все проверки прошли - отель ок
        return True

    return check_price


# Пример использования:


# hotels = [
#    {"city": "New York", "capacity": 2, "features": ["WiFi"], "price": 100, "currency": "USD"},
#    {"city": "Paris", "capacity": 4, "features": ["Pool"], "price": 150, "currency": "EUR"}
# ]

# city_filter = filter_city("New York")
# capacity_filter = filter_capacity(2)
# features_filter = filter_features(["WiFi"])
# price_filter = filter_price(50, 200, "USD")

# filtered = [h for h in hotels if city_filter(h) and capacity_filter(h) and features_filter(h) and price_filter(h)]
