from bs4 import BeautifulSoup


def replay_candidate(
    html: str,
    selector: str,
    expected_value: str,
) -> dict:
    """
    Test a candidate selector against the HTML and golden value
    before allowing it to be promoted.
    """

    soup = BeautifulSoup(html, "lxml")

    elements = soup.select(selector)

    if not elements:
        return {
            "passed": False,
            "reason": "Candidate matched nothing",
        }

    values = [
        element.get_text(strip=True)
        for element in elements
    ]

    if expected_value not in values:
        return {
            "passed": False,
            "reason": "Candidate did not reproduce golden value",
            "values": values,
        }

    if len(elements) != 1:
        return {
            "passed": False,
            "reason": "Candidate is not unique",
            "values": values,
        }

    return {
        "passed": True,
        "reason": "Candidate reproduced golden value",
        "value": values[0],
    }