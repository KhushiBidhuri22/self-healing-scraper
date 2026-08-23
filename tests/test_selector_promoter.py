from pathlib import Path

from app.selector_promoter import promote_selector


def test_promote_selector(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.selector_promoter.SELECTOR_DIRECTORY",
        tmp_path,
    )

    current = {
        "version": 1,
        "fields": {
            "name": ".product-name",
            "price": ".price",
        },
    }

    result = promote_selector(
        current,
        "name",
        "h2.title",
    )

    assert result["version"] == 2
    assert result["fields"]["name"] == "h2.title"
    assert result["fields"]["price"] == ".price"

    version_file = Path(tmp_path) / "v2.json"

    assert version_file.exists()