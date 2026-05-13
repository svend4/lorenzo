"""Heuristic change detector for documentation files."""
from __future__ import annotations

import re

from docstoolkit.doc_versioning.version import ChangeType


class ChangeDetector:
    """Determine the semantic impact of a text change without an LLM."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect(self, old_text: str, new_text: str) -> ChangeType:
        """Classify the change from *old_text* to *new_text*.

        Decision tree
        -------------
        1. NONE   — texts are byte-identical.
        2. PATCH  — after normalising whitespace/punctuation the texts are
                    identical (only cosmetic changes).
        3. MAJOR  — word-count delta > 30 % **or** heading-count delta > 2.
        4. MINOR  — word-count increased by > 10 % **or** new headings added.
        5. PATCH  — fallback (something changed but none of the above).
        """
        if old_text == new_text:
            return ChangeType.NONE

        if self._normalize(old_text) == self._normalize(new_text):
            return ChangeType.PATCH

        old_wc = self.word_count(old_text)
        new_wc = self.word_count(new_text)
        old_hc = self.heading_count(old_text)
        new_hc = self.heading_count(new_text)

        wc_delta = abs(new_wc - old_wc)
        hc_delta = abs(new_hc - old_hc)

        # Compute percentage change (guard against zero-length originals)
        if old_wc > 0:
            wc_pct = wc_delta / old_wc
        else:
            wc_pct = 1.0 if new_wc > 0 else 0.0

        if wc_pct > 0.30 or hc_delta > 2:
            return ChangeType.MAJOR

        if wc_pct > 0.10 or new_hc > old_hc:
            return ChangeType.MINOR

        return ChangeType.PATCH

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------

    @staticmethod
    def word_count(text: str) -> int:
        """Return the number of whitespace-separated tokens in *text*."""
        return len(text.split())

    @staticmethod
    def heading_count(text: str) -> int:
        """Return the number of Markdown headings (lines starting with ``#``)."""
        count = 0
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                count += 1
        return count

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(text: str) -> str:
        """Strip whitespace and punctuation variations for PATCH detection.

        Collapses all whitespace runs to a single space, removes leading/
        trailing whitespace, and strips common punctuation characters so
        that purely cosmetic edits (extra spaces, trailing commas, …) are
        not treated as content changes.
        """
        # Collapse whitespace
        normalised = re.sub(r"\s+", " ", text).strip()
        # Remove punctuation characters that are often adjusted in formatting
        normalised = re.sub(r"[.,;:!?\-–—\"'`(){}\[\]]", "", normalised)
        return normalised
