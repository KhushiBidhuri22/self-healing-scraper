from app.health_engine import HealthEngine


def test_healthy_dataset():

    records = [
        {
            "name": "Product A",
            "price": "100",
            "rating": "4.5"
        },
        {
            "name": "Product B",
            "price": "200",
            "rating": "4.2"
        }
    ]

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        ["name", "price", "rating"]
    )

    assert report.status == "healthy"
    assert report.overall_score == 100
    assert report.drift_fields == []


def test_price_drift():

    records = [
        {
            "name": "Product A",
            "price": "100",
            "rating": "4.5"
        },
        {
            "name": "Product B",
            "price": None,
            "rating": "4.2"
        }
    ]

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        ["name", "price", "rating"]
    )

    assert "price" in report.drift_fields
    assert report.status == "degraded"


def test_invalid_price_is_detected():

    records = [
        {
            "name": "Product A",
            "price": "100",
            "rating": "4.5"
        },
        {
            "name": "Product B",
            "price": "INVALID",
            "rating": "4.2"
        }
    ]

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        ["name", "price", "rating"]
    )

    assert report.fields["price"].valid == 1
    assert report.fields["price"].missing == 1
    assert "price" in report.drift_fields


def test_invalid_rating_is_detected():

    records = [
        {
            "name": "Product A",
            "price": "100",
            "rating": "4.5"
        },
        {
            "name": "Product B",
            "price": "200",
            "rating": "10"
        }
    ]

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        ["name", "price", "rating"]
    )

    assert report.fields["rating"].valid == 1
    assert "rating" in report.drift_fields


def test_invalid_review_count_is_detected():

    records = [
        {
            "name": "Product A",
            "price": "100",
            "rating": "4.5",
            "review_count": "1200"
        },
        {
            "name": "Product B",
            "price": "200",
            "rating": "4.2",
            "review_count": "not-a-number"
        }
    ]

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        ["name", "price", "rating", "review_count"]
    )

    assert report.fields["review_count"].valid == 1
    assert "review_count" in report.drift_fields

def test_health_engine_uses_validator_rules():

    records = [
        {
            "name": "Full Cream Milk",
            "price": "$4.50"
        },
        {
            "name": "Another Product",
            "price": "INVALID"
        }
    ]

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        ["name", "price"]
    )

    assert report.fields["price"].valid == 1
    assert report.fields["price"].missing == 1
    assert "price" in report.drift_fields