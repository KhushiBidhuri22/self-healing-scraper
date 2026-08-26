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


def add_extra_wrapper(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    products = soup.select(".product")

    for product in products:
        wrapper = soup.new_tag("div")
        wrapper["class"] = "extra-wrapper"

        children = list(product.children)

        for child in children:
            wrapper.append(child.extract())

        product.append(wrapper)

    return str(soup)
def reorder_product_children(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for product in soup.select(".product"):
        children = [
            child
            for child in product.children
            if getattr(child, "name", None)
        ]

        children.reverse()

        for child in children:
            product.append(child.extract())

    return str(soup)

def change_price_format(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for element in soup.select(".price"):
        text = element.get_text(strip=True)

        if text == "$4.50":
            element.string = "4,50 USD"

    return str(soup)
def drop_attributes(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for element in soup.select(".product-name, .price"):
        if element.has_attr("data-testid"):
            del element["data-testid"]

        if element.has_attr("id"):
            del element["id"]

    return str(soup)

def lazy_load_product(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for product in soup.select(".product"):
        for element in product.select(".product-name, .price"):
            element.decompose()

        loading = soup.new_tag("div")
        loading["class"] = "loading"
        loading.string = "Loading..."

        product.append(loading)

    return str(soup)

def remove_price_element(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for element in soup.select(".price"):
        element.decompose()

    return str(soup)

def change_name_tag(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for element in soup.select(".product-name"):
        element.name = "div"

    return str(soup)