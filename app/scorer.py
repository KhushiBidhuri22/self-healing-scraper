from bs4 import BeautifulSoup


def score_candidate(
    html: str,
    selector: str,
    expected_value: str,
    field: str | None = None,
) -> dict:

    soup = BeautifulSoup(html, "lxml")

    elements = soup.select(selector)

    if not elements:
        return {
            "selector": selector,
            "score": 0,
            "matched": False,
            "reasons": ["selector matched nothing"],
        }

    values = [
        element.get_text(strip=True)
        for element in elements
    ]

    score = 0
    reasons = []

    # Evidence 1: candidate reproduces the golden value
    if expected_value in values:
        score += 70
        reasons.append("matched expected value")

    # Evidence 2: candidate is unique
    if len(elements) == 1:
        score += 20
        reasons.append("matched exactly one element")

    # Evidence 3: class-based selectors are more specific
    if "." in selector:
        score += 10
        reasons.append("selector includes a class")

    # Evidence 4: semantic relationship between selector and field
    if field and _selector_matches_field(selector, field):
        score += 10
        reasons.append("selector matches field semantics")

    # A candidate with all strong evidence should score 100.
    score = min(score, 100)

    return {
        "selector": selector,
        "score": score,
        "matched": expected_value in values,
        "reasons": reasons,
    }


def _selector_matches_field(
    selector: str,
    field: str,
) -> bool:

    selector_lower = selector.lower()
    field_lower = field.lower()

    semantic_terms = {
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

    terms = semantic_terms.get(
        field_lower,
        [field_lower],
    )

    return any(
        term in selector_lower
        for term in terms
    )