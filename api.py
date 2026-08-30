from pathlib import Path
import json

from fastapi import FastAPI, Query

from app.store import load_items

from metrics import calculate_metrics


app = FastAPI(
    title="Self-Healing Scraper API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "name": "Self-Healing E-Commerce Scraper",
        "status": "ok",
        "docs": "/docs"
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
            if name.lower()
            in item["name"].lower()
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

    return {
        "status": "ok"
    }