"""Span-level claim extraction and source linking."""
import re
from dataclasses import dataclass, field

from docstoolkit.provenance.bootstrap import bootstrap_ci


@dataclass
class Source:
    doc_id: str
    passage_text: str
    span: tuple[int, int]    # (start_char, end_char) within passage_text
    similarity: float        # 0-1, token overlap score


@dataclass
class Claim:
    id: str                  # e.g. "claim_0"
    text: str                # the claim sentence
    confidence: float        # 0-1 point estimate
    confidence_ci: tuple[float, float]  # (low, high) 95% CI from bootstrap
    sources: list[Source] = field(default_factory=list)


# Heuristic keywords that indicate factual / noun-like content
_FACTUAL_KEYWORDS = {
    "is", "are", "was", "were", "has", "have", "had", "can", "will",
    "does", "do", "did", "the", "a", "an", "this", "that", "these", "those",
    "он", "она", "оно", "они", "это", "есть", "является", "был", "была",
}


# Phase IV.3 — pre-compile every regex once. Each was being recompiled on
# every claim×passage iteration inside link_sources (M×N matrix), which
# accounted for ~6 μs of the +9 μs provenance overhead in cProfile.
_CITATION_RE = re.compile(r'\[\d+(?:-\d+)?\]')
_WORD_RE = re.compile(r'\b\w+\b')
_TOKEN_RE = re.compile(r'\w+')
_SENT_RE = re.compile(r'(?<=[.!?])[ \t]+|(?<=[.!?])\n+|\n{2,}')
_CLAIM_SENT_RE = re.compile(r'(?<=[.!?])[ \t]+|(?<=[.!?])\n+')


def _strip_citations(text: str) -> str:
    """Remove citation markers like [1], [2-4], [n] from text."""
    return _CITATION_RE.sub('', text).strip()


def _has_noun_like_token(sentence: str) -> bool:
    """Heuristic: sentence has ≥1 word with uppercase letter or known keyword."""
    for w in _WORD_RE.findall(sentence):
        if w[0].isupper() and len(w) > 1:
            return True
        if w.lower() in _FACTUAL_KEYWORDS:
            return True
    return False


def _tokenise(text: str) -> set[str]:
    """Lowercase tokenisation cached at the call site (used heavily in link_sources)."""
    return set(_TOKEN_RE.findall(text.lower()))


def extract_claims(answer_text: str) -> list[str]:
    """Split answer into atomic claims (sentences with factual content).

    Algorithm:
    1. Split on sentence boundaries: '. ', '.\\n', '? ', '! '
    2. Filter: keep sentences that are >= 10 chars and contain a noun-like token
       (heuristic: has >=1 word with uppercase or known keywords)
    3. Strip citations like [1], [2-4], [n]
    4. Return list of claim strings
    """
    if not answer_text or not answer_text.strip():
        return []

    # Split on sentence boundaries
    raw = _CLAIM_SENT_RE.split(answer_text)
    claims = []
    for raw_sentence in raw:
        sentence = _strip_citations(raw_sentence.strip())
        if len(sentence) < 10:
            continue
        if _has_noun_like_token(sentence):
            claims.append(sentence)

    return claims


def _token_overlap(a: str, b: str) -> float:
    """Jaccard token overlap between two strings (lowercased words).

    Phase IV.3 — uses the pre-compiled `_TOKEN_RE` instead of re.findall
    (which had to look up the compiled pattern in the re cache on every
    call). Kept as a thin shim for backwards compatibility — internal
    hot paths use `_token_overlap_pre(tokens_a, b_text)` to avoid
    re-tokenising the same `a` for every passage.
    """
    return _token_overlap_pre(_tokenise(a), b)


def _token_overlap_pre(tokens_a: set[str], b: str) -> float:
    """Variant of `_token_overlap` that takes pre-tokenised `tokens_a`."""
    if not tokens_a:
        return 0.0
    tokens_b = _tokenise(b)
    if not tokens_b:
        return 0.0
    intersection = len(tokens_a & tokens_b)
    union = len(tokens_a | tokens_b)
    return intersection / union if union else 0.0


def _find_best_span_pre(
    claim_tokens: set[str],
    passage_text: str,
) -> tuple[int, int]:
    """Find the sentence in `passage_text` with highest token overlap to claim.

    Phase IV.3 — accepts pre-computed claim tokens to avoid re-tokenising
    the same claim once per passage inside `link_sources`'s M×N loop.

    Returns (start_char, end_char) of the best matching sentence.
    """
    sentences = _SENT_RE.split(passage_text)
    if not sentences:
        return (0, len(passage_text))

    best_score = -1.0
    best_start = 0
    best_end = len(passage_text)
    pos = 0
    for sent in sentences:
        sent_stripped = sent.strip()
        if not sent_stripped:
            pos += len(sent)
            continue
        score = _token_overlap_pre(claim_tokens, sent_stripped)
        start = passage_text.find(sent_stripped, pos)
        if start == -1:
            start = pos
        end = start + len(sent_stripped)
        if score > best_score:
            best_score = score
            best_start = start
            best_end = end
        pos = end
    return (best_start, best_end)


def _find_best_span(claim: str, passage_text: str) -> tuple[int, int]:
    """Backwards-compat shim — see `_find_best_span_pre`."""
    return _find_best_span_pre(_tokenise(claim), passage_text)


def link_sources(
    claims: list[str],
    passages: list,          # list[Passage] — use .text and .doc_id
    *,
    min_similarity: float = 0.1,
) -> list[Claim]:
    """Link each claim to supporting passage spans.

    For each (claim, passage) pair:
    1. Compute _token_overlap(claim, passage.text)
    2. If overlap >= min_similarity: find best matching span within passage
       (find the sentence in passage.text with highest overlap to claim)
    3. Assign Source with span=(start, end) chars in passage.text

    confidence = max similarity across all sources (or 0 if no sources)
    confidence_ci = bootstrap_ci(similarities, n_bootstrap=100) if sources else (0, 0)
    """
    result: list[Claim] = []

    # Phase IV.3 — pre-tokenise every passage once (was N×M in the loop).
    passage_tokens = [_tokenise(p.text) for p in passages]

    for idx, claim_text in enumerate(claims):
        # Pre-tokenise the claim once; reused for both overlap and best-span.
        claim_tokens = _tokenise(claim_text)
        sources: list[Source] = []

        for p_idx, passage in enumerate(passages):
            pt = passage_tokens[p_idx]
            if not claim_tokens or not pt:
                continue
            inter = len(claim_tokens & pt)
            uni = len(claim_tokens | pt)
            sim = inter / uni if uni else 0.0
            if sim >= min_similarity:
                span = _find_best_span_pre(claim_tokens, passage.text)
                sources.append(Source(
                    doc_id=passage.doc_id,
                    passage_text=passage.text,
                    span=span,
                    similarity=sim,
                ))

        if sources:
            similarities = [s.similarity for s in sources]
            confidence = max(similarities)
            ci = bootstrap_ci(similarities, n_bootstrap=100)
            confidence_ci = (ci.ci_low, ci.ci_high)
        else:
            confidence = 0.0
            confidence_ci = (0.0, 0.0)

        result.append(Claim(
            id=f"claim_{idx}",
            text=claim_text,
            confidence=confidence,
            confidence_ci=confidence_ci,
            sources=sources,
        ))

    return result
