from app.parser import parse_product


def test_parse_product():
    html = """
    <html>
        <body>
            <div class="product">
                <h2 class="product-name">Full Cream Milk</h2>
                <span class="price">$4.50</span>
            </div>
        </body>
    </html>
    """

    result = parse_product(html)

    assert result["name"] == "Full Cream Milk"
    assert result["price"] == "$4.50"
    assert result["selector_version"] == 1