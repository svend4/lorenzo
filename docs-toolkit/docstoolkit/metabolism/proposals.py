"""High-level rewrite proposals for stale documents.

Sprint 80 / N1 — document metabolism integration helper.

Given a stale document and a pool of fresh source documents (or passages),
produce a `RewriteProposal` recommending which fragments to absorb and
where to insert them.

Stdlib only; no LLM call here — caller plugs in an LLM if they want
actual rewriting. This module produces structured suggestions only.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from docstoolkit.metabolism.absorber import (
    AbsorptionResult,
    absorb_fragment,
)
from docstoolkit.metabolism.aging import age_document, DocAge
from docstoolkit.metabolism.lifecycle import DocLifecycle, LifecycleState
from docstoolkit.metabolism.signals import FreshnessScore


@dataclass
class RewriteFragment:
    """A single fragment that the proposal recommends absorbing."""

    source_doc_id: str
    text: str
    relevance: float
    insertion_hint: str = ""


@dataclass
class RewriteProposal:
    """Outcome of analysing a stale doc against a pool of fresh sources."""

    target_doc_id: str
    target_state: LifecycleState
    target_age: DocAge | None = None
    fragments: list[RewriteFragment] = field(default_factory=list)
    rejected: list[tuple[str, str]] = field(default_factory=list)
    # Suggested merged content if the caller wants a quick text diff
    suggested_content: str = ""

    @property
    def has_changes(self) -> bool:
        return bool(self.fragments)

    def to_markdown(self) -> str:
        lines = [
            f"# Rewrite proposal — `{self.target_doc_id}`",
            "",
            f"State: **{self.target_state.value}**",
        ]
        if self.target_age is not None:
            lines.append(f"Age: {self.target_age.days_since_update:.0f} days")
        lines.append("")
        if self.fragments:
            lines.append("## Proposed insertions")
            for f in self.fragments:
                lines.append(
                    f"- from `{f.source_doc_id}` (relevance {f.relevance:.2f})"
                    + (f" → near `{f.insertion_hint}`" if f.insertion_hint else "")
                )
                lines.append(f"  > {f.text[:200]}")
        else:
            lines.append("_No fragments crossed the absorption threshold._")
        if self.rejected:
            lines.append("")
            lines.append("## Rejected sources")
            for src, reason in self.rejected:
                lines.append(f"- `{src}` — {reason}")
        return "\n".join(lines)


def propose_rewrite(
    target_doc_id: str,
    target_content: str,
    sources: Iterable[tuple[str, str]],
    *,
    last_modified_iso: str = "",
    min_relevance: float = 0.15,
) -> RewriteProposal:
    """Analyse a stale `target` doc against `sources`, return a proposal.

    `sources` is iterable of `(source_doc_id, source_text)` pairs.
    Each source is run through `absorb_fragment()`; absorbed ones are
    captured as fragments, rejected ones are recorded with the reason.
    """
    age = age_document(target_doc_id, target_content, last_modified_iso)
    life = DocLifecycle(doc_id=target_doc_id, content=target_content)
    # Freshness initialised in __post_init__; nudge by age
    if age.days_since_update > 180:
        life.freshness = FreshnessScore(
            doc_id=target_doc_id, score=0.3,
        )
        life.state = LifecycleState.STALE
    elif age.days_since_update > 90:
        life.freshness = FreshnessScore(
            doc_id=target_doc_id, score=0.55,
        )
        life.state = LifecycleState.AGING

    fragments: list[RewriteFragment] = []
    rejected: list[tuple[str, str]] = []
    for src_id, src_text in sources:
        result = absorb_fragment(
            target_content, src_text, doc_id=target_doc_id,
            min_relevance=min_relevance,
        )
        if result.was_absorbed:
            fragments.append(RewriteFragment(
                source_doc_id=src_id,
                text=src_text,
                relevance=result.relevance_score,
                insertion_hint=result.insertion_hint,
            ))
        else:
            rejected.append((src_id, result.reason))

    # Build a naive merged content suggestion (caller may swap in LLM later)
    suggested = target_content.rstrip()
    if fragments:
        suggested += "\n\n## Updates\n"
        for f in fragments:
            suggested += f"\n<!-- absorbed from {f.source_doc_id} -->\n{f.text}\n"

    return RewriteProposal(
        target_doc_id=target_doc_id,
        target_state=life.state,
        target_age=age,
        fragments=fragments,
        rejected=rejected,
        suggested_content=suggested,
    )


def rank_stale_documents(
    docs: Iterable[tuple[str, str, str]],
    *,
    threshold_days: float = 180.0,
) -> list[tuple[str, DocAge]]:
    """Rank `(doc_id, content, last_modified_iso)` triples by staleness.

    Returns list sorted oldest-first, restricted to docs older than threshold.
    """
    aged: list[tuple[str, DocAge]] = []
    for doc_id, content, modified in docs:
        age = age_document(doc_id, content, modified)
        if age.days_since_update > threshold_days:
            aged.append((doc_id, age))
    aged.sort(key=lambda x: -x[1].days_since_update)
    return aged
