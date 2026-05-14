"""E348 DocTokenIndex — token frequency index for fast term lookup."""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass
from typing import Optional

_TOKEN_RE = re.compile(r'\b[a-zA-Z0-9]+\b')


def _tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


@dataclass
class TokenInfo:
    """Info about a single token."""

    token: str
    doc_count: int
    total_count: int


@dataclass
class IndexStats:
    """Aggregate statistics for the index."""

    total_docs: int
    unique_tokens: int
    total_tokens: int


class DocTokenIndex:
    """Token frequency index for fast term lookup.

    Thread-safe via internal :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._doc_tokens: dict[str, dict[str, int]] = {}
        self._token_docs: dict[str, set[str]] = {}
        self._total_counts: dict[str, int] = {}
        self._lock = threading.Lock()

    def _remove_doc_locked(self, doc_id: str) -> bool:
        """Remove ``doc_id`` assuming the lock is already held."""
        if doc_id not in self._doc_tokens:
            return False
        for token, count in self._doc_tokens[doc_id].items():
            self._total_counts[token] -= count
            if self._total_counts[token] <= 0:
                del self._total_counts[token]
            docs = self._token_docs.get(token)
            if docs is not None:
                docs.discard(doc_id)
                if not docs:
                    del self._token_docs[token]
        del self._doc_tokens[doc_id]
        return True

    def index_doc(self, doc_id: str, text: str) -> int:
        """Tokenize ``text`` and index under ``doc_id``.

        If the document was previously indexed, its old entries are removed
        first. Returns the total token count for the doc.
        """
        with self._lock:
            self._remove_doc_locked(doc_id)
            tokens = _tokenize(text)
            counts: dict[str, int] = {}
            for tok in tokens:
                counts[tok] = counts.get(tok, 0) + 1
            self._doc_tokens[doc_id] = counts
            for tok, c in counts.items():
                self._token_docs.setdefault(tok, set()).add(doc_id)
                self._total_counts[tok] = self._total_counts.get(tok, 0) + c
            return len(tokens)

    def remove_doc(self, doc_id: str) -> bool:
        """Remove document from index. Returns ``True`` if it existed."""
        with self._lock:
            return self._remove_doc_locked(doc_id)

    def tokens_for_doc(self, doc_id: str) -> dict[str, int]:
        """Return a copy of ``{token: count}`` for the given doc."""
        with self._lock:
            return dict(self._doc_tokens.get(doc_id, {}))

    def docs_for_token(self, token: str) -> list[str]:
        """Return sorted doc_ids containing ``token``."""
        key = token.lower()
        with self._lock:
            docs = self._token_docs.get(key)
            if not docs:
                return []
            return sorted(docs)

    def token_count_in_doc(self, doc_id: str, token: str) -> int:
        """Return occurrence count of ``token`` in ``doc_id`` (0 if absent)."""
        key = token.lower()
        with self._lock:
            return self._doc_tokens.get(doc_id, {}).get(key, 0)

    def token_info(self, token: str) -> Optional[TokenInfo]:
        """Return :class:`TokenInfo` for ``token`` or ``None`` if unknown."""
        key = token.lower()
        with self._lock:
            if key not in self._total_counts:
                return None
            return TokenInfo(
                token=key,
                doc_count=len(self._token_docs.get(key, set())),
                total_count=self._total_counts[key],
            )

    def top_tokens(self, limit: int = 10) -> list[tuple]:
        """Return ``[(token, total_count), ...]`` sorted by total desc, token asc."""
        with self._lock:
            items = list(self._total_counts.items())
        items.sort(key=lambda x: (-x[1], x[0]))
        return items[:limit]

    def co_occurring_tokens(self, token: str, limit: int = 10) -> list[str]:
        """Return tokens co-occurring with ``token`` in the same docs.

        Excludes ``token`` itself. Sorted by joint doc count desc, then token asc.
        """
        key = token.lower()
        with self._lock:
            docs = self._token_docs.get(key)
            if not docs:
                return []
            joint: dict[str, int] = {}
            for doc_id in docs:
                for other in self._doc_tokens.get(doc_id, {}):
                    if other == key:
                        continue
                    joint[other] = joint.get(other, 0) + 1
        items = list(joint.items())
        items.sort(key=lambda x: (-x[1], x[0]))
        return [t for t, _ in items[:limit]]

    def search(self, token: str) -> list[str]:
        """Alias for :meth:`docs_for_token`."""
        return self.docs_for_token(token)

    def tokens_starting_with(self, prefix: str) -> list[str]:
        """Return sorted tokens starting with ``prefix`` (case-insensitive)."""
        key = prefix.lower()
        with self._lock:
            return sorted(t for t in self._total_counts if t.startswith(key))

    def clear(self) -> int:
        """Remove all docs from the index. Returns the number cleared."""
        with self._lock:
            n = len(self._doc_tokens)
            self._doc_tokens.clear()
            self._token_docs.clear()
            self._total_counts.clear()
            return n

    def stats(self) -> IndexStats:
        """Return aggregate :class:`IndexStats`."""
        with self._lock:
            return IndexStats(
                total_docs=len(self._doc_tokens),
                unique_tokens=len(self._total_counts),
                total_tokens=sum(self._total_counts.values()),
            )
