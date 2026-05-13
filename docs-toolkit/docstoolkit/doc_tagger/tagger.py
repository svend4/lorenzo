"""Rule-based document tagger.

Stdlib only. Each :class:`TagRule` defines a tag plus the keywords / regex
patterns that should trigger it. :class:`DocTagger` evaluates a set of rules
against a document and returns a :class:`TaggingResult`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class TagRule:
    """A single tagging rule.

    Parameters
    ----------
    tag:
        The tag to apply when this rule matches.
    keywords:
        Plain keywords. Each *unique* keyword that appears in the document
        counts as one match.
    patterns:
        Regular expressions. ``re.findall`` is used; every match counts.
    min_matches:
        Total number of matches (keywords + patterns) required to fire.
    excluded_keywords:
        If any of these keywords is present the rule is skipped entirely.
    """

    tag: str
    keywords: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)
    min_matches: int = 1
    excluded_keywords: list[str] = field(default_factory=list)


@dataclass
class TaggingResult:
    """Outcome of tagging a single document."""

    doc_id: str
    tags: list[str]
    matched_rules: list[str]
    score_by_tag: dict[str, int]


@dataclass
class TaggerConfig:
    """Configuration affecting how matching is performed."""

    case_sensitive: bool = False
    whole_word: bool = True
    max_tags: int = 0  # 0 = unlimited


# ---------------------------------------------------------------------------
# DocTagger
# ---------------------------------------------------------------------------


class DocTagger:
    """Apply :class:`TagRule` definitions to documents."""

    #: Regex used by :meth:`extract_existing_tags`.
    _HASHTAG_RE = re.compile(r"(?<![\w&])#([A-Za-z0-9_\-]+)")

    def __init__(self, config: TaggerConfig | None = None) -> None:
        self.config = config or TaggerConfig()
        self._rules: dict[str, TagRule] = {}

    # ------------------------------------------------------------------
    # Rule management
    # ------------------------------------------------------------------
    def add_rule(self, rule: TagRule) -> None:
        """Add or replace a rule (keyed by ``rule.tag``)."""
        if not isinstance(rule, TagRule):
            raise TypeError("rule must be a TagRule instance")
        if not rule.tag:
            raise ValueError("rule.tag must be non-empty")
        self._rules[rule.tag] = rule

    def add_rules(self, rules: list[TagRule]) -> None:
        for rule in rules:
            self.add_rule(rule)

    def remove_rule(self, tag: str) -> bool:
        """Remove a rule by tag. Returns ``True`` if a rule was removed."""
        return self._rules.pop(tag, None) is not None

    def clear(self) -> None:
        """Remove every rule."""
        self._rules.clear()

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    @property
    def tags_supported(self) -> list[str]:
        return sorted(self._rules.keys())

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate_rule(self, rule: TagRule) -> tuple[bool, list[str]]:
        """Return ``(valid, errors)`` for a rule."""
        errors: list[str] = []
        if not isinstance(rule, TagRule):
            return False, ["rule is not a TagRule instance"]
        if not rule.tag or not rule.tag.strip():
            errors.append("tag must be non-empty")
        if not rule.keywords and not rule.patterns:
            errors.append("rule must define at least one keyword or pattern")
        if rule.min_matches < 1:
            errors.append("min_matches must be >= 1")
        for pattern in rule.patterns:
            try:
                re.compile(pattern)
            except re.error as exc:  # pragma: no cover - message varies
                errors.append(f"invalid regex {pattern!r}: {exc}")
        return (not errors), errors

    # ------------------------------------------------------------------
    # Tagging
    # ------------------------------------------------------------------
    def tag(self, text: str, doc_id: str = "doc") -> TaggingResult:
        """Tag a single document and return a :class:`TaggingResult`."""
        haystack = text if self.config.case_sensitive else text.lower()
        re_flags = 0 if self.config.case_sensitive else re.IGNORECASE

        applied: list[tuple[str, int]] = []  # (tag, total_matches)
        matched_rules: list[str] = []

        for rule in self._rules.values():
            if self._is_excluded(rule, haystack):
                continue

            keyword_matches = self._count_keyword_hits(rule.keywords, haystack)
            pattern_matches = self._count_pattern_hits(rule.patterns, text, re_flags)
            total = keyword_matches + pattern_matches

            if total >= rule.min_matches:
                applied.append((rule.tag, total))
                matched_rules.append(rule.tag)

        # Honour max_tags by keeping highest-scoring entries.
        if self.config.max_tags > 0 and len(applied) > self.config.max_tags:
            applied.sort(key=lambda item: (-item[1], item[0]))
            applied = applied[: self.config.max_tags]
            kept = {tag for tag, _ in applied}
            matched_rules = [t for t in matched_rules if t in kept]

        score_by_tag = {tag: score for tag, score in applied}
        tags = sorted({tag for tag, _ in applied})
        matched_rules = sorted(set(matched_rules))
        return TaggingResult(
            doc_id=doc_id,
            tags=tags,
            matched_rules=matched_rules,
            score_by_tag=score_by_tag,
        )

    def tag_batch(self, docs: dict[str, str]) -> list[TaggingResult]:
        """Tag many documents (``{doc_id: text}``)."""
        return [self.tag(text, doc_id) for doc_id, text in docs.items()]

    # ------------------------------------------------------------------
    # Existing tag helpers
    # ------------------------------------------------------------------
    def extract_existing_tags(self, text: str) -> list[str]:
        """Return ``#hashtag`` occurrences (without the ``#``) sorted unique."""
        if not text:
            return []
        found = self._HASHTAG_RE.findall(text)
        return sorted(set(found))

    def merge_tags(self, existing: list[str], new: list[str]) -> list[str]:
        """Return the sorted, unique union of two tag lists."""
        return sorted({*existing, *new})

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _is_excluded(self, rule: TagRule, haystack: str) -> bool:
        for kw in rule.excluded_keywords:
            if self._keyword_in_text(kw, haystack):
                return True
        return False

    def _count_keyword_hits(self, keywords: list[str], haystack: str) -> int:
        if not keywords:
            return 0
        seen: set[str] = set()
        for kw in keywords:
            if not kw:
                continue
            normalized = kw if self.config.case_sensitive else kw.lower()
            if normalized in seen:
                continue
            if self._keyword_in_text(kw, haystack):
                seen.add(normalized)
        return len(seen)

    def _keyword_in_text(self, keyword: str, haystack: str) -> bool:
        if not keyword:
            return False
        needle = keyword if self.config.case_sensitive else keyword.lower()
        if self.config.whole_word:
            pattern = r"(?<!\w)" + re.escape(needle) + r"(?!\w)"
            return re.search(pattern, haystack) is not None
        return needle in haystack

    def _count_pattern_hits(self, patterns: list[str], text: str, flags: int) -> int:
        total = 0
        for pat in patterns:
            if not pat:
                continue
            try:
                compiled = re.compile(pat, flags)
            except re.error:
                continue
            total += len(compiled.findall(text))
        return total
