import json
from pathlib import Path


SELECTOR_DIRECTORY = Path("selectors")


def get_latest_selector_file() -> Path:
    selector_files = list(
        SELECTOR_DIRECTORY.glob("v*.json")
    )

    if not selector_files:
        raise FileNotFoundError(
            "No selector files found."
        )

    return max(
        selector_files,
        key=lambda file: int(
            file.stem[1:]
        ),
    )


def load_selectors() -> dict:
    selector_file = get_latest_selector_file()

    with selector_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)