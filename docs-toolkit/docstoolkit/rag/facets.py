"""Faceted aggregation over retrieved passages.

Sprint 55 / S2 — facets backend.

Aggregates `Passage` lists across configurable fields and supports
post-retrieval filtering. Stdlib-only; field extractors are pluggable.

Usage:
    from docstoolkit.rag.facets import aggregate_facets, apply_filters

    passages = retriever.search("query", top_k=20)
    facets = aggregate_facets(passages, fields=("section", "tag"))
    # → [FacetAggregation(field="section", values=[("docs", 12), ...]), ...]

    filtered = apply_filters(passages, {"section": "05-habr-projects"})
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence

from docstoolkit.rag.types import Passage


# ---------------------------------------------------------------------------
# Field extractors
# ---------------------------------------------------------------------------

_TAG_RE = re.compile(r"\b(tag|topic|theme):([a-zA-Z0-9_\-/]+)", re.IGNORECASE)
_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def _section(p: Passage) -> list[str]:
    """First path segment of doc_id → section."""
    if not p.doc_id:
        return []
    head = p.doc_id.split("/", 1)[0]
    return [head] if head else []


def _tag(p: Passage) -> list[str]:
    """Extract `tag:foo` markers from passage text."""
    if not p.text:
        return []
    return [m.group(2).lower() for m in _TAG_RE.finditer(p.text)]


def _year(p: Passage) -> list[str]:
    """Pull 4-digit years from text or title."""
    blob = " ".join((p.text or "", p.title or ""))
    return list({m.group(0) for m in _YEAR_RE.finditer(blob)})


def _path_depth(p: Passage) -> list[str]:
    """Tree depth of doc_id (number of path segments) as discrete bucket."""
    if not p.doc_id:
        return []
    return [str(p.doc_id.count("/") + 1)]


DEFAULT_EXTRACTORS: dict[str, Callable[[Passage], list[str]]] = {
    "section": _section,
    "tag": _tag,
    "year": _year,
    "depth": _path_depth,
}


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

@dataclass
class FacetAggregation:
    """Counts of a single facet field over a passage list."""

    field_name: str
    values: list[tuple[str, int]] = field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(c for _, c in self.values)

    def top(self, n: int) -> list[tuple[str, int]]:
        return self.values[:n]

    def to_dict(self) -> dict:
        return {"field": self.field_name, "values": self.values}


def aggregate_facets(
    passages: Sequence[Passage],
    fields: Iterable[str] = ("section", "tag", "year"),
    extractors: dict[str, Callable[[Passage], list[str]]] | None = None,
    top_n: int = 20,
) -> list[FacetAggregation]:
    """Build per-field value counters over `passages`.

    Returns one `FacetAggregation` per requested field, values sorted
    by count descending and truncated to `top_n`.
    """
    merged = dict(DEFAULT_EXTRACTORS)
    if extractors:
        merged.update(extractors)

    out: list[FacetAggregation] = []
    for fname in fields:
        ex = merged.get(fname)
        if ex is None:
            out.append(FacetAggregation(field_name=fname, values=[]))
            continue
        counter: Counter[str] = Counter()
        for p in passages:
            for v in ex(p):
                if v:
                    counter[v] += 1
        most = counter.most_common(top_n)
        out.append(FacetAggregation(field_name=fname, values=most))
    return out


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def apply_filters(
    passages: Sequence[Passage],
    filters: dict[str, str | list[str]],
    extractors: dict[str, Callable[[Passage], list[str]]] | None = None,
) -> list[Passage]:
    """Keep `Passage` objects matching every (field, value) constraint.

    `filters` semantics:
      - value=str → passage's extracted list must include the string
      - value=list → passage's extracted list must include AT LEAST ONE element (OR)
      - multiple fields → AND across fields

    Unknown fields are ignored (returns unfiltered subset for that key).
    """
    if not filters:
        return list(passages)
    merged = dict(DEFAULT_EXTRACTORS)
    if extractors:
        merged.update(extractors)

    out: list[Passage] = []
    for p in passages:
        ok = True
        for fname, expected in filters.items():
            ex = merged.get(fname)
            if ex is None:
                continue
            got = set(ex(p))
            if isinstance(expected, (list, tuple, set)):
                if not (got & set(expected)):
                    ok = False
                    break
            else:
                if expected not in got:
                    ok = False
                    break
        if ok:
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def facet_summary(
    aggregations: Sequence[FacetAggregation],
    top_n: int = 5,
) -> str:
    """Render facets as a one-line summary for logs / dashboards."""
    parts: list[str] = []
    for a in aggregations:
        if not a.values:
            continue
        top = ", ".join(f"{v}={c}" for v, c in a.top(top_n))
        parts.append(f"{a.field_name}[{top}]")
    return " · ".join(parts)
