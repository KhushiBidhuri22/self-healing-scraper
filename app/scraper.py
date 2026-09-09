from pathlib import Path


def fetch_html(source: str | Path) -> str:
    """
    Load HTML from a local file.

    This keeps the scraper input layer separate from
    parsing, validation, and self-healing logic.
    """

    path = Path(source)

    if not path.exists():
        raise FileNotFoundError(
            f"HTML source not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"HTML source is not a file: {path}"
        )

    return path.read_text(
        encoding="utf-8"
    )