from pathlib import Path

from app.parser import parse_products


HTML_FILE = Path("fixtures/golden/multi_product.html")


def test_parse_multiple_products():

    html = HTML_FILE.read_text(
        encoding="utf-8"
    )

    selectors = {
        "version": 1,
        "fields": {
            "name": ".product-name",
            "price": ".price",
        },
    }

    products = parse_products(
        html,
        selectors=selectors,
    )

    assert len(products) == 3

    assert products[0]["name"] == "Full Cream Milk"
    assert products[0]["price"] == "$4.50"

    assert products[1]["name"] == "Toned Milk"
    assert products[1]["price"] == "$3.80"

    assert products[2]["name"] == "Organic Milk"
    assert products[2]["price"] == "$5.20"