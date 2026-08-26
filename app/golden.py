import json
from pathlib import Path


GOLDEN_FILE = Path("fixtures/golden/expected.json")


def load_golden() -> dict:
    with GOLDEN_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)