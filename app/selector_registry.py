import json
from pathlib import Path


SELECTOR_FILE = Path("selectors/v1.json")


def load_selectors() -> dict:
    with SELECTOR_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)