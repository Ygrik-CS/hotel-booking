from datetime import datetime, timedelta
from typing import Tuple
from core.domain import RatePlan, Rule

def split_date_range(checkin: str, checkout: str) -> tuple[str, ...]:
    start = datetime.fromisoformat(checkin).date()
    end = datetime.fromisoformat(checkout).date()

    
    if start >= end:
        return ()
    
    
    next_date = start + timedelta(days=1)
    return (start.isoformat(),) + split_date_range(next_date.isoformat(), checkout)


def apply_rate_inheritance(rate: RatePlan, rules: tuple[Rule, ...]) -> RatePlan:

    if len(rules) == 0:
        return rate
    

    rule = rules[0]


    if rule.kind == "override_cancel_before":
        new_cancel_limit = rule.payload.get("cancel_before_days")
        

        if new_cancel_limit is not None:
            updated_rate = RatePlan(
                id=rate.id,
                hotel_id=rate.hotel_id,
                room_type_id=rate.room_type_id,
                title=rate.title,
                meal=rate.meal,
                refundable=rate.refundable,
                cancel_before_days=new_cancel_limit
            )
            rate = updated_rate
    return apply_rate_inheritance(rate, rules[1:])




def build_policy_tree(rate):
    days_left = rate.cancel_before_days

    if days_left <= 0:
        return ()
    
    return (
        {"days_before": days_left, "refundable": rate.refundable},
        build_policy_tree(RatePlan(
            id=rate.id,
            hotel_id=rate.hotel_id,
            room_type_id=rate.room_type_id,
            title=rate.title,
            meal=rate.meal,
            refundable=rate.refundable,
            cancel_before_days=days_left - 1
        ))
    )


