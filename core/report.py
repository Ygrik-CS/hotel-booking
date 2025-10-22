from core.ftypes import Either
from core.transforms import validate_booking

def check_and_quote_booking(booking, prices, availability, rules=(), rates=(), room_types=()):
    res = validate_booking(booking, prices, availability, rules, rates, room_types)
    if res.is_left():
        return res
    # просто возвращаем фиктивную сумму
    return Either.right({"booking": booking, "calc_total": 12345})
