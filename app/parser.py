from bs4 import BeautifulSoup

from app.selector_registry import load_selectors


def parse_product(
    html: str,
    selectors: dict | None = None,
) -> dict:
    """
    Parse the first product from the HTML.

    Kept for backward compatibility with the existing
    tests and single-product workflow.
    """
    products = parse_products(html, selectors)

    if not products:
        return {
            "name": None,
            "price": None,
            "selector_version": (
                selectors["version"]
                if selectors
                else load_selectors()["version"]
            ),
        }

    return products[0]


def parse_products(
    html: str,
    selectors: dict | None = None,
) -> list[dict]:
    """
    Parse all products from the HTML.
    """

    soup = BeautifulSoup(html, "lxml")

    if selectors is None:
        selectors = load_selectors()

    name_selector = selectors["fields"]["name"]
    price_selector = selectors["fields"]["price"]

    products = []

    product_elements = soup.select(".product")

    # If the page doesn't contain product containers,
    # fall back to treating the entire document as one product.
    if not product_elements:
        product_elements = [soup]

    for product in product_elements:

        name_element = product.select_one(name_selector)
        price_element = product.select_one(price_selector)

        products.append(
            {
                "name": (
                    name_element.get_text(strip=True)
                    if name_element
                    else None
                ),
                "price": (
                    price_element.get_text(strip=True)
                    if price_element
                    else None
                ),
                "selector_version": selectors["version"],
            }
        )

    return products