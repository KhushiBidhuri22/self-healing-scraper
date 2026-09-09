from app.candidate_generator import generate_candidates
from app.scorer import score_candidate
from app.replay import replay_candidate
from app.selector_promoter import promote_selector
from app.repair_logger import log_repair


PROMOTION_THRESHOLD = 90


def heal_selector(
    html: str,
    field: str,
    expected_value: str,
    current_selectors: dict,
) -> dict:

    
    candidates = generate_candidates(html, field)

    scored_candidates = []

    for candidate in candidates:
        result = score_candidate(
          html,
          candidate,
          expected_value,
          field,
      )

        scored_candidates.append(result)

   
    if not scored_candidates:
        return {
            "healed": False,
            "reason": "No candidates generated",
        }

  
    best_candidate = max(
        scored_candidates,
        key=lambda candidate: candidate["score"],
    )

  
    if best_candidate["score"] < PROMOTION_THRESHOLD:
        return {
            "healed": False,
            "reason": "No candidate reached the required score",
            "best_candidate": best_candidate,
        }


    replay = replay_candidate(
        html=html,
        selector=best_candidate["selector"],
        expected_value=expected_value,
    )

    if not replay["passed"]:
        return {
            "healed": False,
            "reason": f"Replay validation failed: {replay['reason']}",
            "best_candidate": best_candidate,
            "replay": replay,
        }

    
    old_selector = current_selectors["fields"].get(field)

    promoted = promote_selector(
        current_selectors,
        field,
        best_candidate["selector"],
    )

    repair = log_repair(
        field=field,
        old_selector=old_selector,
        new_selector=best_candidate["selector"],
        score=best_candidate["score"],
        evidence=best_candidate["reasons"],
        new_version=promoted["version"],
    )

    return {
    "healed": True,
    "field": field,
    "old_selector": old_selector,
    "new_selector": best_candidate["selector"],
    "score": best_candidate["score"],
    "evidence": best_candidate["reasons"],
    "new_version": promoted["version"],
    "selectors": promoted,
    "repair": repair,
    "replay": replay,
}