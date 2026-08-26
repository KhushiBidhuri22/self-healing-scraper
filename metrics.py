from pathlib import Path
import json


LOG_FILE = Path("logs/repairs.jsonl")


def load_repairs():
    if not LOG_FILE.exists():
        return []

    repairs = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                repairs.append(json.loads(line))

    return repairs


def calculate_metrics():
    repairs = load_repairs()

    total = len(repairs)

    if total == 0:
        return {
            "total_repairs": 0,
            "successful_repairs": 0,
            "average_score": 0,
        }

    successful = sum(
        repair.get("score", 0) >= 90
        for repair in repairs
    )

    average_score = (
        sum(repair.get("score", 0) for repair in repairs)
        / total
    )

    return {
        "total_repairs": total,
        "successful_repairs": successful,
        "success_rate": round(
            successful / total * 100,
            2,
        ),
        "average_score": round(
            average_score,
            2,
        ),
    }


if __name__ == "__main__":
    metrics = calculate_metrics()

    print("=== HEALING METRICS ===")

    for key, value in metrics.items():
        print(f"{key}: {value}")