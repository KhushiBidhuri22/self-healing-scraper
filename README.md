# Self-Healing E-Commerce Scraper

## Problem

Traditional web scrapers depend on fragile CSS selectors.
When a website changes its DOM structure, extraction silently fails.

This project detects extraction drift and automatically searches
for replacement selectors.

## Architecture

Fetcher
→ Parser
→ Validator
→ Candidate Generator
→ Scorer
→ Golden Replay
→ Promote / Rollback
→ API

## Self-Healing Flow

1. Parse using current selector version.
2. Validate extracted records.
3. Detect drift.
4. Generate candidate selectors.
5. Score candidates.
6. Replay candidate against golden records.
7. Promote only when confidence is sufficient.
8. Otherwise reject/quarantine the candidate.
9. Log the repair.

## Chaos Testing

8 deliberate DOM mutations were tested.

| Mutation | Result |
|---|---|
| rename class | recovered |
| add wrapper | recovered |
| reorder children | recovered |
| change price format | recovered |
| drop attributes | recovered |
| lazy loading | failed safely |
| remove price | failed safely |
| change name tag | recovered |

Recovery: 6/8 (75%).

## Safe Failure

The system intentionally does not invent values when the
source data has been removed.

## Testing

```bash
python -m pytest
python chaos_runner.py