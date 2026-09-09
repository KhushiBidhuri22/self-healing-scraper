from pathlib import Path

from app.golden import load_golden
from app.parser import parse_product
from app.validator import detect_drift
from app.healer import heal_selector
from app.selector_registry import load_selectors


HTML_FILE = Path("fixtures/chaos/rename_class.html")


def test_self_healing_flow():

    html = HTML_FILE.read_text(
        encoding="utf-8"
    )

    selectors = {
    "version": 1,
    "fields": {
        "name": ".product-name",
        "price": ".price",
    },
}
    golden = load_golden()

    # 1. Parse using the currently active selectors
    record = parse_product(
        html,
        selectors=selectors,
    )

    # 2. Detect drift
    validation = detect_drift([record])

    assert validation["drift"] is True
    assert "name" in validation["fields"]

    # 3. Attempt healing
    result = heal_selector(
        html=html,
        field="name",
        expected_value=golden["name"],
        current_selectors=selectors,
    )

    assert result["healed"] is True
    assert result["new_selector"] == ".title"

    # 4. Replay must succeed
    assert result["replay"]["passed"] is True

    # 5. Parse again using the promoted selectors
    repaired_record = parse_product(
        html,
        selectors=result["selectors"],
    )

    # 6. The product should now be recovered
    assert repaired_record["name"] == golden["name"]

    # 7. Verify that the repaired dataset is healthy
    repaired_validation = detect_drift(
        [repaired_record]
    )

    assert repaired_validation["drift"] is False