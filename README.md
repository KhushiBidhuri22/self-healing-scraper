# Self-Healing E-Commerce Scraper

A fault-tolerant web scraping system that detects DOM drift, automatically searches for replacement CSS selectors, validates candidate repairs against known-good data, and promotes successful selectors without requiring manual code changes.

##  Live Demo

**API:** https://self-healing-scraper-1.onrender.com

**Swagger / API Docs:** https://self-healing-scraper-1.onrender.com/docs

**GitHub:** https://github.com/KhushiBidhuri22/self-healing-scraper

---

## Problem

Traditional web scrapers depend on fixed CSS selectors.

For example:

```text
.product-name
.price
```

When a website changes its HTML structure or class names, the scraper can silently stop extracting data.

This project treats selector failure as **recoverable drift**.

Instead of immediately failing, the system:

1. Detects broken or invalid extraction results.
2. Generates alternative selectors from the current DOM.
3. Scores candidates using multiple signals.
4. Compares candidates against known-good ("golden") values.
5. Promotes a high-confidence replacement selector.
6. Versions the updated selector configuration.
7. Records the repair as an auditable JSONL event.

---

##  Architecture

```text
                    HTML
                     │
                     ▼
              ┌─────────────┐
              │   Parser    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │  Validator  │
              └──────┬──────┘
                     │
              DOM drift detected
                     │
                     ▼
          ┌─────────────────────┐
          │ Candidate Generator │
          └──────────┬──────────┘
                     │
                     ▼
              ┌─────────────┐
              │    Scorer   │
              └──────┬──────┘
                     │
              confidence threshold
                     │
                     ▼
          ┌─────────────────────┐
          │ Selector Promoter   │
          └──────────┬──────────┘
                     │
             versioned selector
                     │
                     ▼
              ┌─────────────┐
              │ Repair Log  │
              └─────────────┘
```

---

##  Core Components

### Parser

Extracts product fields using the currently active selector configuration.

### Validator

Detects extraction drift using:

* null-rate thresholds
* invalid-name detection
* invalid-price detection
* field-level drift reporting

### Candidate Generator

Searches the current DOM for alternative selectors when an existing selector breaks.

### Candidate Scorer

Ranks candidate selectors using evidence such as:

* expected value match
* unique element match
* selector specificity

A candidate must reach the configured promotion threshold before it can replace the existing selector.

### Selector Promoter

Writes successful repairs as a new selector version.

Example:

```text
v1 → v2
.product-name → .title
```

### Repair Logger

Every successful repair is stored in:

```text
logs/repairs.jsonl
```

Example:

```json
{
  "field": "name",
  "old_selector": ".product-name",
  "new_selector": ".title",
  "score": 100,
  "new_version": 2
}
```

This makes selector repairs auditable and reproducible.

---

##  Chaos Testing

The project includes deliberate DOM mutations to simulate real scraper failures.

Current chaos scenarios include:

| Mutation                | Result            |
| ----------------------- | ----------------- |
| Rename class            |  Recovered       |
| Add wrapper             |  Recovered       |
| Reorder children        |  Recovered       |
| Change price format     |  Recovered       |
| Drop attributes         |  Recovered       |
| Lazy-load/remove fields |  Safely rejected |
| Remove price element    |  Safely rejected |
| Change name tag         |  Recovered       |

### Current recovery result

**6 / 8 mutations recovered — 75% recovery rate**

The two failed cases intentionally demonstrate an important safety property: when the required source data is actually removed from the DOM, the system does not fabricate a replacement value.

---

##  Test Coverage

The project currently passes:

```text
25 passed
```

Test coverage includes:

* parser behavior
* validator behavior
* selector candidate generation
* candidate scoring
* selector healing
* selector promotion
* repair logging
* golden-data validation
* replay behavior
* chaos mutations

Run the test suite with:

```bash
python -m pytest
```

---

##  Running Locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the scraper demonstration:

```bash
python run.py
```

Run chaos testing:

```bash
python chaos_runner.py
```

Run tests:

```bash
python -m pytest
```

Run the API:

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

---

##  Deployment

The API is deployed using Render.

Production start command:

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Live service:

https://self-healing-scraper-1.onrender.com

---

##  Design Philosophy

The system follows a conservative repair strategy:

> **Detect → Search → Score → Validate → Promote → Log**

It does not automatically accept every possible selector.

A replacement must provide sufficient evidence before it is promoted. When the source data itself disappears, the system fails safely rather than inventing data.

---

##  Example Repair

Original HTML:

```html
<h2 class="product-name">Full Cream Milk</h2>
```

Existing selector:

```css
.product-name
```

After a simulated website change:

```html
<h2 class="title">Full Cream Milk</h2>
```

The original selector fails.

The healing pipeline identifies:

```css
.title
```

as a high-confidence replacement:

```text
Score: 100

Old selector: .product-name
New selector: .title
Version: 2
```

The repair is persisted and logged.

---


