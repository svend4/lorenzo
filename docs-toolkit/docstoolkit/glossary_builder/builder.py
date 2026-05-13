"""GlossaryBuilder — builds glossaries from document text, stdlib only."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GlossaryTerm:
    """A single glossary term with metadata."""

    term: str
    definition: str
    aliases: list[str] = field(default_factory=list)
    occurrences: int = 0
    first_line: int = 0
    context: str = ""


@dataclass
class GlossaryConfig:
    """Configuration for glossary building."""

    min_term_length: int = 3
    min_occurrences: int = 2
    extract_abbreviations: bool = True
    max_definition_length: int = 200


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences on .  !  ? boundaries."""
    return re.split(r"(?<=[.!?])\s+", text.strip())


def _find_first_line(text: str, phrase: str) -> int:
    """Return 1-based line number of the first occurrence of *phrase* in *text*."""
    pattern = re.compile(re.escape(phrase), re.IGNORECASE)
    for lineno, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line):
            return lineno
    return 0


def _count_occurrences(text: str, phrase: str) -> int:
    """Count case-insensitive occurrences of *phrase* as a whole phrase."""
    pattern = re.compile(re.escape(phrase), re.IGNORECASE)
    return len(pattern.findall(text))


class GlossaryBuilder:
    """Builds a glossary from plain-text documents.

    Parameters
    ----------
    config:
        A :class:`GlossaryConfig` instance.  Defaults to
        ``GlossaryConfig()`` when *None* is supplied.
    """

    # Regex: capitalized multi-word phrase (2+ words, each starting with uppercase)
    _TERM_PATTERN = re.compile(
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b"
    )
    # Regex: "Phrase (ABBR)" where ABBR is 2-5 uppercase letters
    _ABBR_PATTERN = re.compile(
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\(([A-Z]{2,5})\)"
    )

    def __init__(self, config: Optional[GlossaryConfig] = None) -> None:
        self._config: GlossaryConfig = config if config is not None else GlossaryConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self, text: str) -> list[GlossaryTerm]:
        """Extract glossary terms from *text*.

        Parameters
        ----------
        text:
            Plain-text (or Markdown) document content.

        Returns
        -------
        list[GlossaryTerm]
            Terms sorted alphabetically.
        """
        if not text or not text.strip():
            return []

        cfg = self._config
        sentences = _split_sentences(text)

        # --- Phase 1: collect abbreviation mappings (phrase -> [abbr, ...]) ---
        abbr_map: dict[str, list[str]] = {}  # canonical term -> list of aliases
        abbr_reverse: dict[str, str] = {}    # ABBR -> canonical term

        if cfg.extract_abbreviations:
            for sentence in sentences:
                for match in self._ABBR_PATTERN.finditer(sentence):
                    phrase = match.group(1)
                    abbr = match.group(2)
                    canonical = self._canonical(phrase)
                    if canonical not in abbr_map:
                        abbr_map[canonical] = []
                    if abbr not in abbr_map[canonical]:
                        abbr_map[canonical].append(abbr)
                    abbr_reverse[abbr] = canonical

        # --- Phase 2: find all capitalized multi-word phrases ---
        candidate_terms: set[str] = set()
        for match in self._TERM_PATTERN.finditer(text):
            phrase = match.group(1)
            if len(phrase) >= cfg.min_term_length:
                candidate_terms.add(phrase)

        # --- Phase 3: build GlossaryTerm objects ---
        # Map canonical (lower) -> GlossaryTerm being built
        terms_map: dict[str, GlossaryTerm] = {}

        for phrase in candidate_terms:
            canonical = self._canonical(phrase)

            # Count occurrences (phrase itself + any alias abbreviations)
            occ = _count_occurrences(text, phrase)
            # Also count alias occurrences
            for alias in abbr_map.get(canonical, []):
                occ += _count_occurrences(text, alias)

            if occ < cfg.min_occurrences:
                continue

            first_line = _find_first_line(text, phrase)

            # Find defining sentence (first sentence where term appears)
            definition_sentence = ""
            for sentence in sentences:
                if re.search(re.escape(phrase), sentence, re.IGNORECASE):
                    definition_sentence = sentence.strip()
                    break

            definition = definition_sentence[:cfg.max_definition_length]
            aliases = list(abbr_map.get(canonical, []))

            if canonical not in terms_map:
                terms_map[canonical] = GlossaryTerm(
                    term=phrase,
                    definition=definition,
                    aliases=aliases,
                    occurrences=occ,
                    first_line=first_line,
                    context=definition_sentence,
                )
            else:
                # Keep the version with the earlier first_line
                existing = terms_map[canonical]
                if first_line > 0 and (existing.first_line == 0 or first_line < existing.first_line):
                    terms_map[canonical] = GlossaryTerm(
                        term=phrase,
                        definition=definition,
                        aliases=aliases,
                        occurrences=max(existing.occurrences, occ),
                        first_line=first_line,
                        context=definition_sentence,
                    )
                else:
                    existing.occurrences = max(existing.occurrences, occ)
                    if not existing.aliases:
                        existing.aliases = aliases

        result = sorted(terms_map.values(), key=lambda t: t.term.lower())
        return result

    def build_from_files(self, texts: list[str]) -> list[GlossaryTerm]:
        """Build a merged glossary from multiple text documents.

        Terms are merged across files: occurrences are summed, and the
        earliest first_line (from the first file where the term appears)
        is kept.  Aliases are unified.

        Parameters
        ----------
        texts:
            List of document contents.

        Returns
        -------
        list[GlossaryTerm]
            Terms sorted alphabetically.
        """
        if not texts:
            return []

        merged: dict[str, GlossaryTerm] = {}

        for text in texts:
            file_terms = self.build(text)
            for term in file_terms:
                canonical = self._canonical(term.term)
                if canonical not in merged:
                    merged[canonical] = GlossaryTerm(
                        term=term.term,
                        definition=term.definition,
                        aliases=list(term.aliases),
                        occurrences=term.occurrences,
                        first_line=term.first_line,
                        context=term.context,
                    )
                else:
                    existing = merged[canonical]
                    existing.occurrences += term.occurrences
                    # Merge aliases
                    for alias in term.aliases:
                        if alias not in existing.aliases:
                            existing.aliases.append(alias)

        return sorted(merged.values(), key=lambda t: t.term.lower())

    def find_term(
        self, terms: list[GlossaryTerm], query: str
    ) -> Optional[GlossaryTerm]:
        """Look up a term case-insensitively.

        Also matches against aliases.

        Parameters
        ----------
        terms:
            The glossary list returned by :meth:`build`.
        query:
            Term string to search for.

        Returns
        -------
        GlossaryTerm or None
        """
        q = query.lower().strip()
        for term in terms:
            if term.term.lower() == q:
                return term
            if any(a.lower() == q for a in term.aliases):
                return term
        return None

    def to_markdown(self, terms: list[GlossaryTerm]) -> str:
        """Render glossary as Markdown.

        Each term produces::

            ## Term

            definition

        Parameters
        ----------
        terms:
            The glossary list to render.

        Returns
        -------
        str
            Markdown-formatted glossary.
        """
        if not terms:
            return ""
        parts: list[str] = []
        for term in terms:
            parts.append(f"## {term.term}\n\n{term.definition}\n\n")
        return "".join(parts)

    def to_dict(self, terms: list[GlossaryTerm]) -> list[dict]:
        """Serialize glossary to a list of plain dicts.

        Parameters
        ----------
        terms:
            The glossary list to serialize.

        Returns
        -------
        list[dict]
            One dict per :class:`GlossaryTerm`.
        """
        return [
            {
                "term": t.term,
                "definition": t.definition,
                "aliases": list(t.aliases),
                "occurrences": t.occurrences,
                "first_line": t.first_line,
                "context": t.context,
            }
            for t in terms
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _canonical(phrase: str) -> str:
        """Return a normalised lower-case key for deduplication."""
        return phrase.lower().strip()
