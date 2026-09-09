#  Self-Healing E-Commerce Scraper

A resilient web scraping system that can **detect broken selectors, automatically discover replacement selectors, validate the repair, and promote the repaired selector** without requiring manual code changes.

Traditional scrapers are fragile: a small HTML change such as renaming a CSS class can silently break data extraction.

This project treats scraper failures as **recoverable drift**.

* Deployed Link -https://self-healing-scraper-1.onrender.com
* Docs Link -https://self-healing-scraper-1.onrender.com/docs?

---

##  The Problem

Websites frequently change their HTML structure.

For example, a scraper may originally use:

```css
.product-name
```

But after a website update, the same product name may become:

```css
.title
```

A traditional scraper returns:

```text
Product: None
```

and requires a developer to manually inspect the website and update the selector.

### Our approach

Instead of stopping at the failure, the system:

1. Detects the broken field
2. Generates alternative selectors
3. Scores candidates using multiple signals
4. Replays the candidate against the expected value
5. Promotes the best valid selector
6. Logs the repair
7. Re-runs the scraper
8. Confirms that scraper health has been restored

---

#  How It Works

```text
             HTML PAGE
                 │
                 ▼
        ┌─────────────────┐
        │     Parser      │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Health / Drift  │
        │    Detection    │
        └────────┬────────┘
                 │
          Drift detected
                 │
                 ▼
        ┌─────────────────┐
        │    Candidate    │
        │    Generator    │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │     Scorer      │
        └────────┬────────┘
                 │
          Best candidate
                 │
                 ▼
        ┌─────────────────┐
        │ Replay / Verify │
        └────────┬────────┘
                 │
          Validation passed
                 │
                 ▼
        ┌─────────────────┐
        │    Selector     │
        │    Promoter     │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Repair Logger  │
        └────────┬────────┘
                 │
                 ▼
          HEALTH RESTORED
```

---

#  Key Features

###  Drift Detection

Detects when required fields stop producing valid values.

Example:

```text
Product name → None
Price         → $4.50
```

The system identifies:

```text
Broken fields: ['name']
```

---

###  Automatic Candidate Generation

When a selector fails, the system searches the HTML for alternative selectors using:

* Semantic class names
* Field-specific hints
* HTML tags
* `data-testid` attributes
* More specific selector combinations

For example:

```text
.product-name
.title
h2.title
```

---

###  Candidate Scoring

Candidates are evaluated using multiple pieces of evidence:

* Expected/golden value match
* Selector uniqueness
* Selector specificity
* Semantic relationship to the field

A strong candidate can reach:

```text
Score: 100
```

---

###  Replay Validation

The candidate is not automatically accepted.

The system first replays the candidate selector against the HTML and verifies that it actually produces the expected value.

This prevents weak or incorrect selectors from being promoted.

---

###  Selector Promotion

Once a candidate passes validation, it becomes the new active selector.

Example:

```text
Old selector: .product-name
New selector: .title
New version: 2
```

---

###  Health Engine

The project also evaluates scraper health at the field level.

Each field receives a health score based on the percentage of valid records.

Possible overall states:

```text
healthy
degraded
critical
```

This allows the system to monitor scraper quality rather than simply checking whether the program crashed.

---

###  Multi-Product Parsing

The parser supports multiple products on the same page.

Example:

```text
1. Full Cream Milk — $4.50
2. Toned Milk      — $3.80
3. Organic Milk    — $5.20
```

---

###  Repair Logging

Successful repairs are recorded so that selector changes can be audited later.

Repair information includes:

* Field
* Old selector
* New selector
* Candidate score
* Evidence
* New selector version

---

#  Example: Self-Healing in Action

The original selector configuration contains:

```json
{
  "name": ".product-name",
  "price": ".price"
}
```

The website changes:

```html
<h2 class="title">Full Cream Milk</h2>
```

The scraper initially produces:

```text
Product: None
Price: $4.50
```

The health system detects:

