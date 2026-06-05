import re
import math
from dataclasses import dataclass, field
from typing import Callable


def _tokenize(text: str) -> set[str]:
    """Lowercase words, strip punctuation."""
    tokens = re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower())
    return {t for t in tokens if t}


def _jaccard(a: str, b: str) -> float:
    """Jaccard similarity between token sets."""
    set_a = _tokenize(a)
    set_b = _tokenize(b)
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def _semantic_diff(answer_a: str, answer_b: str) -> float:
    """Measure how much answer changed: 1.0 = completely different, 0.0 = identical.
    Use 1 - jaccard(answer_a, answer_b).
    """
    return 1.0 - _jaccard(answer_a, answer_b)


def _claim_loss(base_answer: str, new_answer: str) -> list[str]:
    """Find sentences in base_answer that are absent from new_answer.
    Split on '. ', check token overlap < 0.3 for each sentence.
    """
    sentences = base_answer.split(". ")
    lost = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        overlap = _jaccard(sentence, new_answer)
        if overlap < 0.3:
            lost.append(sentence)
    return lost


@dataclass
class AttributionScore:
    passage_id: str           # index as string: "0", "1", etc.
    doc_id: str
    influence: float          # 0-1, how much answer changed without this passage
    semantic_diff: float      # 1 - jaccard(base, counterfactual)
    claim_loss: list[str] = field(default_factory=list)  # lost sentences


@dataclass
class AttributionMap:
    query: str
    base_answer: str
    scores: list[AttributionScore]   # sorted by influence desc
    is_balanced: bool                # True if no passage > 50% influence

    def top_contributor(self) -> "AttributionScore | None":
        """Return highest-influence passage, or None if empty."""
        if not self.scores:
            return None
        return self.scores[0]

    def to_markdown(self) -> str:
        """Markdown report: query, balance status, table of passages by influence."""
        lines = ["# Attribution Map\n"]
        lines.append(f"**Query:** {self.query}\n")
        status = "balanced" if self.is_balanced else "unbalanced (overreliance detected)"
        lines.append(f"**Balance status:** {status}\n")
        lines.append("## Passage Influence\n")
        lines.append("| Passage ID | Doc ID | Influence | Semantic Diff | Claims Lost |")
        lines.append("|-----------|--------|-----------|---------------|-------------|")
        for s in self.scores:
            claims = len(s.claim_loss)
            lines.append(
                f"| {s.passage_id} | {s.doc_id} | {s.influence:.3f} "
                f"| {s.semantic_diff:.3f} | {claims} |"
            )
        return "\n".join(lines)


def counterfactual_attribution(
    query: str,
    base_answer: str,
    passages: list,           # list[Passage] — use .text and .doc_id
    answerer_fn: Callable[[str, list], str] | None = None,
) -> AttributionMap:
    """Leave-one-out attribution.

    For each passage i:
    1. Build subset = passages without passage i
    2. If answerer_fn provided: call answerer_fn(query, subset) → new_answer
       Else: concatenate subset passage texts as surrogate answer
    3. influence = _semantic_diff(base_answer, new_answer)
    4. semantic_diff = influence
    5. claim_loss = _claim_loss(base_answer, new_answer)

    Normalize influences so they sum to 1.0 (if any > 0).
    Sort scores by influence descending.
    is_balanced = max(influence) <= 0.5
    """
    if not passages:
        return AttributionMap(
            query=query,
            base_answer=base_answer,
            scores=[],
            is_balanced=True,
        )

    raw_scores = []
    for i, passage in enumerate(passages):
        subset = [p for j, p in enumerate(passages) if j != i]

        if answerer_fn is not None:
            new_answer = answerer_fn(query, subset)
        else:
            new_answer = " ".join(p.text for p in subset)

        influence = _semantic_diff(base_answer, new_answer)
        claim_loss = _claim_loss(base_answer, new_answer)

        raw_scores.append(AttributionScore(
            passage_id=str(i),
            doc_id=passage.doc_id,
            influence=influence,
            semantic_diff=influence,
            claim_loss=claim_loss,
        ))

    # Normalize influences so they sum to 1.0
    total = sum(s.influence for s in raw_scores)
    if total > 0:
        for s in raw_scores:
            s.influence = s.influence / total
            s.semantic_diff = s.influence

    # Sort by influence descending
    raw_scores.sort(key=lambda s: s.influence, reverse=True)

    max_influence = max(s.influence for s in raw_scores) if raw_scores else 0.0
    is_balanced = max_influence <= 0.5

    return AttributionMap(
        query=query,
        base_answer=base_answer,
        scores=raw_scores,
        is_balanced=is_balanced,
    )


def embedding_attribution(
    query: str,
    base_answer: str,
    passages: list,           # list[Passage]
) -> AttributionMap:
    """Faster approximation: use token overlap(passage, answer) as proxy for influence.

    influence[i] = jaccard(passage[i].text, base_answer)
    Normalize so sum = 1.0.
    No answerer_fn needed.
    """
    if not passages:
        return AttributionMap(
            query=query,
            base_answer=base_answer,
            scores=[],
            is_balanced=True,
        )

    raw_influences = []
    for passage in passages:
        influence = _jaccard(passage.text, base_answer)
        raw_influences.append(influence)

    total = sum(raw_influences)
    if total > 0:
        normalized = [v / total for v in raw_influences]
    else:
        normalized = raw_influences[:]

    scores = []
    for i, (passage, influence) in enumerate(zip(passages, normalized)):
        scores.append(AttributionScore(
            passage_id=str(i),
            doc_id=passage.doc_id,
            influence=influence,
            semantic_diff=influence,
            claim_loss=[],
        ))

    scores.sort(key=lambda s: s.influence, reverse=True)

    max_influence = max(s.influence for s in scores) if scores else 0.0
    is_balanced = max_influence <= 0.5

    return AttributionMap(
        query=query,
        base_answer=base_answer,
        scores=scores,
        is_balanced=is_balanced,
    )
