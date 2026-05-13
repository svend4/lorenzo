"""Evaluation dataset: EvalQuery and EvalDataset."""
import uuid
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class EvalQuery:
    """A single evaluation query with its ground-truth relevant documents."""

    query: str
    relevant_docs: set[str]
    query_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    metadata: dict = field(default_factory=dict)


class EvalDataset:
    """Collection of EvalQuery objects, keyed by query_id."""

    def __init__(self) -> None:
        self._queries: dict[str, EvalQuery] = {}
        self._order: list[str] = []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, query: EvalQuery) -> None:
        """Add an EvalQuery to the dataset."""
        self._queries[query.query_id] = query
        if query.query_id not in self._order:
            self._order.append(query.query_id)

    # ------------------------------------------------------------------
    # Access
    # ------------------------------------------------------------------

    def get(self, query_id: str) -> "EvalQuery | None":
        """Return EvalQuery by id, or None if not found."""
        return self._queries.get(query_id)

    def __len__(self) -> int:
        return len(self._queries)

    def __iter__(self) -> Iterator[EvalQuery]:
        for qid in self._order:
            yield self._queries[qid]

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    @classmethod
    def from_list(cls, queries: list[dict]) -> "EvalDataset":
        """Build an EvalDataset from a list of dicts.

        Each dict must contain:
            - "query" (str)
            - "relevant_docs" (list[str])
        Optional keys:
            - "query_id" (str)
            - "metadata" (dict)
        """
        ds = cls()
        for item in queries:
            kwargs: dict = {
                "query": item["query"],
                "relevant_docs": set(item["relevant_docs"]),
            }
            if "query_id" in item:
                kwargs["query_id"] = item["query_id"]
            if "metadata" in item:
                kwargs["metadata"] = item["metadata"]
            ds.add(EvalQuery(**kwargs))
        return ds

    def to_list(self) -> list[dict]:
        """Serialise the dataset to a list of plain dicts."""
        result = []
        for q in self:
            result.append({
                "query_id": q.query_id,
                "query": q.query,
                "relevant_docs": sorted(q.relevant_docs),
                "metadata": q.metadata,
            })
        return result
