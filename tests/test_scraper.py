from pathlib import Path

from app.scraper import fetch_html


HTML_FILE = Path(
    "fixtures/golden/multi_product.html"
)


def test_fetch_html():
    html = fetch_html(HTML_FILE)

    assert "<html>" in html
    assert "Full Cream Milk" in html