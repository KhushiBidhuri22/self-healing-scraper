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