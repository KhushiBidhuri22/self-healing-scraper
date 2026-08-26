import re
from collections.abc import Sequence


NULL_THRESHOLD = 0.20
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 200


def null_rate(values: Sequence[object]) -> float:
    if not values:
        return 1.0

    missing = sum(value is None for value in values)

    return missing / len(values)


def invalid_name(value: object) -> bool:
    if value is None:
        return True

    if not isinstance(value, str):
        return True

    length = len(value.strip())

    return length < MIN_NAME_LENGTH or length > MAX_NAME_LENGTH


def invalid_price(value: object) -> bool:
    if value is None:
        return True

    if not isinstance(value, str):
        return True

    cleaned = value.strip().upper()

    cleaned = cleaned.replace("$", "")
    cleaned = cleaned.replace("USD", "")
    cleaned = cleaned.strip()

    if "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")

    else:
        cleaned = cleaned.replace(",", "")

    try:
        price = float(cleaned)
    except ValueError:
        return True

    return price <= 0 or price > 10000

def detect_drift(records: list[dict]) -> dict:
    if not records:
        return {
            "drift": True,
            "reason": "No records were produced",
        }

    names = [record.get("name") for record in records]
    prices = [record.get("price") for record in records]

    name_null_rate = null_rate(names)
    price_null_rate = null_rate(prices)

    invalid_name_count = sum(invalid_name(name) for name in names)
    invalid_price_count = sum(invalid_price(price) for price in prices)

    name_invalid_rate = invalid_name_count / len(names)
    price_invalid_rate = invalid_price_count / len(prices)

    drift_fields = []

    if name_null_rate > NULL_THRESHOLD:
        drift_fields.append("name")

    if name_invalid_rate > NULL_THRESHOLD:
        if "name" not in drift_fields:
            drift_fields.append("name")

    if price_null_rate > NULL_THRESHOLD:
        drift_fields.append("price")

    if price_invalid_rate > NULL_THRESHOLD:
        if "price" not in drift_fields:
            drift_fields.append("price")

    return {
        "drift": bool(drift_fields),
        "fields": drift_fields,
        "name_null_rate": name_null_rate,
        "price_null_rate": price_null_rate,
        "name_invalid_rate": name_invalid_rate,
        "price_invalid_rate": price_invalid_rate,
    }