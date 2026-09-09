from app.baseline import BaselineComparator


def test_baseline_matches():

    expected = {
        "name": "Full Cream Milk",
        "price": "$4.50"
    }

    actual = {
        "name": "Full Cream Milk",
        "price": "$4.50"
    }

    comparator = BaselineComparator()

    report = comparator.compare(
        actual,
        expected
    )

    assert report.drift_fields == []
    assert report.comparisons["price"].matches is True


def test_baseline_detects_price_drift():

    expected = {
        "name": "Full Cream Milk",
        "price": "$4.50"
    }

    actual = {
        "name": "Full Cream Milk",
        "price": None
    }

    comparator = BaselineComparator()

    report = comparator.compare(
        actual,
        expected
    )

    assert "price" in report.drift_fields
    assert report.comparisons["price"].expected == "$4.50"
    assert report.comparisons["price"].actual is None


def test_baseline_detects_multiple_drift_fields():

    expected = {
        "name": "Full Cream Milk",
        "price": "$4.50"
    }

    actual = {
        "name": "Wrong Product",
        "price": None
    }

    comparator = BaselineComparator()

    report = comparator.compare(
        actual,
        expected
    )

    assert "name" in report.drift_fields
    assert "price" in report.drift_fields