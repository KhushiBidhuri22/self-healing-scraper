from pathlib import Path

from bs4 import BeautifulSoup

from chaos import (
    rename_product_name_class,
    add_extra_wrapper,
    reorder_product_children,
    change_price_format,
    drop_attributes,
    lazy_load_product,
    remove_price_element,
    change_name_tag,
)

from app.parser import parse_product
from app.validator import detect_drift
from app.healer import heal_selector
from app.golden import load_golden


BASE_HTML_FILE = Path("fixtures/raw/test_product.html")


MUTATIONS = {
    "rename_class": rename_product_name_class,
    "add_wrapper": add_extra_wrapper,
    "reorder_children": reorder_product_children,
    "change_price_format": change_price_format,
    "drop_attributes": drop_attributes,
    "lazy_load": lazy_load_product,
    "remove_price": remove_price_element,
    "change_name_tag": change_name_tag,
}


def load_base_html():
    return BASE_HTML_FILE.read_text(encoding="utf-8")


def fresh_selectors():
    """
    Every chaos experiment starts from the original
    selector registry.

    This prevents one experiment from affecting another.
    """
    return {
        "version": 1,
        "fields": {
            "name": ".product-name",
            "price": ".price",
        },
    }


def test_mutation(name, mutation):
    """
    Run one chaos mutation and attempt to heal it.
    """

  

    html = load_base_html()

 

    mutated_html = mutation(html)


    selectors = fresh_selectors()

    golden = load_golden()



    record = parse_product(mutated_html)

 

    validation = detect_drift([record])

   
    if not validation["drift"]:
        return {
            "name": name,
            "status": "RECOVERED",
            "recovered": True,
            "broken_fields": [],
            "healed_fields": [],
        }

  

    healed_fields = []

    for field in validation["fields"]:

        expected_value = golden.get(field)

        if expected_value is None:
            continue

        result = heal_selector(
            html=mutated_html,
            field=field,
            expected_value=expected_value,
            current_selectors=selectors,
        )

        if result["healed"]:

            healed_fields.append(field)

            selectors["fields"][field] = result["new_selector"]
            selectors["version"] = result["new_version"]




    soup = BeautifulSoup(mutated_html, "lxml")

    final_values = {}

    for field in ["name", "price"]:

        selector = selectors["fields"].get(field)

        if selector:
            element = soup.select_one(selector)

            final_values[field] = (
                element.get_text(strip=True)
                if element
                else None
            )
        else:
            final_values[field] = None

  

    recovered = all(
        final_values.get(field) == golden.get(field)
        for field in ["name", "price"]
    )

    return {
        "name": name,
        "status": "RECOVERED" if recovered else "FAILED",
        "recovered": recovered,
        "broken_fields": validation["fields"],
        "healed_fields": healed_fields,
        "final_values": final_values,
    }


def main():

    print("=== SELF-HEALING CHAOS TEST ===")
    print()

    results = []



    for name, mutation in MUTATIONS.items():

        result = test_mutation(
            name,
            mutation,
        )

        results.append(result)

        if result["recovered"]:

            print(
                f"{name:25}  RECOVERED"
            )

        else:

            print(
                f"{name:25}  FAILED"
            )

            if result.get("broken_fields"):
                print(
                    f"    Broken: "
                    f"{result['broken_fields']}"
                )

            if result.get("healed_fields"):
                print(
                    f"    Healed: "
                    f"{result['healed_fields']}"
                )

 

    recovered_count = sum(
        result["recovered"]
        for result in results
    )

    total = len(results)

    recovery_rate = (
        recovered_count / total * 100
        if total
        else 0
    )

   

    print()
    print("================================")
    print(
        f"Recovery: {recovered_count}/{total}"
    )
    print(
        f"Rate: {recovery_rate:.1f}%"
    )
    print("================================")


if __name__ == "__main__":
    main()