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