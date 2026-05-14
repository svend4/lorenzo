"""Chunk data types for adaptive chunking."""
from dataclasses import dataclass, field
from enum import Enum
import uuid


class ChunkType(Enum):
    """Type of text chunk."""
    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"
    HEADING_SECTION = "heading_section"
    FIXED = "fixed"
    SEMANTIC = "semantic"


def _short_uuid() -> str:
    """Generate a short 8-character UUID4 string."""
    return uuid.uuid4().hex[:8]


@dataclass
class Chunk:
    """A single chunk of text with metadata."""
    text: str
    chunk_type: ChunkType
    doc_id: str
    start_char: int
    end_char: int
    chunk_id: str = field(default_factory=_short_uuid)
    metadata: dict = field(default_factory=dict)

    def word_count(self) -> int:
        """Return the number of words in the chunk."""
        return len(self.text.split())

    def char_count(self) -> int:
        """Return the number of characters in the chunk."""
        return len(self.text)

    def is_empty(self) -> bool:
        """Return True if the text strip is empty."""
        return self.text.strip() == ""
