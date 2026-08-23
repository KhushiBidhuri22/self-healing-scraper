from app.candidate_generator import generate_candidates


def test_generate_name_candidates():
    html = """
    <html>
        <body>
            <h2 class="title">Full Cream Milk</h2>
        </body>
    </html>
    """

    candidates = generate_candidates(html, "name")

    assert ".title" in candidates
    assert "h2.title" in candidates
    assert "h2" in candidates