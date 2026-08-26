from app.golden import load_golden


def test_load_golden():
    golden = load_golden()

    assert golden["name"] == "Full Cream Milk"
    assert golden["price"] == "$4.50"