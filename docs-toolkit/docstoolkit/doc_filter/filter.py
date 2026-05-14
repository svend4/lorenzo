"""Doc filter implementation — stdlib only."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FilterOp(Enum):
    """Supported filter operators."""

    EQ = "eq"
    NE = "ne"
    LT = "lt"
    LE = "le"
    GT = "gt"
    GE = "ge"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    MATCHES = "matches"
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"


@dataclass
class FilterCondition:
    """A single filter condition.

    Attributes
    ----------
    field
        Dotted path like ``"title"`` or ``"metadata.author"``.
    op
        Operator from :class:`FilterOp`.
    value
        Comparison value (unused for EXISTS/NOT_EXISTS).
    """

    field: str
    op: FilterOp
    value: Any = None


@dataclass
class Document:
    """Document representation."""

    doc_id: str
    content: str
    metadata: dict = field(default_factory=dict)


@dataclass
class FilterResult:
    """Result of a filter operation."""

    matched: list
    total_input: int

    @property
    def match_count(self) -> int:
        return len(self.matched)

    @property
    def match_rate(self) -> float:
        if self.total_input <= 0:
            return 0.0
        return self.match_count / self.total_input


# Sentinel used to mark "field missing".
_MISSING = object()


def _get_field(doc: Document, path: str) -> Any:
    """Resolve dotted field path against a Document.

    Special handling:
    - ``"content"`` → ``doc.content``
    - ``"doc_id"`` → ``doc.doc_id``
    - ``"metadata"`` (or anything else) → walked through ``doc.metadata`` /
      nested dicts / attributes.

    Returns ``_MISSING`` sentinel if any path segment is absent.
    """
    if not path:
        return _MISSING

    parts = path.split(".")
    head, rest = parts[0], parts[1:]

    if head == "content":
        current: Any = doc.content
    elif head == "doc_id":
        current = doc.doc_id
    elif head == "metadata":
        current = doc.metadata
        if not rest:
            return current
    else:
        # Treat top-level non-special keys as metadata lookups by default.
        if head in doc.metadata:
            current = doc.metadata[head]
        elif hasattr(doc, head):
            current = getattr(doc, head)
        else:
            return _MISSING

    for seg in rest:
        if current is None:
            return _MISSING
        if isinstance(current, dict):
            if seg in current:
                current = current[seg]
            else:
                return _MISSING
        elif hasattr(current, seg):
            current = getattr(current, seg)
        else:
            return _MISSING

    return current


def _apply_op(value: Any, op: FilterOp, target: Any) -> bool:
    """Apply operator to (value, target). ``value`` may be ``_MISSING``."""
    if op is FilterOp.NOT_EXISTS:
        return value is _MISSING or value is None
    if op is FilterOp.EXISTS:
        return value is not _MISSING and value is not None

    if value is _MISSING:
        return False

    try:
        if op is FilterOp.EQ:
            return value == target
        if op is FilterOp.NE:
            return value != target
        if op is FilterOp.LT:
            return value < target
        if op is FilterOp.LE:
            return value <= target
        if op is FilterOp.GT:
            return value > target
        if op is FilterOp.GE:
            return value >= target
        if op is FilterOp.IN:
            if target is None:
                return False
            return value in target
        if op is FilterOp.NOT_IN:
            if target is None:
                return True
            return value not in target
        if op is FilterOp.CONTAINS:
            if value is None:
                return False
            if isinstance(value, str):
                if not isinstance(target, str):
                    return False
                return target in value
            if isinstance(value, (list, tuple, set, dict)):
                return target in value
            return False
        if op is FilterOp.NOT_CONTAINS:
            if value is None:
                return True
            if isinstance(value, str):
                if not isinstance(target, str):
                    return True
                return target not in value
            if isinstance(value, (list, tuple, set, dict)):
                return target not in value
            return True
        if op is FilterOp.STARTSWITH:
            if not isinstance(value, str) or not isinstance(target, str):
                return False
            return value.startswith(target)
        if op is FilterOp.ENDSWITH:
            if not isinstance(value, str) or not isinstance(target, str):
                return False
            return value.endswith(target)
        if op is FilterOp.MATCHES:
            if not isinstance(value, str) or not isinstance(target, str):
                return False
            return re.search(target, value) is not None
    except TypeError:
        return False

    return False


def _matches(doc: Document, cond: FilterCondition) -> bool:
    val = _get_field(doc, cond.field)
    return _apply_op(val, cond.op, cond.value)


class DocFilter:
    """Filter engine for collections of documents."""

    def __init__(self) -> None:
        pass

    # --- core API ----------------------------------------------------------

    def filter(
        self,
        docs: list,
        conditions: list,
        mode: str = "AND",
    ) -> FilterResult:
        """Apply a list of conditions joined by ``mode`` (AND/OR)."""
        mode_upper = (mode or "AND").upper()
        if mode_upper not in {"AND", "OR"}:
            raise ValueError(f"Unknown mode: {mode!r}; expected AND or OR")

        if not conditions:
            # No conditions: in AND-mode everything matches, in OR-mode nothing.
            if mode_upper == "AND":
                return FilterResult(matched=list(docs), total_input=len(docs))
            return FilterResult(matched=[], total_input=len(docs))

        matched: list = []
        for doc in docs:
            results = [_matches(doc, c) for c in conditions]
            if mode_upper == "AND":
                ok = all(results)
            else:
                ok = any(results)
            if ok:
                matched.append(doc)
        return FilterResult(matched=matched, total_input=len(docs))

    def filter_one(
        self, docs: list, condition: FilterCondition
    ) -> FilterResult:
        """Filter by a single condition."""
        return self.filter(docs, [condition], mode="AND")

    def filter_by_field(
        self,
        docs: list,
        field: str,
        value: Any,
        op: FilterOp = FilterOp.EQ,
    ) -> FilterResult:
        """Filter by a single field/op/value triple."""
        return self.filter_one(docs, FilterCondition(field=field, op=op, value=value))

    def filter_by_content(
        self,
        docs: list,
        substring: str,
        case_sensitive: bool = False,
    ) -> FilterResult:
        """Filter documents whose ``content`` contains ``substring``."""
        matched: list = []
        if case_sensitive:
            needle = substring
            for d in docs:
                if isinstance(d.content, str) and needle in d.content:
                    matched.append(d)
        else:
            needle = substring.lower() if isinstance(substring, str) else substring
            for d in docs:
                if isinstance(d.content, str) and isinstance(needle, str):
                    if needle in d.content.lower():
                        matched.append(d)
        return FilterResult(matched=matched, total_input=len(docs))

    def filter_by_regex(self, docs: list, pattern: str) -> FilterResult:
        """Filter documents whose ``content`` matches ``pattern`` via ``re.search``."""
        rx = re.compile(pattern)
        matched = [d for d in docs if isinstance(d.content, str) and rx.search(d.content)]
        return FilterResult(matched=matched, total_input=len(docs))

    def filter_by_metadata(
        self, docs: list, key: str, value: Any
    ) -> FilterResult:
        """Equality filter over a (possibly dotted) metadata key."""
        path = key if key.startswith("metadata.") else f"metadata.{key}"
        return self.filter_by_field(docs, path, value, FilterOp.EQ)

    # --- ordering & paging -------------------------------------------------

    def sort_by(
        self,
        docs: list,
        field: str,
        reverse: bool = False,
    ) -> list:
        """Stable sort by a field path. Missing/None values sink to the end."""

        def _key(doc):
            val = _get_field(doc, field)
            if val is _MISSING or val is None:
                # Place missing values at the end (whichever direction).
                return (1, None)
            return (0, val)

        try:
            return sorted(docs, key=_key, reverse=reverse)
        except TypeError:
            # Fallback when values are not mutually comparable: coerce to str.
            def _key_str(doc):
                val = _get_field(doc, field)
                if val is _MISSING or val is None:
                    return (1, "")
                return (0, str(val))

            return sorted(docs, key=_key_str, reverse=reverse)

    def limit(self, docs: list, n: int, offset: int = 0) -> list:
        """Slice ``docs`` to ``[offset : offset + n]``."""
        if n < 0:
            n = 0
        if offset < 0:
            offset = 0
        return list(docs[offset : offset + n])

    def paginate(
        self, docs: list, page: int, page_size: int
    ) -> tuple:
        """Return ``(page_docs, total_pages)`` for 1-based ``page``."""
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        if page < 1:
            page = 1
        total = len(docs)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        start = (page - 1) * page_size
        end = start + page_size
        return list(docs[start:end]), total_pages
