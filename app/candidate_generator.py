from bs4 import BeautifulSoup


def generate_candidates(html: str, field: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")

    candidates = []

    # Field-specific semantic hints
    hints = {
        "name": [
            "name",
            "title",
            "product-name",
            "product-title",
        ],
        "price": [
            "price",
            "cost",
            "amount",
        ],
        "rating": [
            "rating",
            "stars",
            "score",
        ],
        "review_count": [
            "review",
            "reviews",
            "review-count",
        ],
    }

    field_hints = hints.get(field, [field])

    # 1. Class-based candidates
    for element in soup.find_all(True):

        classes = element.get("class", [])

        for class_name in classes:
            class_lower = class_name.lower()

            if any(
                hint in class_lower
                for hint in field_hints
            ):
                candidates.append(f".{class_name}")
                candidates.append(
                    f"{element.name}.{class_name}"
                )

    # 2. Semantic HTML candidates
    semantic_tags = {
        "name": ["h1", "h2", "h3", "h4"],
        "price": ["span", "div"],
        "rating": ["span", "div"],
        "review_count": ["span", "div"],
    }

    for tag in semantic_tags.get(field, []):

        for element in soup.find_all(tag):

            classes = element.get("class", [])

            for class_name in classes:
                candidates.append(f".{class_name}")
                candidates.append(
                    f"{element.name}.{class_name}"
                )

            if field == "name":
                candidates.append(element.name)

    # 3. data-testid candidates
    for element in soup.find_all(True):

        test_id = element.get("data-testid")

        if test_id:
            test_id_lower = test_id.lower()

            if any(
                hint in test_id_lower
                for hint in field_hints
            ):
                candidates.append(
                    f'[data-testid="{test_id}"]'
                )

    # 4. ID-based candidates
    for element in soup.find_all(True):

        element_id = element.get("id")

        if element_id:
            id_lower = element_id.lower()

            if any(
                hint in id_lower
                for hint in field_hints
            ):
                candidates.append(f"#{element_id}")
                candidates.append(
                    f"{element.name}#{element_id}"
                )

    return list(dict.fromkeys(candidates))