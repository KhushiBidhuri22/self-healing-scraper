import json
from pathlib import Path

from app.parser import parse_product
from app.validator import detect_drift
from app.healer import heal_selector
from app.golden import load_golden


HTML_FILE = Path("fixtures/chaos/rename_class.html")
STARTING_SELECTOR_FILE = Path("selectors/v1.json")


def load_html() -> str:
    return HTML_FILE.read_text(encoding="utf-8")


def load_starting_selectors() -> dict:
    with STARTING_SELECTOR_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def main():
    print("=== Self-Healing Scraper ===")

    # 1. Load HTML
    print("\n[1] Loading HTML...")
    html = load_html()

    # 2. Load starting selectors
    print("[2] Loading selectors...")
    selectors = load_starting_selectors()
    golden = load_golden()

    print(
        f"    Starting selector version: "
        f"{selectors['version']}"
    )

    # 3. Parse
    print("\n[3] Parsing product...")

    record = parse_product(
        html,
        selectors=selectors,
    )

    print(f"    Product: {record['name']}")
    print(f"    Price: {record['price']}")
    print(
        f"    Selector version: "
        f"{record['selector_version']}"
    )

    # 4. Validate
    print("\n[4] Validating...")

    validation = detect_drift([record])

    if not validation["drift"]:
        print("     No drift detected")
        print("\n=== Finished ===")
        return

    print("     Drift detected")
    print(
        f"    Broken fields: "
        f"{validation['fields']}"
    )

    # 5. Attempt repairs
    for field in validation["fields"]:

        print(
            f"\n[5] Attempting "
            f"{field} selector repair..."
        )

        expected_value = golden.get(field)

        if expected_value is None:
            print(
                f"     No golden value found "
                f"for {field}"
            )
            continue

        result = heal_selector(
            html=html,
            field=field,
            expected_value=expected_value,
            current_selectors=selectors,
        )

        if not result["healed"]:
            print("     Repair failed")
            print(
                f"    Reason: "
                f"{result['reason']}"
            )
            continue

        print("     Repair successful")
        print(
            f"    Old selector: "
            f"{result['old_selector']}"
        )
        print(
            f"    New selector: "
            f"{result['new_selector']}"
        )
        print(
            f"    Score: "
            f"{result['score']}"
        )
        print(
            f"    New version: "
            f"{result['new_version']}"
        )

        # 6. Verify repair
        print(
            "\n[6] Verifying repaired scraper..."
        )

        selectors = result["selectors"]

        repaired_record = parse_product(
            html,
            selectors=selectors,
        )

        print(
            f"    Product: "
            f"{repaired_record['name']}"
        )
        print(
            f"    Price: "
            f"{repaired_record['price']}"
        )
        print(
            f"    Selector version: "
            f"{repaired_record['selector_version']}"
        )

        repaired_validation = detect_drift(
            [repaired_record]
        )

        if not repaired_validation["drift"]:
            print("     HEALTH RESTORED")
        else:
            print(
                "     Repair did not restore health"
            )
            print(
                f"    Remaining drift: "
                f"{repaired_validation['fields']}"
            )

    print("\n=== Finished ===")


if __name__ == "__main__":
    main()