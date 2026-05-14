from dataclasses import dataclass, field
from enum import Enum


class NodeType(str, Enum):
    HYPOTHESIS = "hypothesis"   # partial answer / claim to verify
    FACT = "fact"               # confirmed from corpus
    REFUTED = "refuted"         # contradicted by corpus
    REFINED = "refined"         # updated version of another node
    SYNTHESIS = "synthesis"     # combination of multiple nodes


@dataclass
class ThoughtNode:
    """One node in the graph-of-thoughts."""
    node_id: str
    text: str                            # the hypothesis/fact text
    node_type: NodeType = NodeType.HYPOTHESIS
    source_passages: list = field(default_factory=list)  # list of doc_ids
    confidence: float = 0.5              # 0-1
    parent_ids: list = field(default_factory=list)  # list of node_id strings
    children_ids: list = field(default_factory=list)

    def is_confirmed(self) -> bool:
        return self.node_type == NodeType.FACT

    def is_refuted(self) -> bool:
        return self.node_type == NodeType.REFUTED

    def summary(self) -> str:
        return f"[{self.node_type.value}] {self.text[:80]} (conf={self.confidence:.2f})"
