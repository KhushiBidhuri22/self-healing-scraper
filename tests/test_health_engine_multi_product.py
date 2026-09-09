from app.health_engine import HealthEngine


def test_multi_product_health():

    records = [
        {
            "name": "Full Cream Milk",
            "price": "$4.50",
        },
        {
            "name": "Toned Milk",
            "price": "$3.80",
        },
        {
            "name": "Organic Milk",
            "price": "$5.20",
        },
    ]

    engine = HealthEngine()

    report = engine.evaluate(
        records,
        required_fields=["name", "price"],
    )

    assert report.overall_score == 100.0
    assert report.status == "healthy"
    assert report.drift_fields == []