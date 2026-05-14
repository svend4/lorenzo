"""DocChunker implementation (E155).

Stdlib only. Provides ``DocChunker`` with several strategies for splitting
text into ``Chunk`` objects suitable for RAG pipelines.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ---------------------------------------------------------------------------
# Enums and dataclasses
# ---------------------------------------------------------------------------


class ChunkStrategy(Enum):
    """Available chunking strategies."""

    FIXED_SIZE = "fixed_size"
    BY_PARAGRAPH = "by_paragraph"
    BY_SENTENCE = "by_sentence"
    BY_HEADING = "by_heading"
    BY_TOKEN_COUNT = "by_token_count"
    SLIDING_WINDOW = "sliding_window"


@dataclass
class Chunk:
    """A single chunk of text with positional and metadata info."""

    text: str
    chunk_id: int
    start_pos: int
    end_pos: int
    metadata: dict = field(default_factory=dict)
    token_count: int = 0


@dataclass
class ChunkConfig:
    """Configuration for :class:`DocChunker`."""

    strategy: ChunkStrategy = ChunkStrategy.FIXED_SIZE
    chunk_size: int = 500
    overlap: int = 0
    min_chunk_size: int = 50
    separator: str = "\n\n"


# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# DocChunker
# ---------------------------------------------------------------------------


class DocChunker:
    """Chunk documents into pieces using configurable strategy."""

    def __init__(self, config: Optional[ChunkConfig] = None) -> None:
        self.config = config if config is not None else ChunkConfig()

    # ------------------------------------------------------------------
    # Top-level dispatch
    # ------------------------------------------------------------------

    def chunk(self, text: str) -> List[Chunk]:
        """Split ``text`` using the configured strategy.

        Applies ``min_chunk_size`` filtering at the end (chunks smaller
        than ``min_chunk_size`` are discarded — except when *all* chunks
        would be discarded, in which case the original chunks are kept
        so the caller still receives something).
        """
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        if text == "":
            return []

        cfg = self.config
        if cfg.strategy is ChunkStrategy.FIXED_SIZE:
            chunks = self.chunk_fixed_size(text, cfg.chunk_size, cfg.overlap)
        elif cfg.strategy is ChunkStrategy.BY_PARAGRAPH:
            chunks = self.chunk_by_paragraph(text, cfg.separator)
        elif cfg.strategy is ChunkStrategy.BY_SENTENCE:
            chunks = self.chunk_by_sentence(text)
        elif cfg.strategy is ChunkStrategy.BY_HEADING:
            chunks = self.chunk_by_heading(text)
        elif cfg.strategy is ChunkStrategy.BY_TOKEN_COUNT:
            chunks = self.chunk_by_token_count(text, cfg.chunk_size, cfg.overlap)
        elif cfg.strategy is ChunkStrategy.SLIDING_WINDOW:
            step = cfg.chunk_size - cfg.overlap if cfg.overlap else cfg.chunk_size
            if step <= 0:
                step = max(1, cfg.chunk_size)
            chunks = self.chunk_sliding_window(text, cfg.chunk_size, step)
        else:  # pragma: no cover - defensive
            raise ValueError(f"unknown strategy: {cfg.strategy}")

        # Apply min_chunk_size filtering
        if cfg.min_chunk_size > 0:
            filtered = [c for c in chunks if len(c.text) >= cfg.min_chunk_size]
            if filtered:
                chunks = self._renumber(filtered)
        return chunks

    # ------------------------------------------------------------------
    # Strategy implementations
    # ------------------------------------------------------------------

    def chunk_fixed_size(
        self, text: str, size: int, overlap: int = 0
    ) -> List[Chunk]:
        """Split ``text`` into chunks of ``size`` chars with ``overlap``.

        Tries to break on whitespace near the boundary when possible.
        """
        if size <= 0:
            raise ValueError("size must be positive")
        if overlap < 0:
            raise ValueError("overlap must be non-negative")
        if overlap >= size:
            raise ValueError("overlap must be < size")
        if text == "":
            return []

        chunks: List[Chunk] = []
        step = size - overlap
        pos = 0
        chunk_id = 0
        n = len(text)
        while pos < n:
            end = min(pos + size, n)
            # If we are not at the end of text, try to break on whitespace
            if end < n:
                # search backwards for whitespace within the last 20% of the window
                window = max(1, size // 5)
                search_start = max(pos + 1, end - window)
                # find rightmost whitespace in [search_start, end)
                break_at = -1
                for i in range(end - 1, search_start - 1, -1):
                    if text[i].isspace():
                        break_at = i
                        break
                if break_at != -1:
                    end = break_at + 1  # include the whitespace
            piece = text[pos:end]
            chunks.append(
                Chunk(
                    text=piece,
                    chunk_id=chunk_id,
                    start_pos=pos,
                    end_pos=end,
                    metadata={"strategy": "fixed_size"},
                    token_count=len(piece.split()),
                )
            )
            chunk_id += 1
            if end >= n:
                break
            pos = end - overlap
            if pos <= chunks[-1].start_pos:
                # ensure forward progress
                pos = chunks[-1].start_pos + 1
        return chunks

    def chunk_by_paragraph(
        self, text: str, separator: str = "\n\n"
    ) -> List[Chunk]:
        """Split text on ``separator`` (default ``\\n\\n``)."""
        if text == "":
            return []
        if separator == "":
            raise ValueError("separator must not be empty")

        chunks: List[Chunk] = []
        sep_len = len(separator)
        pos = 0
        chunk_id = 0
        para_num = 0
        n = len(text)
        while pos <= n:
            idx = text.find(separator, pos)
            if idx == -1:
                piece = text[pos:]
                start = pos
                end = n
                if piece:
                    chunks.append(
                        Chunk(
                            text=piece,
                            chunk_id=chunk_id,
                            start_pos=start,
                            end_pos=end,
                            metadata={
                                "strategy": "by_paragraph",
                                "paragraph_num": para_num,
                            },
                            token_count=len(piece.split()),
                        )
                    )
                    chunk_id += 1
                    para_num += 1
                break
            piece = text[pos:idx]
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        chunk_id=chunk_id,
                        start_pos=pos,
                        end_pos=idx,
                        metadata={
                            "strategy": "by_paragraph",
                            "paragraph_num": para_num,
                        },
                        token_count=len(piece.split()),
                    )
                )
                chunk_id += 1
                para_num += 1
            pos = idx + sep_len
        return chunks

    def chunk_by_sentence(self, text: str) -> List[Chunk]:
        """Split text on sentence-ending punctuation: ``(?<=[.!?])\\s+``."""
        if text == "":
            return []
        chunks: List[Chunk] = []
        chunk_id = 0
        sentence_num = 0
        pos = 0
        # Use the regex to find split points
        last = 0
        for m in _SENTENCE_SPLIT.finditer(text):
            split_start = m.start()
            split_end = m.end()
            piece = text[last:split_start]
            if piece.strip():
                chunks.append(
                    Chunk(
                        text=piece,
                        chunk_id=chunk_id,
                        start_pos=last,
                        end_pos=split_start,
                        metadata={
                            "strategy": "by_sentence",
                            "sentence_num": sentence_num,
                        },
                        token_count=len(piece.split()),
                    )
                )
                chunk_id += 1
                sentence_num += 1
            last = split_end
        # tail
        tail = text[last:]
        if tail.strip():
            chunks.append(
                Chunk(
                    text=tail,
                    chunk_id=chunk_id,
                    start_pos=last,
                    end_pos=len(text),
                    metadata={
                        "strategy": "by_sentence",
                        "sentence_num": sentence_num,
                    },
                    token_count=len(tail.split()),
                )
            )
        return chunks

    def chunk_by_heading(self, text: str) -> List[Chunk]:
        """Split on markdown ATX headings; each heading + body is one chunk."""
        if text == "":
            return []
        matches = list(_HEADING_RE.finditer(text))
        if not matches:
            # No headings at all: whole text is one chunk
            return [
                Chunk(
                    text=text,
                    chunk_id=0,
                    start_pos=0,
                    end_pos=len(text),
                    metadata={"strategy": "by_heading", "heading": None},
                    token_count=len(text.split()),
                )
            ]

        chunks: List[Chunk] = []
        chunk_id = 0
        # Preamble (text before the first heading), if non-empty
        first_start = matches[0].start()
        if first_start > 0:
            preamble = text[:first_start]
            if preamble.strip():
                chunks.append(
                    Chunk(
                        text=preamble,
                        chunk_id=chunk_id,
                        start_pos=0,
                        end_pos=first_start,
                        metadata={
                            "strategy": "by_heading",
                            "heading": None,
                            "level": 0,
                        },
                        token_count=len(preamble.split()),
                    )
                )
                chunk_id += 1

        # Each heading slice runs to the next heading (or EOF)
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            piece = text[start:end]
            level = len(m.group(1))
            heading_text = m.group(2).strip()
            chunks.append(
                Chunk(
                    text=piece,
                    chunk_id=chunk_id,
                    start_pos=start,
                    end_pos=end,
                    metadata={
                        "strategy": "by_heading",
                        "heading": heading_text,
                        "level": level,
                    },
                    token_count=len(piece.split()),
                )
            )
            chunk_id += 1
        return chunks

    def chunk_by_token_count(
        self, text: str, max_tokens: int, overlap: int = 0
    ) -> List[Chunk]:
        """Group whitespace-tokens into chunks of at most ``max_tokens``."""
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if overlap < 0:
            raise ValueError("overlap must be non-negative")
        if overlap >= max_tokens:
            raise ValueError("overlap must be < max_tokens")
        if text == "":
            return []

        # Find token spans (start, end) of each whitespace-delimited token
        spans: List[tuple] = []
        for m in re.finditer(r"\S+", text):
            spans.append((m.start(), m.end()))
        if not spans:
            return []

        step = max_tokens - overlap
        chunks: List[Chunk] = []
        chunk_id = 0
        i = 0
        n_tokens = len(spans)
        while i < n_tokens:
            j = min(i + max_tokens, n_tokens)
            start = spans[i][0]
            end = spans[j - 1][1]
            piece = text[start:end]
            chunks.append(
                Chunk(
                    text=piece,
                    chunk_id=chunk_id,
                    start_pos=start,
                    end_pos=end,
                    metadata={
                        "strategy": "by_token_count",
                        "token_start": i,
                        "token_end": j,
                    },
                    token_count=j - i,
                )
            )
            chunk_id += 1
            if j >= n_tokens:
                break
            i += step
        return chunks

    def chunk_sliding_window(
        self, text: str, window: int, step: int
    ) -> List[Chunk]:
        """Sliding window chunks of ``window`` chars advanced by ``step``."""
        if window <= 0:
            raise ValueError("window must be positive")
        if step <= 0:
            raise ValueError("step must be positive")
        if text == "":
            return []

        chunks: List[Chunk] = []
        chunk_id = 0
        pos = 0
        n = len(text)
        while pos < n:
            end = min(pos + window, n)
            piece = text[pos:end]
            chunks.append(
                Chunk(
                    text=piece,
                    chunk_id=chunk_id,
                    start_pos=pos,
                    end_pos=end,
                    metadata={
                        "strategy": "sliding_window",
                        "window": window,
                        "step": step,
                    },
                    token_count=len(piece.split()),
                )
            )
            chunk_id += 1
            if end >= n:
                break
            pos += step
        return chunks

    # ------------------------------------------------------------------
    # Post-processing utilities
    # ------------------------------------------------------------------

    def merge_small_chunks(
        self, chunks: List[Chunk], min_size: int
    ) -> List[Chunk]:
        """Merge consecutive chunks so that each is at least ``min_size`` chars.

        If a chunk is smaller than ``min_size``, it is appended to the
        previous chunk (or merged forward into the next if it is the first).
        """
        if not chunks:
            return []
        if min_size <= 0:
            return list(chunks)

        merged: List[Chunk] = []
        for c in chunks:
            if merged and len(merged[-1].text) < min_size:
                # extend previous
                prev = merged[-1]
                gap = max(0, c.start_pos - prev.end_pos)
                joiner = " " if gap and not prev.text.endswith((" ", "\n")) else ""
                new_text = prev.text + joiner + c.text
                merged[-1] = Chunk(
                    text=new_text,
                    chunk_id=prev.chunk_id,
                    start_pos=prev.start_pos,
                    end_pos=c.end_pos,
                    metadata={**prev.metadata, "merged": True},
                    token_count=len(new_text.split()),
                )
            else:
                merged.append(c)

        # If the last chunk is still too small, merge it back into the previous
        if len(merged) >= 2 and len(merged[-1].text) < min_size:
            last = merged.pop()
            prev = merged[-1]
            gap = max(0, last.start_pos - prev.end_pos)
            joiner = " " if gap and not prev.text.endswith((" ", "\n")) else ""
            new_text = prev.text + joiner + last.text
            merged[-1] = Chunk(
                text=new_text,
                chunk_id=prev.chunk_id,
                start_pos=prev.start_pos,
                end_pos=last.end_pos,
                metadata={**prev.metadata, "merged": True},
                token_count=len(new_text.split()),
            )

        return self._renumber(merged)

    def chunk_batch(self, texts: List[str]) -> List[List[Chunk]]:
        """Chunk a list of texts using the current configuration."""
        return [self.chunk(t) for t in texts]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _renumber(chunks: List[Chunk]) -> List[Chunk]:
        """Reassign ``chunk_id`` to be sequential starting at 0."""
        for i, c in enumerate(chunks):
            c.chunk_id = i
        return chunks
