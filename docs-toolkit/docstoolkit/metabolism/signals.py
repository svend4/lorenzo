from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StalenessSignal:
    """A signal that a doc section may be outdated."""
    doc_id: str
    section: str           # heading or substring that might be stale
    newer_doc_id: str      # doc that has more recent info
    confidence: float      # 0-1
    reason: str = ""


@dataclass
class ConflictSignal:
    """Two passages contradict each other."""
    doc_id_a: str
    doc_id_b: str
    passage_a: str         # short snippet
    passage_b: str
    overlap_score: float   # token overlap (jaccard) of shared terms
    confidence: float      # 0-1


@dataclass
class FreshnessScore:
    """Freshness score for a document."""
    doc_id: str
    score: float           # 0 (stale) to 1 (fresh)
    staleness_signals: list = field(default_factory=list)   # list[StalenessSignal]
    conflict_signals: list = field(default_factory=list)    # list[ConflictSignal]
    last_updated: str = ""

    def is_fresh(self, threshold: float = 0.6) -> bool:
        return self.score >= threshold

    def summary(self) -> str:
        return (f"doc={self.doc_id} score={self.score:.2f} "
                f"stale_signals={len(self.staleness_signals)} "
                f"conflicts={len(self.conflict_signals)}")
