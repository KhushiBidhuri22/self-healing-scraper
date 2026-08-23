from bs4 import BeautifulSoup


def rename_product_name_class(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    elements = soup.select(".product-name")

    for element in elements:
        classes = element.get("class", [])

        if "product-name" in classes:
            classes.remove("product-name")
            classes.append("title")
            element["class"] = classes

    return str(soup)