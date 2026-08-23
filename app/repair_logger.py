import json
from datetime import datetime, timezone
from pathlib import Path


LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "repairs.jsonl"


def log_repair(
    field: str,
    old_selector: str,
    new_selector: str,
    score: int,
    evidence: list[str],
    new_version: int,
) -> dict:
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    repair = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "field": field,
        "old_selector": old_selector,
        "new_selector": new_selector,
        "score": score,
        "evidence": evidence,
        "new_version": new_version,
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(repair) + "\n")

    return repair