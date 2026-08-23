from bs4 import BeautifulSoup

from app.selector_registry import load_selectors


def parse_product(
    html: str,
    selectors: dict | None = None,
) -> dict:
    soup = BeautifulSoup(html, "lxml")

    if selectors is None:
        selectors = load_selectors()

    name_selector = selectors["fields"]["name"]
    price_selector = selectors["fields"]["price"]

    name_element = soup.select_one(name_selector)
    price_element = soup.select_one(price_selector)

    return {
        "name": name_element.get_text(strip=True) if name_element else None,
        "price": price_element.get_text(strip=True) if price_element else None,
        "selector_version": selectors["version"],
    }