from chaos import rename_product_name_class


def test_rename_product_name_class():
    html = """
    <html>
        <body>
            <h2 class="product-name">Full Cream Milk</h2>
        </body>
    </html>
    """

    mutated_html = rename_product_name_class(html)

    assert 'class="title"' in mutated_html
    assert "Full Cream Milk" in mutated_html

from chaos import add_extra_wrapper


def test_add_extra_wrapper():
    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <span class="price">$4.50</span>
    </div>
    """

    mutated = add_extra_wrapper(html)

    assert 'class="extra-wrapper"' in mutated
    assert "Full Cream Milk" in mutated
    assert "$4.50" in mutated

from chaos import reorder_product_children


def test_reorder_product_children():
    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <span class="price">$4.50</span>
    </div>
    """

    mutated = reorder_product_children(html)

    name_position = mutated.index("Full Cream Milk")
    price_position = mutated.index("$4.50")

    assert price_position < name_position

from chaos import change_price_format


def test_change_price_format():
    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <span class="price">$4.50</span>
    </div>
    """

    mutated = change_price_format(html)

    assert "4,50 USD" in mutated
    assert "$4.50" not in mutated

from chaos import drop_attributes


def test_drop_attributes():
    html = """
    <div class="product">
        <h2
            class="product-name"
            id="milk-name"
            data-testid="product-name"
        >
            Full Cream Milk
        </h2>

        <span
            class="price"
            id="milk-price"
            data-testid="price"
        >
            $4.50
        </span>
    </div>
    """

    mutated = drop_attributes(html)

    assert "data-testid" not in mutated
    assert 'id="milk-name"' not in mutated
    assert 'id="milk-price"' not in mutated

    assert "product-name" in mutated
    assert "price" in mutated

from chaos import lazy_load_product


def test_lazy_load_product():
    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <span class="price">$4.50</span>
    </div>
    """

    mutated = lazy_load_product(html)

    assert "Full Cream Milk" not in mutated
    assert "$4.50" not in mutated
    assert "Loading..." in mutated

from chaos import remove_price_element


def test_remove_price_element():
    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <span class="price">$4.50</span>
    </div>
    """

    mutated = remove_price_element(html)

    assert "$4.50" not in mutated
    assert 'class="price"' not in mutated
    assert "Full Cream Milk" in mutated