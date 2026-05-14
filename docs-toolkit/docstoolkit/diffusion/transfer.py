import re
from dataclasses import dataclass, field
from datetime import datetime

from docstoolkit.diffusion.alignment import ConceptAlignment


@dataclass
class TransferRecord:
    """One concept transferred from corpus A to corpus B."""
    concept: str
    source_doc_id: str       # in corpus A
    target_doc_id: str       # in corpus B (best match or new)
    content_snippet: str     # the text snippet being transferred
    similarity: float
    accepted: bool           # True if passed trust threshold
    ts: str = ""

    def __post_init__(self):
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')


@dataclass
class TransferReport:
    """Report of a diffusion transfer operation."""
    records: list = field(default_factory=list)   # list[TransferRecord]
    accepted_count: int = 0
    rejected_count: int = 0
    source_corpus_id: str = ""
    target_corpus_id: str = ""

    def acceptance_rate(self) -> float:
        total = self.accepted_count + self.rejected_count
        return self.accepted_count / total if total > 0 else 0.0

    def accepted_records(self) -> list:
        return [r for r in self.records if r.accepted]


class DiffusionTransfer:
    """Transfers aligned concepts from corpus A into corpus B."""

    def __init__(self, trust_threshold: float = 0.2, max_snippet_words: int = 50):
        self.trust_threshold = trust_threshold
        self.max_snippet_words = max_snippet_words

    def transfer(
        self,
        alignments: list,       # list[ConceptAlignment]
        corpus_a: dict,         # {doc_id: content}
        source_id: str = "A",
        target_id: str = "B",
    ) -> TransferReport:
        """Create transfer records from alignments.

        For each alignment:
        1. Extract content_snippet: first N words from source doc containing concept
           (search for concept in corpus_a[doc_id_a], take surrounding 50 words)
        2. accepted = alignment.similarity >= trust_threshold
        3. Create TransferRecord

        Return TransferReport with counts.
        """
        report = TransferReport(
            source_corpus_id=source_id,
            target_corpus_id=target_id,
        )

        for alignment in alignments:
            content = corpus_a.get(alignment.doc_id_a, "")
            snippet = self._extract_snippet(content, alignment.concept)
            accepted = alignment.similarity >= self.trust_threshold

            record = TransferRecord(
                concept=alignment.concept,
                source_doc_id=alignment.doc_id_a,
                target_doc_id=alignment.doc_id_b,
                content_snippet=snippet,
                similarity=alignment.similarity,
                accepted=accepted,
            )
            report.records.append(record)
            if accepted:
                report.accepted_count += 1
            else:
                report.rejected_count += 1

        return report

    def _extract_snippet(self, content: str, concept: str) -> str:
        """Extract snippet: surrounding words around concept in content."""
        words = re.findall(r'\S+', content)
        concept_lower = concept.lower()

        for i, word in enumerate(words):
            if word.lower().strip('.,;:!?"\'-()[]{}') == concept_lower:
                half = self.max_snippet_words // 2
                start = max(0, i - half)
                end = min(len(words), i + half + 1)
                return " ".join(words[start:end])

        # Fallback: return first max_snippet_words words
        return " ".join(words[: self.max_snippet_words])
