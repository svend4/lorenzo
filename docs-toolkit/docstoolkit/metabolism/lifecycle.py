from dataclasses import dataclass, field
from enum import Enum
from docstoolkit.metabolism.signals import FreshnessScore, StalenessSignal, ConflictSignal
from docstoolkit.metabolism.absorber import absorb_fragment, AbsorptionResult


class LifecycleState(str, Enum):
    FRESH = "fresh"
    AGING = "aging"
    STALE = "stale"
    CONFLICTED = "conflicted"
    ABSORBING = "absorbing"


@dataclass
class DocLifecycle:
    """Full lifecycle tracker for a document."""
    doc_id: str
    content: str
    state: LifecycleState = LifecycleState.FRESH
    freshness: FreshnessScore = None
    pending_absorptions: list = field(default_factory=list)  # list[AbsorptionResult]

    def __post_init__(self):
        if self.freshness is None:
            self.freshness = FreshnessScore(doc_id=self.doc_id, score=1.0)

    def add_staleness_signal(self, signal: StalenessSignal) -> None:
        """Add a staleness signal; reduce freshness score by 0.1 * signal.confidence."""
        self.freshness.staleness_signals.append(signal)
        self.freshness.score = max(0.0, self.freshness.score - 0.1 * signal.confidence)
        self._update_state()

    def add_conflict_signal(self, signal: ConflictSignal) -> None:
        """Add a conflict signal; reduce freshness score by 0.15 * signal.confidence."""
        self.freshness.conflict_signals.append(signal)
        self.freshness.score = max(0.0, self.freshness.score - 0.15 * signal.confidence)
        self._update_state()

    def try_absorb(self, fragment: str, min_relevance: float = 0.15) -> AbsorptionResult:
        """Try to absorb a fragment. If absorbed, store in pending_absorptions."""
        result = absorb_fragment(self.content, fragment, self.doc_id, min_relevance)
        if result.was_absorbed:
            self.pending_absorptions.append(result)
            if self.state not in (LifecycleState.CONFLICTED, LifecycleState.STALE):
                self.state = LifecycleState.ABSORBING
        return result

    def commit_absorptions(self) -> str:
        """Apply all pending_absorptions to content; return updated content.

        For each absorption: append fragment to content (simplest model).
        Clear pending_absorptions. Update state.
        """
        if not self.pending_absorptions:
            return self.content
        fragments = [r.fragment_text for r in self.pending_absorptions]
        self.content = self.content.rstrip() + "\n\n" + "\n\n".join(fragments)
        self.pending_absorptions.clear()
        self._update_state()
        return self.content

    def _update_state(self) -> None:
        if self.freshness.conflict_signals:
            self.state = LifecycleState.CONFLICTED
        elif self.freshness.score < 0.3:
            self.state = LifecycleState.STALE
        elif self.freshness.score < 0.6:
            self.state = LifecycleState.AGING
        elif self.pending_absorptions:
            self.state = LifecycleState.ABSORBING
        else:
            self.state = LifecycleState.FRESH
