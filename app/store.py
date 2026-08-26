import json
from pathlib import Path


DATA_FILE = Path("data/items.json")


def save_items(items: list[dict]) -> None:
    DATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with DATA_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            items,
            file,
            indent=2,
        )


def load_items() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)