from core.ftypes import Maybe, Either
from core.transforms import safe_rate, validate_cart_item, validate_booking
from core.report import check_and_quote_booking

class Dummy:
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

def test_maybe_either_basic():
    m = Maybe.some(2).map(lambda x: x * 2)
    assert m.get_or_else(0) == 4
    e = Either.right(3).map(lambda x: x + 1)
    assert e.get_or_else(0) == 4

def test_safe_rate_found():
    rates = (Dummy(id="r1"),)
    assert safe_rate(rates, "r1").is_some()
    assert safe_rate(rates, "r2").is_none()

def test_validate_cart_item_ok():
    item = Dummy(checkin="2025-10-01", checkout="2025-10-05")
    res = validate_cart_item(item, ())
    assert res.is_right()

def test_validate_cart_item_fail():
    item = Dummy()
    res = validate_cart_item(item, ())
    assert res.is_left()

def test_validate_booking_and_report():
    item = Dummy(checkin="2025-10-01", checkout="2025-10-05")
    booking = Dummy(items=(item,))
    assert validate_booking(booking).is_right()
    assert check_and_quote_booking(booking, (), ()).is_right()