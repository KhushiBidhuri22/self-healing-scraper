from pathlib import Path

from app.parser import parse_product
from app.store import save_items


HTML_FILE = Path(
    "fixtures/raw/test_product.html"
)


def main():
    html = HTML_FILE.read_text(
        encoding="utf-8"
    )

    record = parse_product(html)

    record["id"] = 1

    save_items([record])

    print("Saved product:")
    print(record)


if __name__ == "__main__":
    main()
