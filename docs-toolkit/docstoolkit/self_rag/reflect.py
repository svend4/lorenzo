"""Rule-based reflection scoring for Self-RAG (no LLM needed)."""
import re
from dataclasses import dataclass, field


@dataclass
class ReflectScore:
    score: float                      # 0-10
    missing_topics: list[str]         # topics from question not covered in answer
    contradictions: list[str]         # flagged contradictions (simple heuristic)
    suggested_query: str              # reformulated query if score < threshold
    decision: str                     # "answer_ok" | "answer_insufficient"


def _token_overlap(a: str, b: str) -> float:
    """Jaccard overlap between word sets."""
    set_a = set(re.findall(r'\b\w+\b', a.lower()))
    set_b = set(re.findall(r'\b\w+\b', b.lower()))
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def _extract_key_terms(text: str) -> set[str]:
    """Extract significant words (>= 4 chars, not stopwords)."""
    STOPWORDS = {
        "это", "для", "что", "как", "или", "при", "без", "над",
        "под", "про", "все", "они", "его", "ее", "the", "and",
        "for", "with", "that", "this", "from", "are", "was", "were",
    }
    words = re.findall(r'\b\w{4,}\b', text.lower())
    return {w for w in words if w not in STOPWORDS}


def reflect_on_answer(
    question: str,
    answer: str,
    passages: list,                   # list[Passage]
    *,
    reflect_threshold: float = 7.0,
) -> ReflectScore:
    """Rule-based reflection scoring (no LLM needed).

    Algorithm:
    1. Coverage score (0-10):
       - Extract key terms from question
       - Count how many appear in answer (term coverage ratio)
       - score = 10 * (covered / total_terms) if total_terms > 0 else 5.0

    2. Source support score (0-10):
       - For each key term: does any passage mention it?
       - source_support = 10 * (supported_terms / total_terms)

    3. Final score = 0.6 * coverage_score + 0.4 * source_support_score

    4. missing_topics = key terms from question not in answer (max 3)

    5. contradictions = [] (heuristic: detect obvious negation patterns)

    6. suggested_query = question + " " + " ".join(missing_topics[:2])
       if missing_topics else question

    7. decision = "answer_ok" if score >= reflect_threshold else "answer_insufficient"
    """
    question_terms = _extract_key_terms(question)
    total_terms = len(question_terms)

    if total_terms == 0:
        # No key terms in question — give a neutral score
        coverage_score = 5.0
        source_support_score = 5.0
    else:
        # 1. Coverage: how many question terms appear in the answer?
        answer_lower = answer.lower()
        covered_terms = {t for t in question_terms if t in answer_lower}
        coverage_score = 10.0 * (len(covered_terms) / total_terms)

        # 2. Source support: how many question terms appear in any passage?
        all_passage_text = " ".join(
            getattr(p, "text", str(p)).lower() for p in passages
        )
        supported_terms = {t for t in question_terms if t in all_passage_text}
        source_support_score = 10.0 * (len(supported_terms) / total_terms)

    # 3. Weighted final score
    score = 0.6 * coverage_score + 0.4 * source_support_score

    # 4. Missing topics (terms from question not in answer), max 3
    if total_terms > 0:
        answer_lower = answer.lower()
        missing = [t for t in sorted(question_terms) if t not in answer_lower][:3]
    else:
        missing = []

    # 5. Contradictions — simple heuristic: look for negation near a passage term
    contradictions: list[str] = []
    if answer and passages:
        all_passage_text_lower = " ".join(
            getattr(p, "text", str(p)).lower() for p in passages
        )
        answer_lower_check = answer.lower()
        # Detect patterns like "нет X" or "not X" where X is mentioned in passages
        negation_pattern = re.compile(r'\b(нет|not|никак|never|нельзя)\s+(\w{4,})')
        for m in negation_pattern.finditer(answer_lower_check):
            negated_word = m.group(2)
            if negated_word in all_passage_text_lower:
                contradictions.append(
                    f"Answer negates '{negated_word}' which appears in passages"
                )

    # 6. Suggested query
    if missing:
        suggested_query = question + " " + " ".join(missing[:2])
    else:
        suggested_query = question

    # 7. Decision
    decision = "answer_ok" if score >= reflect_threshold else "answer_insufficient"

    return ReflectScore(
        score=score,
        missing_topics=missing,
        contradictions=contradictions,
        suggested_query=suggested_query,
        decision=decision,
    )
