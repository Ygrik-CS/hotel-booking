from datetime import datetime, timedelta
from typing import Tuple, Optional
from core.domain import RatePlan, Rule, Price, Availability  # noqa: F401


# Функция делит диапазон дат на отдельные ночи
# используется рекурсия — функция вызывает саму себя, пока не дойдёт до конца диапазона
def split_date_range(checkin: str, checkout: str) -> Tuple[str, ...]:
    # перевожу даты из строкового формата (например "2025-10-01") в объект date
    start = datetime.fromisoformat(checkin).date()
    end = datetime.fromisoformat(checkout).date()

    # если заезд равен или позже выезда — база рекурсии (функция больше не вызывает себя)
    if start >= end:
        return ()

    # считаю следующий день
    next_day = start + timedelta(days=1)

    # возвращаю кортеж: текущая дата + результат следующего рекурсивного вызова
    # то есть функция вызывает саму себя для оставшихся дней
    return (start.isoformat(),) + split_date_range(next_day.isoformat(), checkout)


# Эта функция показывает рекурсию по списку — мы применяем правила одно за другим
def apply_rate_inheritance(rate: RatePlan, rules: Tuple[Rule, ...]) -> RatePlan:
    # если список правил пустой — это базовый случай (дальше не идём)
    if not rules:
        return rate

    # беру первое правило из списка
    rule = rules[0]

    # если правило про "override_cancel_before" — меняем срок отмены
    if rule.kind == "override_cancel_before":
        # беру новое значение из payload (например {"cancel_before_days": 3})
        new_cancel_days: Optional[int] = rule.payload.get("cancel_before_days")

        # если значение есть — создаю новый тариф с обновлённым полем
        # именно создаю новый тпотому что всё иммутабельно
        if new_cancel_days is not None:
            rate = RatePlan(
                id=rate.id,
                hotel_id=rate.hotel_id,
                room_type_id=rate.room_type_id,
                title=rate.title,
                meal=rate.meal,
                refundable=rate.refundable,
                cancel_before_days=new_cancel_days,
            )

    # после применения первого правила вызываю функцию снова,
    # но теперь передаю другие правила (rules[1:])
    # это и есть рекурсия — функция обрабатывает каждый элемент по одному
    return apply_rate_inheritance(rate, rules[1:])


# Эта функция строит дерево - показывает, сколько дней до заезда можно отменять
#  уменьшает счётчик каждый раз
def build_policy_tree(rate: RatePlan) -> Tuple[dict, ...]:
    # если cancel_before_days нет — считаем как 0, чтобы не упасть с ошибкой
    days_left = rate.cancel_before_days if rate.cancel_before_days is not None else 0

    # если значение отрицательное - сразу возвращаем пусто
    if days_left < 0:
        return ()

    # когда осталось 0 дней - возвращаем запись и выходим из рекурсии
    if days_left == 0:
        return ({"days_before": 0, "refundable": rate.refundable},)

    # создаю словарь с текущим состоянием - сколько дней осталось и можно ли отменить
    current = {"days_before": days_left, "refundable": rate.refundable}

    # создаю новый тариф но с уменьшенным числом дней
    # это нужно чтобы передать его в следующий рекурсивный вызов
    smaller = RatePlan(
        id=rate.id,
        hotel_id=rate.hotel_id,
        room_type_id=rate.room_type_id,
        title=rate.title,
        meal=rate.meal,
        refundable=rate.refundable,
        cancel_before_days=days_left - 1,
    )

    # возвращаю кортеж: текущий уровень + рекурсивный вызов для оставшихся дней
    # в итоге получится цепочка: (3,2,1,0)...
    return (current,) + build_policy_tree(smaller)







