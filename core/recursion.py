from datetime import datetime, timedelta
from core.domain import RatePlan, Rule

def split_date_range(checkin: str, checkout: str) -> tuple[str, ...]:
    d1 = datetime.strptime(checkin, "%Y-%m-%d")
    d2 = datetime.strptime(checkout, "%Y-%m-%d")

    if d1 >= d2:
        return ()

    one_day = d1.strftime("%Y-%m-%d")
    next_day = (d1 + timedelta(days=1)).strftime("%Y-%m-%d")

    return (one_day,) + split_date_range(next_day, checkout)


def apply_rate_inheritance(rate: RatePlan, rules: tuple[Rule, ...]) -> RatePlan:
    if not rules:
        return rate

    rule = rules[0]

    if rule.kind == "refundable":
        if "refundable" in rule.payload:
            rate = RatePlan(
                id=rate.id,
                hotel_id=rate.hotel_id,
                room_type_id=rate.room_type_id,
                title=rate.title,
                meal=rate.meal,
                refundable=rule.payload["refundable"],
                cancel_before_days=rate.cancel_before_days
            )

    elif rule.kind == "cancel_before":
        if "days" in rule.payload:
            rate = RatePlan(
                id=rate.id,
                hotel_id=rate.hotel_id,
                room_type_id=rate.room_type_id,
                title=rate.title,
                meal=rate.meal,
                refundable=rate.refundable,
                cancel_before_days=rule.payload["days"]
            )

    return apply_rate_inheritance(rate, rules[1:])