```text
Drift detected
Broken fields: ['name']
```

The healing system searches for candidates and identifies:

```text
.title
```

The candidate matches the expected golden value:

```text
Full Cream Milk
```

After replay validation:

```text
Repair successful
Old selector: .product-name
New selector: .title
Score: 100
New version: 2
```

The scraper is executed again:

```text
Product: Full Cream Milk
Price: $4.50
Selector version: 2

HEALTH RESTORED
```

---

#  Project Structure

```text
self-healing-scraper/
│
├── app/
│   ├── baseline.py
│   ├── candidate_generator.py
│   ├── golden.py
│   ├── healer.py
│   ├── health_engine.py
│   ├── parser.py
│   ├── repair_logger.py
│   ├── replay.py
│   ├── scraper.py
│   ├── scorer.py
│   ├── selector_promoter.py
│   ├── selector_registry.py
│   ├── store.py
│   ├── validator.py
│   └── __init__.py
│
├── fixtures/
│   ├── chaos/
│   │   └── rename_class.html
│   │
│   └── golden/
│       ├── expected.json
│       ├── multi_product.html
│       └── multi_product_expected.json
│
├── selectors/
│   └── v1.json
│
├── tests/
│   ├── test_baseline.py
│   ├── test_candidate_generator.py
│   ├── test_chaos.py
│   ├── test_end_to_end.py
│   ├── test_golden.py
│   ├── test_healer.py
│   ├── test_health_engine.py
│   ├── test_multi_product_parser.py
│   ├── test_parser.py
│   ├── test_repair_logger.py
│   ├── test_replay.py
│   ├── test_scorer.py
│   ├── test_scraper.py
│   ├── test_selector_promoter.py
│   └── test_validator.py
│
├── api.py
├── run.py
├── metrics.py
├── metrics.md
├── requirements.txt
└── README.md
```

---

#  Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd self-healing-scraper
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶ Run the Self-Healing Demo

Run:

```bash
python run.py
```

A successful repair looks like:

```text
=== Self-Healing Scraper ===

[1] Loading HTML...
[2] Loading selectors...
    Starting selector version: 1

[3] Parsing products...
    Products found: 1
    1. None — $4.50

[4] Validating...
     Drift detected
    Broken fields: ['name']

[5] Attempting name selector repair...
     Repair successful
    Old selector: .product-name
    New selector: .title
    Score: 100
    New version: 2

[6] Verifying repaired scraper...
    Products found: 1
    1. Full Cream Milk — $4.50
     HEALTH RESTORED

=== Finished ===
```

---

#  API

The project also exposes a FastAPI interface.

Start the API with:

```bash
uvicorn api:app --reload
```

Available endpoints:

| Endpoint  | Purpose                               |
| --------- | ------------------------------------- |
| `/`       | API information                       |
| `/items`  | Retrieve scraped products             |
| `/drift`  | View repair/drift information         |
| `/health` | API health check                      |
| `/docs`   | Interactive Swagger API documentation |

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

#  Testing

Run the complete test suite:

```bash
python -m pytest
```

Current test result:

```text
45 passed
```

The test suite covers:

* Parsing
* Multi-product extraction
* Candidate generation
* Candidate scoring
* Drift detection
* Health scoring
* Replay validation
* Selector promotion
* Repair logging
* Scraper input
* End-to-end self-healing

---

#  Chaos Testing

The project includes intentionally broken HTML fixtures.

For example:

```text
fixtures/chaos/rename_class.html
```

The fixture simulates a real-world website change where a selector becomes invalid.

This allows the self-healing pipeline to be tested deterministically.

---

#  Design Principle

The system does **not** blindly replace broken selectors.

A selector must provide enough evidence to be considered a valid repair.

The repair pipeline is:

```text
Detect
  ↓
Generate
  ↓
Score
  ↓
Replay
  ↓
Promote
  ↓
Log
  ↓
Verify
```

This makes selector healing safer and more explainable than simply choosing the first element that looks correct.

---

