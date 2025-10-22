from core.domain import Guest, Price, Availability, CartItem
from core.transforms import hold_item, remove_hold


# проверяем, что объект Guest создаётся правильно
def test_guest():
    g = Guest(id="g1", name="Alice", email="alice228@mail.com")
    # тут проверяем поля: айди и имя должны совпадать
    assert g.id == "g1"
    assert g.name == "Alice"


# проверяем что Price создаётся правильно и хранит нужные данные
def test_price():
    p = Price(id="p1", rate_id="rate1", date="2025-10-01", amount=5000, currency="KZT")
    # главное - чтобы цена записалась как число и совпала
    assert p.amount == 5000


# проверяем что Availability хранит количество доступных номеров
def test_availability():
    a = Availability(id="av1", room_type_id="r1", date="2025-10-01", available=3)
    # доступность должна быть 3
    assert a.available == 3


# тестируем добавление в корзину - hold_item не должен ломать неизменяемость
def test_hold_item():
    cart = tuple()  # пустая корзина
    item = CartItem(
        id="c1",
        hotel_id="h1",
        room_type_id="r1",
        rate_id="rate1",
        checkin="2025-10-01",
        checkout="2025-10-02",
        guests=2,
    )
    new_cart = hold_item(cart, item)
    # должно появиться ровно одно бронирование
    assert len(new_cart) == 1


# тестируем удаление из корзины - remove_hold должен вернуть новую корзину без элемента
def test_remove_hold():
    item1 = CartItem(
        id="c1",
        hotel_id="h1",
        room_type_id="r1",
        rate_id="rate1",
        checkin="2025-10-01",
        checkout="2025-10-02",
        guests=2,
    )
    item2 = CartItem(
        id="c2",
        hotel_id="h2",
        room_type_id="r2",
        rate_id="rate2",
        checkin="2025-10-03",
        checkout="2025-10-04",
        guests=1,
    )
    cart = (item1, item2)

    # удаляем первый элемент
    new_cart = remove_hold(cart, "c1")

    # после удаления должен остаться только второй
    assert len(new_cart) == 1
    assert new_cart[0].id == "c2"
