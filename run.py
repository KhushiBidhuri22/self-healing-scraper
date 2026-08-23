from pathlib import Path

from app.parser import parse_product
from app.validator import detect_drift
from app.healer import heal_selector
from app.selector_registry import load_selectors


HTML_FILE = Path("fixtures/chaos/rename_class.html")

def load_html() -> str:
    return HTML_FILE.read_text(encoding="utf-8")


def main():
    print("=== Self-Healing Scraper ===")

    print("\n[1] Loading HTML...")
    html = load_html()

    print("[2] Loading selectors...")
    selectors = load_selectors()

    print("[3] Parsing product...")

    record = parse_product(html)

    # Validator expects a list of records.
    records = [record]

    print(f"    Product: {record['name']}")
    print(f"    Price: {record['price']}")
    print(f"    Selector version: {record['selector_version']}")

    print("\n[4] Validating...")

    validation = detect_drift(records)

    if not validation["drift"]:
        print("    ✅ No drift detected")
        print("\n=== Finished ===")
        return

    print("    🚨 Drift detected")
    print(f"    Broken fields: {validation['fields']}")

    if "name" in validation["fields"]:
        print("\n[5] Attempting name selector repair...")

        expected_name = "Full Cream Milk"

        result = heal_selector(
            html=html,
            field="name",
            expected_value=expected_name,
            current_selectors=selectors,
        )

        if result["healed"]:
            print("    ✅ Repair successful")
            print(f"    Old selector: {result['old_selector']}")
            print(f"    New selector: {result['new_selector']}")
            print(f"    Score: {result['score']}")
            print(f"    New version: {result['new_version']}")
        else:
            print("    ❌ Repair failed")
            print(f"    Reason: {result['reason']}")

    print("\n=== Finished ===")


if __name__ == "__main__":
    main()