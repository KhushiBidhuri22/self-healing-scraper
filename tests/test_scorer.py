from app.scorer import score_candidate


def test_good_candidate_gets_high_score():
    html = """
    <html>
        <body>
            <h2 class="title">Full Cream Milk</h2>
        </body>
    </html>
    """

    result = score_candidate(
        html,
        "h2.title",
        "Full Cream Milk",
    )

    assert result["matched"] is True
    assert result["score"] == 100

def test_bad_candidate_gets_zero_score():
    html = """
    <html>
        <body>
            <h2 class="title">Full Cream Milk</h2>
        </body>
    </html>
    """

    result = score_candidate(
        html,
        ".does-not-exist",
        "Full Cream Milk",
    )

    assert result["matched"] is False
    assert result["score"] == 0

def test_semantic_price_candidate_gets_extra_evidence():

    html = """
    <html>
        <body>
            <div class="product-cost">$4.50</div>
        </body>
    </html>
    """

    result = score_candidate(
        html,
        ".product-cost",
        "$4.50",
        "price",
    )

    assert result["matched"] is True
    assert result["score"] == 100
    assert "selector matches field semantics" in result["reasons"]


def test_non_semantic_candidate_does_not_get_semantic_bonus():

    html = """
    <html>
        <body>
            <div class="random-box">$4.50</div>
        </body>
    </html>
    """

    result = score_candidate(
        html,
        ".random-box",
        "$4.50",
        "price",
    )

    assert result["matched"] is True
    assert "selector matches field semantics" not in result["reasons"]