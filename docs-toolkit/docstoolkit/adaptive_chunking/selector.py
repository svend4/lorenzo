"""Strategy selector for adaptive chunking."""
from __future__ import annotations

import re
from enum import Enum


class ChunkingStrategy(Enum):
    """Available chunking strategies."""
    AUTO = "auto"
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    FIXED = "fixed"
    SENTENCE = "sentence"


class StrategySelector:
    """Selects the best chunking strategy for a given text."""

    def select(self, text: str) -> ChunkingStrategy:
        """Return the recommended strategy for the text.

        AUTO logic:
          - If text has Markdown headings → HEADING
          - elif avg paragraph word count > 200 → FIXED
          - elif sentence count > 20 → SENTENCE
          - else → PARAGRAPH
        """
        if self.heading_count(text) > 0:
            return ChunkingStrategy.HEADING
        if self.avg_paragraph_words(text) > 200:
            return ChunkingStrategy.FIXED
        if self.sentence_count(text) > 20:
            return ChunkingStrategy.SENTENCE
        return ChunkingStrategy.PARAGRAPH

    def heading_count(self, text: str) -> int:
        """Return the number of Markdown headings in the text."""
        return sum(
            1 for line in text.splitlines()
            if re.match(r'^#{1,6}\s', line)
        )

    def avg_paragraph_words(self, text: str) -> float:
        """Return the average word count across non-empty paragraphs."""
        paragraphs = [
            p.strip()
            for p in re.split(r'\n\s*\n', text)
            if p.strip()
        ]
        if not paragraphs:
            return 0.0
        total_words = sum(len(p.split()) for p in paragraphs)
        return total_words / len(paragraphs)

    def sentence_count(self, text: str) -> int:
        """Return the approximate number of sentences in the text."""
        # Count sentence-ending punctuation followed by whitespace or end-of-string
        return len(re.findall(r'[.!?](?:\s|$)', text))
