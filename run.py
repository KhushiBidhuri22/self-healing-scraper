from pathlib import Path

from app.parser import parse_product
from app.validator import detect_drift
from app.healer import heal_selector
from app.selector_registry import load_selectors
from app.golden import load_golden


HTML_FILE = Path("fixtures/chaos/rename_class.html")


def load_html() -> str:
    return HTML_FILE.read_text(encoding="utf-8")


def main():
    print("=== Self-Healing Scraper ===")

    # 1. Load HTML
    print("\n[1] Loading HTML...")
    html = load_html()

    # 2. Load selectors and golden data
    print("[2] Loading selectors...")
    selectors = load_selectors()
    golden = load_golden()

    # 3. Parse product
    print("[3] Parsing product...")

    record = parse_product(html)

    # Validator expects a list of records.
    records = [record]

    print(f"    Product: {record['name']}")
    print(f"    Price: {record['price']}")
    print(f"    Selector version: {record['selector_version']}")

    # 4. Validate
    print("\n[4] Validating...")

    validation = detect_drift(records)

    if not validation["drift"]:
        print("    ✅ No drift detected")
        print("\n=== Finished ===")
        return

    print("    🚨 Drift detected")
    print(f"    Broken fields: {validation['fields']}")

    # 5. Attempt repairs
    for field in validation["fields"]:
        print(f"\n[5] Attempting {field} selector repair...")

        expected_value = golden.get(field)

        if expected_value is None:
            print(f"    ❌ No golden value found for {field}")
            continue

        result = heal_selector(
            html=html,
            field=field,
            expected_value=expected_value,
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