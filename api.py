from pathlib import Path
import json

from fastapi import FastAPI, Query

from app.store import load_items
from app.scraper import fetch_html
from app.parser import parse_products
from app.validator import detect_drift
from app.health_engine import HealthEngine
from app.healer import heal_selector
from app.golden import load_golden
from app.selector_registry import load_selectors

from metrics import calculate_metrics


app = FastAPI(
    title="Self-Healing Scraper API",
    version="1.0.0",
)


HTML_FILE = Path("fixtures/chaos/rename_class.html")
STARTING_SELECTOR_FILE = Path("selectors/v1.json")


def load_starting_selectors() -> dict:
    with STARTING_SELECTOR_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def serialize_health(report):
    return {
        "overall_score": report.overall_score,
        "status": report.status,
        "drift_fields": report.drift_fields,
        "fields": {
            field: {
                "total": health.total,
                "valid": health.valid,
                "missing": health.missing,
                "health_score": health.health_score,
            }
            for field, health in report.fields.items()
        },
    }


@app.get("/")
def root():
    return {
        "name": "Self-Healing E-Commerce Scraper",
        "status": "ok",
        "docs": "/docs",
    }


@app.get("/items")
def get_items(
    name: str | None = Query(
        default=None,
        description="Filter by product name",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    cursor: int = Query(
        default=0,
        ge=0,
    ),
):
    items = load_items()

    if name:
        items = [
            item
            for item in items
            if name.lower() in item["name"].lower()
        ]

    items = [
        item
        for item in items
        if item["id"] > cursor
    ]

    page = items[:limit]

    next_cursor = None

    if len(page) == limit:
        next_cursor = page[-1]["id"]

    return {
        "items": page,
        "count": len(page),
        "next_cursor": next_cursor,
    }


@app.get("/drift")
def get_drift():
    log_file = Path("logs/repairs.jsonl")

    repairs = []

    if log_file.exists():
        with log_file.open(
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:
                line = line.strip()

                if line:
                    repairs.append(
                        json.loads(line)
                    )

    return {
        "metrics": calculate_metrics(),
        "repairs": repairs,
    }


@app.get("/health")
def health():
    html = fetch_html(HTML_FILE)

    selectors = load_selectors()

    records = parse_products(
        html,
        selectors=selectors,
    )

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        required_fields=["name", "price"],
    )

    return {
        "selector_version": selectors["version"],
        "products_found": len(records),
        "health": serialize_health(report),
    }


@app.post("/scrape")
def scrape():
    html = fetch_html(HTML_FILE)

    selectors = load_selectors()

    records = parse_products(
        html,
        selectors=selectors,
    )

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        required_fields=["name", "price"],
    )

    return {
        "selector_version": selectors["version"],
        "products_found": len(records),
        "products": records,
        "health": serialize_health(report),
    }


@app.post("/heal")
def heal():
    html = fetch_html(HTML_FILE)

    selectors = load_starting_selectors()
    golden = load_golden()

    records = parse_products(
        html,
        selectors=selectors,
    )

    validation = detect_drift(records)

    if not validation["drift"]:
        return {
            "healed": False,
            "message": "No drift detected",
            "selector_version": selectors["version"],
            "health": "healthy",
        }

    repairs = []

    for field in validation["fields"]:

        expected_value = golden.get(field)

        if expected_value is None:
            continue

        result = heal_selector(
            html=html,
            field=field,
            expected_value=expected_value,
            current_selectors=selectors,
        )

        repairs.append(result)

        if result["healed"]:
            selectors = result["selectors"]

    repaired_records = parse_products(
        html,
        selectors=selectors,
    )

    engine = HealthEngine()

    report = engine.evaluate(
        repaired_records,
        required_fields=["name", "price"],
    )

    return {
        "healed": any(
            repair["healed"]
            for repair in repairs
        ),
        "repairs": repairs,
        "selector_version": selectors["version"],
        "products": repaired_records,
        "health": serialize_health(report),
    }