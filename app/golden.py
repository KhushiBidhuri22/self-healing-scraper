import json
from pathlib import Path


GOLDEN_FILE = Path("fixtures/golden/expected.json")
MULTI_GOLDEN_FILE = Path(
    "fixtures/golden/multi_product_expected.json"
)


def load_golden() -> dict:
    with GOLDEN_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def load_golden_products() -> list[dict]:
    with MULTI_GOLDEN_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)