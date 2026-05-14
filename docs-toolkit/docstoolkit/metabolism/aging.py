import re
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DocAge:
    """Age metrics for a document."""
    doc_id: str
    days_since_update: float   # 0.0 if unknown
    word_count: int
    heading_count: int
    has_dates: bool            # True if doc contains any date patterns


@dataclass
class AgeReport:
    """Aging analysis report."""
    docs: list = field(default_factory=list)   # list[DocAge]
    oldest_doc_id: str = ""
    newest_doc_id: str = ""
    avg_days: float = 0.0

    def stale_docs(self, threshold_days: float = 180.0) -> list:
        """Return DocAge entries older than threshold."""
        return [d for d in self.docs if d.days_since_update > threshold_days]


def age_document(
    doc_id: str,
    content: str,
    last_modified_iso: str = "",
) -> DocAge:
    """Compute age metrics for a single document.

    days_since_update:
      - parse last_modified_iso as ISO datetime
      - if empty or unparseable: 0.0
      - else: (now - last_modified).days
    word_count: len(content.split())
    heading_count: count lines starting with #
    has_dates: bool — any 4-digit year 1990-2030 found
    """
    # Compute days_since_update
    days_since_update = 0.0
    if last_modified_iso:
        try:
            # Handle both aware and naive datetimes
            dt = datetime.fromisoformat(last_modified_iso)
            now = datetime.now(timezone.utc)
            # If dt is naive, assume UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            delta = now - dt
            days_since_update = float(delta.days)
        except (ValueError, TypeError):
            days_since_update = 0.0

    word_count = len(content.split())

    heading_count = sum(
        1 for line in content.splitlines()
        if line.startswith("#")
    )

    has_dates = bool(re.search(r'\b(199[0-9]|20[0-2][0-9]|2030)\b', content))

    return DocAge(
        doc_id=doc_id,
        days_since_update=days_since_update,
        word_count=word_count,
        heading_count=heading_count,
        has_dates=has_dates,
    )
