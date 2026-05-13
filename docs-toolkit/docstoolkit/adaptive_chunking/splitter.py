"""Adaptive text splitter with multiple chunking strategies."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.adaptive_chunking.chunk import Chunk, ChunkType


@dataclass
class ChunkConfig:
    """Configuration for chunking behaviour."""
    target_size: int = 300   # words
    min_size: int = 50       # words
    max_size: int = 600      # words
    overlap: int = 0         # words to overlap between consecutive chunks


def _word_count(text: str) -> int:
    return len(text.split())


def _split_sentences(text: str) -> list[str]:
    """Split text at sentence boundaries ('. ', '! ', '? ')."""
    # Use a regex that splits after '.', '!', '?' followed by whitespace,
    # keeping the delimiter with the preceding sentence.
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p for p in parts if p]


class AdaptiveChunker:
    """Splits text into chunks using various strategies."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def chunk_by_paragraphs(
        self,
        text: str,
        doc_id: str,
        config: Optional[ChunkConfig] = None,
    ) -> list[Chunk]:
        """Split on double newlines, merge short paragraphs, split oversized ones."""
        if config is None:
            config = ChunkConfig()

        raw_paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in raw_paragraphs if p.strip()]

        # Merge short paragraphs with the next one
        merged: list[str] = []
        pending = ""
        for para in paragraphs:
            if pending:
                combined = pending + "\n\n" + para
                if _word_count(pending) < config.min_size:
                    pending = combined
                    continue
                else:
                    merged.append(pending)
                    pending = para
            else:
                pending = para
        if pending:
            merged.append(pending)

        # Split oversized paragraphs at sentence boundaries
        final_paragraphs: list[str] = []
        for para in merged:
            if _word_count(para) > config.max_size:
                final_paragraphs.extend(
                    self._split_oversized(para, config)
                )
            else:
                final_paragraphs.append(para)

        return self._build_chunks(
            final_paragraphs, text, doc_id, ChunkType.PARAGRAPH
        )

    def chunk_by_headings(
        self,
        text: str,
        doc_id: str,
        config: Optional[ChunkConfig] = None,
    ) -> list[Chunk]:
        """Split on Markdown headings; each heading + content = one HEADING_SECTION chunk."""
        if config is None:
            config = ChunkConfig()

        lines = text.split('\n')
        sections: list[str] = []
        current_lines: list[str] = []

        for line in lines:
            if re.match(r'^#{1,6}\s', line) and current_lines:
                section_text = '\n'.join(current_lines).strip()
                if section_text:
                    sections.append(section_text)
                current_lines = [line]
            else:
                current_lines.append(line)

        # Handle trailing content (or text before any heading)
        if current_lines:
            section_text = '\n'.join(current_lines).strip()
            if section_text:
                sections.append(section_text)

        return self._build_chunks(
            sections, text, doc_id, ChunkType.HEADING_SECTION
        )

    def chunk_fixed(
        self,
        text: str,
        doc_id: str,
        config: Optional[ChunkConfig] = None,
    ) -> list[Chunk]:
        """Split into FIXED chunks of target_size words, with optional overlap."""
        if config is None:
            config = ChunkConfig()

        words = text.split()
        if not words:
            return []

        target = max(1, config.target_size)
        overlap = max(0, min(config.overlap, target - 1))
        step = target - overlap

        chunk_texts: list[str] = []
        i = 0
        while i < len(words):
            chunk_words = words[i: i + target]
            chunk_texts.append(' '.join(chunk_words))
            i += step
            if i >= len(words):
                break

        return self._build_chunks(chunk_texts, text, doc_id, ChunkType.FIXED)

    def chunk_sentences(
        self,
        text: str,
        doc_id: str,
        config: Optional[ChunkConfig] = None,
    ) -> list[Chunk]:
        """Group sentences into chunks up to target_size words."""
        if config is None:
            config = ChunkConfig()

        sentences = _split_sentences(text)
        if not sentences:
            return []

        chunk_texts: list[str] = []
        current_sentences: list[str] = []
        current_words = 0

        for sentence in sentences:
            sw = _word_count(sentence)
            # If adding this sentence would exceed target and we already have
            # enough words, flush the current group.
            if current_sentences and current_words + sw > config.target_size:
                chunk_texts.append(' '.join(current_sentences))
                current_sentences = [sentence]
                current_words = sw
            else:
                current_sentences.append(sentence)
                current_words += sw

        if current_sentences:
            chunk_texts.append(' '.join(current_sentences))

        return self._build_chunks(
            chunk_texts, text, doc_id, ChunkType.SENTENCE
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _split_oversized(self, text: str, config: ChunkConfig) -> list[str]:
        """Split an oversized paragraph at sentence boundaries."""
        sentences = _split_sentences(text)
        if not sentences:
            return [text]

        parts: list[str] = []
        current: list[str] = []
        current_words = 0

        for sentence in sentences:
            sw = _word_count(sentence)
            if current and current_words + sw > config.max_size:
                parts.append(' '.join(current))
                current = [sentence]
                current_words = sw
            else:
                current.append(sentence)
                current_words += sw

        if current:
            parts.append(' '.join(current))

        return parts

    def _build_chunks(
        self,
        texts: list[str],
        original: str,
        doc_id: str,
        chunk_type: ChunkType,
    ) -> list[Chunk]:
        """Turn a list of text strings into Chunk objects with char offsets."""
        chunks: list[Chunk] = []
        search_start = 0

        for text in texts:
            if not text.strip():
                continue
            # Find the offset of this text in the original document.
            idx = original.find(text, search_start)
            if idx == -1:
                # Fallback: search from the beginning (shouldn't happen normally)
                idx = original.find(text)
            start = idx if idx != -1 else search_start
            end = start + len(text)
            search_start = end

            chunks.append(
                Chunk(
                    text=text,
                    chunk_type=chunk_type,
                    doc_id=doc_id,
                    start_char=start,
                    end_char=end,
                )
            )

        return chunks
