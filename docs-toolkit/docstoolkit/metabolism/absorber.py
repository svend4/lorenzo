import re
from dataclasses import dataclass


@dataclass
class AbsorptionResult:
    """Result of absorbing a new fragment into a document."""
    doc_id: str
    fragment_text: str
    was_absorbed: bool
    reason: str              # why absorbed or rejected
    relevance_score: float   # 0-1, Jaccard similarity to doc content
    insertion_hint: str = "" # suggested section/heading to insert near


def absorb_fragment(
    doc_content: str,
    fragment: str,
    doc_id: str = "",
    min_relevance: float = 0.15,
) -> AbsorptionResult:
    """Decide if a new fragment should be absorbed into doc.

    Algorithm:
    1. Compute Jaccard token overlap between fragment and doc_content
    2. If overlap >= min_relevance: absorbed = True
    3. Find best matching heading in doc (lines starting with #) by overlap with fragment
    4. insertion_hint = that heading, or "" if no headings
    5. reason = "relevant (score=X.XX)" or "below threshold (score=X.XX)"
    """
    frag_tokens = _token_set(fragment)
    doc_tokens = _token_set(doc_content)
    score = _jaccard(frag_tokens, doc_tokens)

    absorbed = score >= min_relevance

    if absorbed:
        reason = f"relevant (score={score:.2f})"
    else:
        reason = f"below threshold (score={score:.2f})"

    # Find best matching heading
    insertion_hint = ""
    headings = [line.rstrip() for line in doc_content.splitlines()
                if line.startswith("#")]
    if headings:
        best_heading = ""
        best_score = -1.0
        for heading in headings:
            h_tokens = _token_set(heading)
            h_score = _jaccard(frag_tokens, h_tokens)
            if h_score > best_score:
                best_score = h_score
                best_heading = heading
        insertion_hint = best_heading

    return AbsorptionResult(
        doc_id=doc_id,
        fragment_text=fragment,
        was_absorbed=absorbed,
        reason=reason,
        relevance_score=score,
        insertion_hint=insertion_hint,
    )


def _token_set(text: str) -> set:
    """Lowercase word tokens from text, min length 3."""
    return set(w.lower() for w in re.findall(r'\b\w{3,}\b', text))


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0
