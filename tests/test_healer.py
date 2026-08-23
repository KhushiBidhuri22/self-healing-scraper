from app.healer import heal_selector


def test_healer_finds_and_promotes_replacement(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.selector_promoter.SELECTOR_DIRECTORY",
        tmp_path,
    )

    html = """
    <html>
        <body>
            <h2 class="title">Full Cream Milk</h2>
        </body>
    </html>
    """

    current_selectors = {
        "version": 1,
        "fields": {
            "name": ".product-name",
            "price": ".price",
        },
    }

    result = heal_selector(
        html,
        "name",
        "Full Cream Milk",
        current_selectors,
    )

    assert result["healed"] is True
    assert result["old_selector"] == ".product-name"
    assert result["new_selector"] in [
        ".title",
        "h2.title",
    ]
    assert result["score"] >= 90
    assert result["new_version"] == 2