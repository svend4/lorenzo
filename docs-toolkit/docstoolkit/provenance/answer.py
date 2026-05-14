"""ProvenancedAnswer: RAG answer with span-level provenance."""
from dataclasses import dataclass, field

from docstoolkit.provenance.claims import Claim, extract_claims, link_sources


@dataclass
class ProvenancedAnswer:
    text: str                        # original answer text
    claims: list[Claim]
    overall_confidence: float        # mean of claim confidences

    def to_markdown(self) -> str:
        """Format claims with inline confidence scores.

        Format:
        ## Answer
        <text>

        ## Claims
        1. <claim text> — confidence: 0.82 (CI: 0.71–0.91) | sources: doc1, doc2
        ...
        """
        lines = ["## Answer", self.text, "", "## Claims"]
        for i, claim in enumerate(self.claims, 1):
            ci_low, ci_high = claim.confidence_ci
            source_ids = ", ".join(s.doc_id for s in claim.sources) if claim.sources else "none"
            lines.append(
                f"{i}. {claim.text} — confidence: {claim.confidence:.2f} "
                f"(CI: {ci_low:.2f}–{ci_high:.2f}) | sources: {source_ids}"
            )
        return "\n".join(lines)

    def high_confidence_claims(self, threshold: float = 0.7) -> list[Claim]:
        """Return only claims with confidence >= threshold."""
        return [c for c in self.claims if c.confidence >= threshold]


def ask_with_provenance(
    question: str,
    answer_text: str,
    passages: list,    # list[Passage]
    *,
    min_similarity: float = 0.1,
    bootstrap_samples: int = 200,
) -> ProvenancedAnswer:
    """Build a ProvenancedAnswer from an existing answer + passages.

    Steps:
    1. extract_claims(answer_text) -> list[str]
    2. link_sources(claims, passages, min_similarity=min_similarity) -> list[Claim]
    3. Compute overall_confidence = mean(claim.confidence for claim in claims)
       or 0.0 if no claims
    4. Return ProvenancedAnswer
    """
    claim_texts = extract_claims(answer_text)
    claims = link_sources(claim_texts, passages, min_similarity=min_similarity)

    if claims:
        overall_confidence = sum(c.confidence for c in claims) / len(claims)
    else:
        overall_confidence = 0.0

    return ProvenancedAnswer(
        text=answer_text,
        claims=claims,
        overall_confidence=overall_confidence,
    )
