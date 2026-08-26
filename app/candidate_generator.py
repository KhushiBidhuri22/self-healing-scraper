from bs4 import BeautifulSoup


def generate_candidates(html: str, field: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")

    candidates = []

    if field == "name":
        for element in soup.find_all(["h1", "h2", "h3", "h4"]):
            classes = element.get("class", [])

            for class_name in classes:
                candidates.append(f".{class_name}")
                candidates.append(f"{element.name}.{class_name}")

            candidates.append(element.name)

    
    return list(dict.fromkeys(candidates))