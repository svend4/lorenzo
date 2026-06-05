"""Hierarchical corpus summarization — stdlib only."""
from dataclasses import dataclass, field
from pathlib import Path
from docstoolkit.summarize.extractor import textrank_summary, SummaryCache
from docstoolkit.summarize.reducer import reduce_summaries, cluster_summaries


@dataclass
class HierarchicalSummary:
    topic: str
    summary: str
    sources: list  # doc paths / titles contributing to this summary
    sub_summaries: list = field(default_factory=list)
    coverage: float = 0.0  # fraction of input docs included

    def to_markdown(self, indent: int = 0) -> str:
        """Recursive markdown rendering.

        ## {topic}
        {summary}
        Sources: {sources}

        ### sub_topic_1
        ...
        """
        level = indent + 2
        heading = "#" * level
        lines = [
            f"{heading} {self.topic}",
            "",
            self.summary,
            "",
            f"Sources: {', '.join(self.sources)}",
        ]
        for sub in self.sub_summaries:
            lines.append("")
            lines.append(sub.to_markdown(indent=indent + 1))
        return "\n".join(lines)

    def all_sources(self) -> list:
        """Recursively collect all source paths."""
        result = list(self.sources)
        for sub in self.sub_summaries:
            result.extend(sub.all_sources())
        return result

    def depth(self) -> int:
        """Max nesting depth (1 if no sub_summaries)."""
        if not self.sub_summaries:
            return 1
        return 1 + max(sub.depth() for sub in self.sub_summaries)


def summarize_corpus(
    docs: dict,  # {path_or_title: content}
    *,
    query: str = "",
    max_summary_length: int = 2000,
    n_clusters: int = 5,
    n_sentences_per_doc: int = 3,
    cache: SummaryCache = None,
) -> HierarchicalSummary:
    """Build hierarchical summary of a document collection.

    Algorithm:
    1. Map step: textrank_summary(content, n_sentences=n_sentences_per_doc, query=query)
       for each doc. Use cache to skip unchanged docs.
    2. If query: filter to docs with token overlap > 0 with query. If none match, use all.
    3. Cluster summaries into n_clusters groups (cluster_summaries).
    4. Reduce step: for each cluster, reduce_summaries(cluster_summaries, query=query).
    5. Build HierarchicalSummary:
       - top-level: reduce all cluster summaries together
       - sub_summaries: one per cluster
    6. coverage = len(included_docs) / len(docs)

    Edge cases:
    - Empty docs → HierarchicalSummary(topic="empty", summary="", sources=[], coverage=0)
    - Single doc → no sub_summaries, just top-level
    - n_clusters > len(docs) → n_clusters = len(docs)
    """
    import re

    if not docs:
        return HierarchicalSummary(
            topic="empty",
            summary="",
            sources=[],
            coverage=0.0,
        )

    # Map step: summarize each doc
    doc_summaries: dict[str, str] = {}
    for path, content in docs.items():
        if cache is not None:
            cached = cache.get(content)
            if cached is not None:
                doc_summaries[path] = cached
                continue
        summary = textrank_summary(content, n_sentences=n_sentences_per_doc, query=query)
        doc_summaries[path] = summary
        if cache is not None:
            cache.set(content, summary)

    all_paths = list(doc_summaries.keys())

    # Filter by query relevance
    if query:
        query_tokens = set(re.findall(r"[a-zа-яё]+", query.lower()))
        if query_tokens:
            relevant = []
            for path in all_paths:
                content = docs[path]
                content_tokens = set(re.findall(r"[a-zа-яё]+", content.lower()))
                if content_tokens & query_tokens:
                    relevant.append(path)
            if relevant:
                included_paths = relevant
            else:
                included_paths = all_paths
        else:
            included_paths = all_paths
    else:
        included_paths = all_paths

    coverage = len(included_paths) / len(docs)

    # Single doc case
    if len(included_paths) == 1:
        path = included_paths[0]
        top_summary = doc_summaries[path][:max_summary_length]
        return HierarchicalSummary(
            topic="corpus",
            summary=top_summary,
            sources=list(included_paths),
            sub_summaries=[],
            coverage=coverage,
        )

    # Adjust n_clusters
    effective_clusters = min(n_clusters, len(included_paths))

    # Build summary list and path list for clustering
    summary_list = [doc_summaries[p] for p in included_paths]

    # Cluster
    clusters = cluster_summaries(summary_list, n_clusters=effective_clusters)

    # Build sub-summaries
    sub_summaries = []
    cluster_reduced = []

    for cluster_idx, indices in enumerate(clusters):
        cluster_paths = [included_paths[i] for i in indices]
        cluster_sums = [summary_list[i] for i in indices]
        reduced = reduce_summaries(cluster_sums, query=query)
        cluster_reduced.append(reduced)
        sub = HierarchicalSummary(
            topic=f"cluster_{cluster_idx + 1}",
            summary=reduced,
            sources=cluster_paths,
            sub_summaries=[],
            coverage=len(cluster_paths) / len(docs),
        )
        sub_summaries.append(sub)

    # Top-level summary: reduce all cluster summaries
    top_summary = reduce_summaries(cluster_reduced, query=query)
    top_summary = top_summary[:max_summary_length]

    return HierarchicalSummary(
        topic="corpus",
        summary=top_summary,
        sources=list(included_paths),
        sub_summaries=sub_summaries,
        coverage=coverage,
    )
