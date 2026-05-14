from dataclasses import dataclass, field

from docstoolkit.diffusion.transfer import TransferRecord


@dataclass
class DiffusionProvenance:
    """Provenance chain for a diffused concept."""
    concept: str
    origin_corpus: str
    origin_doc_id: str
    diffused_to_corpus: str
    diffused_to_doc_id: str
    similarity_chain: list = field(default_factory=list)   # list of floats (hop similarities)
    accepted: bool = True

    def hops(self) -> int:
        return len(self.similarity_chain)

    def min_similarity(self) -> float:
        if not self.similarity_chain:
            return 0.0
        return min(self.similarity_chain)

    def provenance_string(self) -> str:
        """Return: 'concept: origin_corpus/origin_doc_id → diffused_to_corpus/diffused_to_doc_id (hops=N)'"""
        return (f"{self.concept}: {self.origin_corpus}/{self.origin_doc_id} "
                f"→ {self.diffused_to_corpus}/{self.diffused_to_doc_id} "
                f"(hops={self.hops()})")


def trace_origin(
    records: list,      # list[TransferRecord]
    source_corpus: str,
    target_corpus: str,
) -> list:
    """Build provenance chains from transfer records.

    For each accepted TransferRecord:
    - Create DiffusionProvenance with similarity_chain = [record.similarity]
    - origin = source_corpus / source_doc_id
    - diffused_to = target_corpus / target_doc_id

    Return list[DiffusionProvenance].
    """
    provenances = []
    for record in records:
        if not record.accepted:
            continue
        prov = DiffusionProvenance(
            concept=record.concept,
            origin_corpus=source_corpus,
            origin_doc_id=record.source_doc_id,
            diffused_to_corpus=target_corpus,
            diffused_to_doc_id=record.target_doc_id,
            similarity_chain=[record.similarity],
            accepted=record.accepted,
        )
        provenances.append(prov)
    return provenances
