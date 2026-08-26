from app.validator import detect_drift, invalid_price
from app.validator import (
    detect_drift,
    invalid_price,
)


def test_healthy_data_has_no_drift():
    records = [
        {"name": "Milk", "price": "$4.50"},
        {"name": "Bread", "price": "$3.20"},
        {"name": "Butter", "price": "$5.00"},
        {"name": "Eggs", "price": "$6.00"},
        {"name": "Cheese", "price": "$7.50"},
    ]

    result = detect_drift(records)

    assert result["drift"] is False


def test_missing_names_trigger_drift():
    records = [
        {"name": None, "price": "$4.50"},
        {"name": None, "price": "$3.20"},
        {"name": None, "price": "$5.00"},
        {"name": "Eggs", "price": "$6.00"},
        {"name": "Cheese", "price": "$7.50"},
    ]

    result = detect_drift(records)

    assert result["drift"] is True
    assert "name" in result["fields"]


def test_invalid_name_triggers_drift():
    records = [
        {"name": "", "price": "$4.50"},
        {"name": "", "price": "$3.20"},
        {"name": "", "price": "$5.00"},
        {"name": "Eggs", "price": "$6.00"},
        {"name": "Cheese", "price": "$7.50"},
    ]

    result = detect_drift(records)

    assert result["drift"] is True
    assert "name" in result["fields"]


def test_invalid_price_triggers_drift():
    records = [
        {"name": "Milk", "price": "hello"},
        {"name": "Bread", "price": "hello"},
        {"name": "Butter", "price": "hello"},
        {"name": "Eggs", "price": "$6.00"},
        {"name": "Cheese", "price": "$7.50"},
    ]

    result = detect_drift(records)

    assert result["drift"] is True
    assert "price" in result["fields"]

def test_price_with_comma_decimal_is_valid():
    assert invalid_price("4,50 USD") is False


def test_price_with_dollar_is_valid():
    assert invalid_price("$4.50") is False


def test_price_with_thousands_separator_is_valid():
    assert invalid_price("1,250.50") is False