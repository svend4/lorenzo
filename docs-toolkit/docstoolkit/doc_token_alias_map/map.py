"""DocTokenAliasMap — token-level alias mapping for doc text normalization.

The map stores ``alias -> canonical`` entries, optionally case-sensitive.
:meth:`DocTokenAliasMap.resolve` returns the canonical form for a token if
an alias exists, otherwise returns the token unchanged.  Bulk substitution
on free text is supported via :meth:`DocTokenAliasMap.replace_tokens`,
which preserves the original whitespace layout.

The module is pure stdlib and thread-safe via a single ``threading.Lock``.
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional


_TOKEN_SPLIT_RE = re.compile(r"\S+|\s+")


@dataclass
class TokenAlias:
    """A single token alias entry."""

    alias: str
    canonical: str
    case_sensitive: bool = False
    created_at: float = 0.0


@dataclass
class AliasMapStats:
    """Aggregate counters reported by :meth:`DocTokenAliasMap.stats`."""

    total_aliases: int
    unique_canonicals: int
    total_replacements: int


class DocTokenAliasMap:
    """Maintain a registry of token aliases and apply them to text.

    Entries with ``case_sensitive=True`` only match the exact alias string.
    Entries with ``case_sensitive=False`` match the alias under
    case-insensitive comparison.  When both styles apply to a token, the
    exact (case-sensitive) match wins.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # alias text -> TokenAlias (alias text preserved as-is)
        self._aliases: dict[str, TokenAlias] = {}
        self._total_replacements: int = 0

    # ----------------------------------------------------------- registration

    def add_alias(
        self,
        alias: str,
        canonical: str,
        case_sensitive: bool = False,
        now: Optional[float] = None,
    ) -> TokenAlias:
        """Create or replace an alias mapping keyed by ``alias`` text."""
        ts = now if now is not None else time.time()
        entry = TokenAlias(
            alias=alias,
            canonical=canonical,
            case_sensitive=case_sensitive,
            created_at=ts,
        )
        with self._lock:
            self._aliases[alias] = entry
        return entry

    def remove_alias(self, alias: str) -> bool:
        """Remove an alias.  Returns ``True`` if the alias existed."""
        with self._lock:
            if alias in self._aliases:
                del self._aliases[alias]
                return True
            return False

    # ------------------------------------------------------------------ lookup

    def get_alias(self, alias: str) -> Optional[TokenAlias]:
        """Return the :class:`TokenAlias` registered under ``alias`` if any."""
        with self._lock:
            return self._aliases.get(alias)

    def _lookup(self, token: str) -> Optional[TokenAlias]:
        """Find a matching entry for ``token`` honouring case sensitivity."""
        # 1) Exact match always wins.
        entry = self._aliases.get(token)
        if entry is not None:
            return entry
        # 2) Case-insensitive scan over case-insensitive entries.
        lowered = token.lower()
        for cand in self._aliases.values():
            if cand.case_sensitive:
                continue
            if cand.alias.lower() == lowered:
                return cand
        return None

    def resolve(self, token: str) -> str:
        """Return the canonical form for ``token`` or ``token`` unchanged."""
        with self._lock:
            entry = self._lookup(token)
            return entry.canonical if entry is not None else token

    # -------------------------------------------------------------- bulk apply

    def replace_tokens(
        self,
        text: str,
        splitter: Optional[Callable[[str], list[str]]] = None,
    ) -> str:
        """Apply alias substitution to every token in ``text``.

        Tokenisation defaults to ``re.findall(r'\\S+|\\s+', text)`` so that
        whitespace runs are preserved verbatim.  A custom ``splitter`` may be
        supplied; it must return a list of pieces whose concatenation equals
        the input.
        """
        if splitter is None:
            pieces = _TOKEN_SPLIT_RE.findall(text)
        else:
            pieces = list(splitter(text))

        changed = 0
        out: list[str] = []
        with self._lock:
            for piece in pieces:
                if piece == "" or piece.isspace():
                    out.append(piece)
                    continue
                entry = self._lookup(piece)
                if entry is None:
                    out.append(piece)
                else:
                    if entry.canonical != piece:
                        changed += 1
                    out.append(entry.canonical)
            self._total_replacements += changed
        return "".join(out)

    # --------------------------------------------------------------- inventory

    def aliases_for(self, canonical: str) -> list[str]:
        """Return sorted aliases that map to ``canonical``."""
        with self._lock:
            return sorted(
                a for a, entry in self._aliases.items()
                if entry.canonical == canonical
            )

    def list_aliases(self) -> list[TokenAlias]:
        """Return all :class:`TokenAlias` entries sorted by alias text."""
        with self._lock:
            return [self._aliases[k] for k in sorted(self._aliases)]

    def canonicals(self) -> list[str]:
        """Return sorted unique canonical forms."""
        with self._lock:
            return sorted({entry.canonical for entry in self._aliases.values()})

    # ----------------------------------------------------------------- cleanup

    def clear(self) -> int:
        """Remove all aliases.  Returns the number of entries cleared."""
        with self._lock:
            n = len(self._aliases)
            self._aliases.clear()
            return n

    # ------------------------------------------------------------------- stats

    def stats(self) -> AliasMapStats:
        """Snapshot of registry size and replacement counters."""
        with self._lock:
            canonicals = {entry.canonical for entry in self._aliases.values()}
            return AliasMapStats(
                total_aliases=len(self._aliases),
                unique_canonicals=len(canonicals),
                total_replacements=self._total_replacements,
            )
