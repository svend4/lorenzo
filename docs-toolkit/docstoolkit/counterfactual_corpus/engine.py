"""Counterfactual corpus engine: sandbox analysis of document removal/addition."""
import re
from dataclasses import dataclass, field
from typing import Callable


def _token_overlap(a: str, b: str) -> float:
    """Jaccard token overlap between two strings."""
    tokens_a = set(re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", a.lower()))
    tokens_b = set(re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", b.lower()))
    if not tokens_a and not tokens_b:
        return 1.0
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def _rank_passages(
    query: str,
    passages: list,  # list[Passage-like with .text, .doc_id]
) -> list[tuple[str, float]]:
    """Simple TF-IDF-like ranking. Returns [(doc_id, score)] sorted desc."""
    query_tokens = set(re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", query.lower()))
    results: list[tuple[str, float]] = []

    for passage in passages:
        doc_tokens = set(re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", passage.text.lower()))
        if not doc_tokens:
            score = 0.0
        else:
            intersection = query_tokens & doc_tokens
            union = query_tokens | doc_tokens
            score = len(intersection) / len(union) if union else 0.0
        results.append((passage.doc_id, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def _rank_docs(
    query: str,
    docs: dict[str, str],
) -> list[tuple[str, float]]:
    """Rank docs dict by relevance to query. Returns [(doc_id, score)] sorted desc."""
    query_tokens = set(re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", query.lower()))
    results: list[tuple[str, float]] = []

    for doc_id, content in docs.items():
        doc_tokens = set(re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", content.lower()))
        if not doc_tokens:
            score = 0.0
        else:
            intersection = query_tokens & doc_tokens
            union = query_tokens | doc_tokens
            score = len(intersection) / len(union) if union else 0.0
        results.append((doc_id, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


@dataclass
class QueryDelta:
    query: str
    baseline_top_doc: str   # doc_id that was #1 before
    new_top_doc: str        # doc_id that is #1 after
    rank_shift: int         # how much target doc shifted (if still present)
    affected: bool          # True if top-1 changed


@dataclass
class DecisionDelta:
    decision_text: str  # text of the decision/link
    source_doc: str     # the removed doc
    severity: str       # "critical" | "moderate" | "minor"


@dataclass
class CounterfactualReport:
    action: str                         # "remove" | "add"
    target_doc: str                     # doc_id affected
    affected_queries: list[QueryDelta]
    affected_decisions: list[DecisionDelta]
    cascade_docs: list[str]             # doc_ids that cited target
    severity: str                       # "low" | "medium" | "high" | "critical"
    summary: str

    def to_markdown(self) -> str:
        """Human-readable markdown report."""
        lines = [
            f"# Counterfactual Report: {self.action.upper()} `{self.target_doc}`\n",
            f"**Action:** {self.action}",
            f"**Target doc:** {self.target_doc}",
            f"**Severity:** {self.severity}",
            f"**Summary:** {self.summary}",
            "",
        ]

        if self.affected_queries:
            lines.append("## Affected Queries\n")
            lines.append("| Query | Baseline Top | New Top | Shift | Affected |")
            lines.append("|-------|-------------|---------|-------|----------|")
            for qd in self.affected_queries:
                lines.append(
                    f"| {qd.query} | {qd.baseline_top_doc} | {qd.new_top_doc} "
                    f"| {qd.rank_shift} | {qd.affected} |"
                )
            lines.append("")

        if self.affected_decisions:
            lines.append("## Affected Decisions\n")
            lines.append("| Decision | Source Doc | Severity |")
            lines.append("|----------|-----------|----------|")
            for dd in self.affected_decisions:
                lines.append(
                    f"| {dd.decision_text[:60]} | {dd.source_doc} | {dd.severity} |"
                )
            lines.append("")

        if self.cascade_docs:
            lines.append("## Cascade Documents\n")
            for doc_id in self.cascade_docs:
                lines.append(f"- {doc_id}")
            lines.append("")

        return "\n".join(lines)


def _classify_severity(
    n_affected_queries: int,
    n_cascade_docs: int,
) -> str:
    """
    critical: > 5 queries or > 3 cascade docs
    high: > 2 queries or > 1 cascade doc
    medium: 1-2 queries
    low: 0 queries
    """
    if n_affected_queries > 5 or n_cascade_docs > 3:
        return "critical"
    if n_affected_queries > 2 or n_cascade_docs > 1:
        return "high"
    if n_affected_queries >= 1:
        return "medium"
    return "low"


def counterfactual_remove(
    target_doc_id: str,
    docs: dict[str, str],               # {doc_id: content} — full corpus
    queries: list[str],                  # test queries to evaluate
    *,
    decisions: list[str] | None = None,  # texts referencing doc_ids (for decision delta)
) -> CounterfactualReport:
    """Sandbox: what happens if we remove target_doc_id?

    Algorithm:
    1. For each query: rank all docs, rank docs_without_target
       If top-1 changes → QueryDelta(affected=True)
    2. For each decision text: if it contains target_doc_id → DecisionDelta
       severity based on how many other docs can replace it
    3. cascade_docs: docs in corpus whose content mentions target_doc_id
    4. severity = _classify_severity(affected_queries, cascade_docs)
    5. summary: "Removing {doc_id} affects {n} queries and {m} cascade docs"

    Return CounterfactualReport(action="remove", ...)
    """
    docs_without = {k: v for k, v in docs.items() if k != target_doc_id}

    # Step 1: evaluate queries
    query_deltas: list[QueryDelta] = []
    for query in queries:
        baseline_ranked = _rank_docs(query, docs)
        new_ranked = _rank_docs(query, docs_without)

        baseline_top = baseline_ranked[0][0] if baseline_ranked else ""
        new_top = new_ranked[0][0] if new_ranked else ""

        # Find rank shift: original rank of target_doc in baseline vs new
        baseline_rank = next(
            (i for i, (doc_id, _) in enumerate(baseline_ranked) if doc_id == target_doc_id),
            -1,
        )
        # target is removed so we track how far down the replacement fell
        # rank_shift = difference in position for the baseline_top_doc after removal
        baseline_top_new_rank = next(
            (i for i, (doc_id, _) in enumerate(new_ranked) if doc_id == baseline_top),
            -1,
        )
        rank_shift = baseline_top_new_rank - (0 if baseline_top != target_doc_id else 0)
        if baseline_top == target_doc_id:
            rank_shift = 0  # target is removed; use how much the new top shifted

        affected = baseline_top != new_top

        query_deltas.append(QueryDelta(
            query=query,
            baseline_top_doc=baseline_top,
            new_top_doc=new_top,
            rank_shift=rank_shift,
            affected=affected,
        ))

    # Step 2: decision deltas
    decision_deltas: list[DecisionDelta] = []
    if decisions:
        for decision_text in decisions:
            if target_doc_id in decision_text:
                # Check how many other docs could replace: count docs with similar content
                target_content = docs.get(target_doc_id, "")
                replaceable_count = sum(
                    1 for doc_id, content in docs_without.items()
                    if _token_overlap(target_content, content) > 0.3
                )
                if replaceable_count == 0:
                    sev = "critical"
                elif replaceable_count <= 2:
                    sev = "moderate"
                else:
                    sev = "minor"
                decision_deltas.append(DecisionDelta(
                    decision_text=decision_text,
                    source_doc=target_doc_id,
                    severity=sev,
                ))

    # Step 3: cascade_docs — docs in corpus that mention target_doc_id
    cascade_docs: list[str] = [
        doc_id for doc_id, content in docs_without.items()
        if target_doc_id in content
    ]

    # Step 4: severity
    n_affected = sum(1 for qd in query_deltas if qd.affected)
    severity = _classify_severity(n_affected, len(cascade_docs))

    # Step 5: summary
    summary = (
        f"Removing {target_doc_id} affects {n_affected} "
        f"quer{'y' if n_affected == 1 else 'ies'} "
        f"and {len(cascade_docs)} cascade doc{'s' if len(cascade_docs) != 1 else ''}."
    )

    return CounterfactualReport(
        action="remove",
        target_doc=target_doc_id,
        affected_queries=query_deltas,
        affected_decisions=decision_deltas,
        cascade_docs=cascade_docs,
        severity=severity,
        summary=summary,
    )


def counterfactual_add(
    new_doc_id: str,
    new_doc_content: str,
    docs: dict[str, str],
    queries: list[str],
) -> CounterfactualReport:
    """Sandbox: what changes if we add new_doc_id?

    Algorithm:
    1. docs_with_new = {**docs, new_doc_id: new_doc_content}
    2. For each query: rank original → rank with new
       If new_doc appears in top-1 → QueryDelta(affected=True, new_top_doc=new_doc_id)
    3. cascade_docs = [] (new doc has no citations yet)
    4. Return CounterfactualReport(action="add", ...)
    """
    docs_with_new = {**docs, new_doc_id: new_doc_content}

    query_deltas: list[QueryDelta] = []
    for query in queries:
        baseline_ranked = _rank_docs(query, docs)
        new_ranked = _rank_docs(query, docs_with_new)

        baseline_top = baseline_ranked[0][0] if baseline_ranked else ""
        new_top = new_ranked[0][0] if new_ranked else ""

        # Rank shift: how far the new doc is in new_ranked
        new_doc_rank = next(
            (i for i, (doc_id, _) in enumerate(new_ranked) if doc_id == new_doc_id),
            -1,
        )
        rank_shift = new_doc_rank  # 0 = new doc is at top

        affected = new_top == new_doc_id

        query_deltas.append(QueryDelta(
            query=query,
            baseline_top_doc=baseline_top,
            new_top_doc=new_top,
            rank_shift=rank_shift,
            affected=affected,
        ))

    cascade_docs: list[str] = []

    n_affected = sum(1 for qd in query_deltas if qd.affected)
    severity = _classify_severity(n_affected, 0)

    summary = (
        f"Adding {new_doc_id} affects {n_affected} "
        f"quer{'y' if n_affected == 1 else 'ies'} "
        f"and 0 cascade docs."
    )

    return CounterfactualReport(
        action="add",
        target_doc=new_doc_id,
        affected_queries=query_deltas,
        affected_decisions=[],
        cascade_docs=cascade_docs,
        severity=severity,
        summary=summary,
    )
