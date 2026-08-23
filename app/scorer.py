from bs4 import BeautifulSoup


def score_candidate(
    html: str,
    selector: str,
    expected_value: str,
) -> dict:
    soup = BeautifulSoup(html, "lxml")

    elements = soup.select(selector)

    score = 0
    reasons = []

    # Does the selector find anything?
    if not elements:
        return {
            "selector": selector,
            "score": 0,
            "matched": False,
            "reasons": ["selector matched nothing"],
        }

    # Does it match the expected value?
    values = [
        element.get_text(strip=True)
        for element in elements
    ]

    if expected_value in values:
        score += 70
        reasons.append("matched expected value")

    # Is it unique?
    if len(elements) == 1:
        score += 20
        reasons.append("matched exactly one element")

    # Prefer more specific selectors.
    if "." in selector:
        score += 10
        reasons.append("selector includes a class")

    return {
        "selector": selector,
        "score": score,
        "matched": expected_value in values,
        "reasons": reasons,
    }