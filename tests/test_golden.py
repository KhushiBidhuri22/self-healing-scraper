from app.golden import load_golden


def test_load_golden():
    golden = load_golden()
    assert golden["name"] == "Full Cream Milk"
    assert golden["price"] == "$4.50"

from app.golden import (
    load_golden,
    load_golden_products,
)


def test_load_golden():
    golden = load_golden()

    assert golden["name"] == "Full Cream Milk"
    assert golden["price"] == "$4.50"


def test_load_golden_products():

    golden = load_golden_products()

    assert len(golden) == 3

    assert golden[0]["name"] == "Full Cream Milk"
    assert golden[0]["price"] == "$4.50"

    assert golden[1]["name"] == "Toned Milk"
    assert golden[1]["price"] == "$3.80"

    assert golden[2]["name"] == "Organic Milk"
    assert golden[2]["price"] == "$5.20"