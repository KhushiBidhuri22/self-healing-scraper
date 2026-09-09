from app.candidate_generator import generate_candidates
def test_generate_price_candidates():

    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <div class="product-cost">$4.50</div>
    </div>
    """

    candidates = generate_candidates(
        html,
        "price"
    )

    assert ".product-cost" in candidates
    assert "div.product-cost" in candidates


def test_generate_rating_candidates():

    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <span class="rating">4.5</span>
    </div>
    """

    candidates = generate_candidates(
        html,
        "rating"
    )

    assert ".rating" in candidates


def test_generate_review_count_candidates():

    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <span class="review-count">1200</span>
    </div>
    """

    candidates = generate_candidates(
        html,
        "review_count"
    )

    assert ".review-count" in candidates

def test_generate_id_candidates():

    html = """
    <div class="product">
        <h2 class="product-name">Full Cream Milk</h2>
        <div id="product-price">$4.50</div>
    </div>
    """

    candidates = generate_candidates(
        html,
        "price"
    )

    assert "#product-price" in candidates
    assert "div#product-price" in candidates