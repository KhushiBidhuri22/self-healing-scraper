from app.replay import replay_candidate


HTML = """
<div class="product">
    <h2 class="title">Full Cream Milk</h2>
    <span class="price">$4.50</span>
</div>
"""


def test_replay_success():
    result = replay_candidate(
        HTML,
        ".title",
        "Full Cream Milk",
    )

    assert result["passed"] is True


def test_replay_wrong_value():
    result = replay_candidate(
        HTML,
        ".title",
        "Chocolate Milk",
    )

    assert result["passed"] is False


def test_replay_missing_selector():
    result = replay_candidate(
        HTML,
        ".does-not-exist",
        "Full Cream Milk",
    )

    assert result["passed"] is False