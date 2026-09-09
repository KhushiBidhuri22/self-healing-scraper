import json
from pathlib import Path


SELECTOR_DIRECTORY = Path("selectors")


def promote_selector(
    current_selectors: dict,
    field: str,
    new_selector: str,
) -> dict:

    current_selector = current_selectors["fields"].get(field)

    # Do not create a new version if nothing actually changed.
    if current_selector == new_selector:
        return current_selectors

    current_version = current_selectors["version"]
    new_version = current_version + 1

    new_selectors = {
        "version": new_version,
        "fields": current_selectors["fields"].copy(),
    }

    new_selectors["fields"][field] = new_selector

    SELECTOR_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        SELECTOR_DIRECTORY / f"v{new_version}.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            new_selectors,
            file,
            indent=2,
        )

    return new_selectors