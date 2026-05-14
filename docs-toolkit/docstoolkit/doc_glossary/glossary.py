"""DocGlossary — CRUD-style glossary manager with auto-linking."""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Term:
    """A glossary term entry."""

    term: str
    definition: str
    category: Optional[str] = None
    examples: list[str] = field(default_factory=list)
    synonyms: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    created_at: float = 0.0
    updated_at: float = 0.0


@dataclass
class GlossaryStats:
    """Aggregate statistics over the glossary."""

    total_terms: int = 0
    total_synonyms: int = 0
    total_categories: int = 0
    terms_by_category: dict = field(default_factory=dict)
    terms_with_examples: int = 0


def _slugify(text: str) -> str:
    """Convert a term to an anchor slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


class DocGlossary:
    """Thread-safe glossary manager with auto-link rendering."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # Canonical storage: lower-cased term -> Term
        self._terms: dict[str, Term] = {}
        # Synonym lookup: lower-cased synonym -> canonical lower-cased term
        self._syn_index: dict[str, str] = {}

    # ---------- internal helpers ----------

    def _key(self, text: str) -> str:
        return (text or "").strip().lower()

    def _resolve(self, name: str) -> Optional[str]:
        """Resolve any term or synonym to a canonical key."""
        k = self._key(name)
        if k in self._terms:
            return k
        if k in self._syn_index:
            return self._syn_index[k]
        return None

    # ---------- CRUD ----------

    def add_term(
        self,
        term: str,
        definition: str,
        category: Optional[str] = None,
        examples: Optional[list[str]] = None,
        synonyms: Optional[list[str]] = None,
        related: Optional[list[str]] = None,
        now: float = 0.0,
    ) -> Term:
        """Register a new term. Raises ValueError on duplicate or empty."""
        if not term or not term.strip():
            raise ValueError("term must not be empty")
        if definition is None:
            raise ValueError("definition is required")
        key = self._key(term)
        with self._lock:
            if key in self._terms:
                raise ValueError(f"term already exists: {term!r}")
            t = Term(
                term=term.strip(),
                definition=definition,
                category=category,
                examples=list(examples) if examples else [],
                synonyms=list(synonyms) if synonyms else [],
                related=list(related) if related else [],
                created_at=now,
                updated_at=now,
            )
            self._terms[key] = t
            for syn in t.synonyms:
                sk = self._key(syn)
                if sk and sk != key:
                    self._syn_index[sk] = key
            return t

    def update_term(
        self,
        term: str,
        definition: Optional[str] = None,
        category: Optional[str] = None,
        examples: Optional[list[str]] = None,
        synonyms: Optional[list[str]] = None,
        related: Optional[list[str]] = None,
        now: float = 0.0,
    ) -> Optional[Term]:
        """Update fields on an existing term. Returns the updated Term, or None if not found."""
        with self._lock:
            key = self._resolve(term)
            if key is None:
                return None
            t = self._terms[key]
            if definition is not None:
                t.definition = definition
            if category is not None:
                t.category = category
            if examples is not None:
                t.examples = list(examples)
            if synonyms is not None:
                # Remove old synonym entries belonging to this term
                for sk in list(self._syn_index.keys()):
                    if self._syn_index[sk] == key:
                        del self._syn_index[sk]
                t.synonyms = list(synonyms)
                for syn in t.synonyms:
                    sk = self._key(syn)
                    if sk and sk != key:
                        self._syn_index[sk] = key
            if related is not None:
                t.related = list(related)
            t.updated_at = now
            return t

    def remove_term(self, term: str) -> bool:
        """Remove a term (and its synonyms). Returns True if removed."""
        with self._lock:
            key = self._resolve(term)
            if key is None:
                return False
            # Clear synonyms pointing here
            for sk in list(self._syn_index.keys()):
                if self._syn_index[sk] == key:
                    del self._syn_index[sk]
            del self._terms[key]
            # Also clear related references in other terms
            for other in self._terms.values():
                other.related = [
                    r for r in other.related if self._key(r) != key
                ]
            return True

    def get_term(self, term: str) -> Optional[Term]:
        """Look up a term by canonical name or synonym."""
        with self._lock:
            key = self._resolve(term)
            if key is None:
                return None
            return self._terms[key]

    # ---------- Synonyms ----------

    def add_synonym(self, term: str, synonym: str) -> bool:
        """Add a synonym to an existing term."""
        if not synonym or not synonym.strip():
            return False
        with self._lock:
            key = self._resolve(term)
            if key is None:
                return False
            sk = self._key(synonym)
            if sk == key:
                return False
            t = self._terms[key]
            if synonym not in t.synonyms:
                t.synonyms.append(synonym)
            self._syn_index[sk] = key
            return True

    def remove_synonym(self, term: str, synonym: str) -> bool:
        """Remove a synonym from a term."""
        with self._lock:
            key = self._resolve(term)
            if key is None:
                return False
            t = self._terms[key]
            sk = self._key(synonym)
            # find original-cased synonym in list
            removed = False
            new_list = []
            for s in t.synonyms:
                if self._key(s) == sk:
                    removed = True
                    continue
                new_list.append(s)
            if not removed:
                return False
            t.synonyms = new_list
            if sk in self._syn_index and self._syn_index[sk] == key:
                del self._syn_index[sk]
            return True

    # ---------- Related ----------

    def add_related(self, term: str, related_term: str) -> bool:
        """Add a related-term reference. Both must already exist."""
        with self._lock:
            key = self._resolve(term)
            rkey = self._resolve(related_term)
            if key is None or rkey is None or key == rkey:
                return False
            t = self._terms[key]
            r = self._terms[rkey]
            if r.term not in t.related and not any(
                self._key(x) == rkey for x in t.related
            ):
                t.related.append(r.term)
                return True
            return False

    def remove_related(self, term: str, related_term: str) -> bool:
        """Remove a related-term reference."""
        with self._lock:
            key = self._resolve(term)
            if key is None:
                return False
            t = self._terms[key]
            rk = self._key(related_term)
            new_list = [r for r in t.related if self._key(r) != rk]
            if len(new_list) == len(t.related):
                return False
            t.related = new_list
            return True

    # ---------- Queries ----------

    def find_by_category(self, category: str) -> list[Term]:
        """All terms in a category (case-insensitive match)."""
        ck = (category or "").strip().lower()
        with self._lock:
            return [
                t
                for t in self._terms.values()
                if (t.category or "").strip().lower() == ck
            ]

    def find_by_keyword(self, keyword: str) -> list[Term]:
        """Terms whose definition contains the keyword (case-insensitive)."""
        kw = (keyword or "").lower()
        if not kw:
            return []
        with self._lock:
            return [
                t for t in self._terms.values() if kw in t.definition.lower()
            ]

    def search(self, query: str) -> list[Term]:
        """Search term name, definition, examples, and synonyms."""
        q = (query or "").lower()
        if not q:
            return []
        results = []
        with self._lock:
            for t in self._terms.values():
                if (
                    q in t.term.lower()
                    or q in t.definition.lower()
                    or any(q in e.lower() for e in t.examples)
                    or any(q in s.lower() for s in t.synonyms)
                ):
                    results.append(t)
        return results

    def all_terms(self) -> list[Term]:
        """Return all terms sorted alphabetically."""
        with self._lock:
            return sorted(self._terms.values(), key=lambda t: t.term.lower())

    def categories(self) -> list[str]:
        """Distinct categories, sorted."""
        with self._lock:
            cats = {
                t.category for t in self._terms.values() if t.category
            }
        return sorted(cats)

    # ---------- Auto-link ----------

    def _build_link_targets(self) -> list[tuple[str, str]]:
        """Return list of (display_text, canonical_term) sorted by length desc.

        Longer phrases take precedence so they match before shorter substrings.
        """
        targets: list[tuple[str, str]] = []
        for key, t in self._terms.items():
            targets.append((t.term, t.term))
            for s in t.synonyms:
                if s.strip():
                    targets.append((s, t.term))
        # Sort by length desc, then by text for determinism
        targets.sort(key=lambda x: (-len(x[0]), x[0]))
        return targets

    @staticmethod
    def _protected_spans(text: str) -> list[tuple[int, int]]:
        """Return character ranges that should NOT be linked.

        Covers fenced code blocks ```...```, inline code `...`, and existing
        markdown links [text](url).
        """
        spans: list[tuple[int, int]] = []
        # Fenced code blocks
        for m in re.finditer(r"```.*?```", text, flags=re.DOTALL):
            spans.append((m.start(), m.end()))
        # Inline code
        for m in re.finditer(r"`[^`\n]+`", text):
            spans.append((m.start(), m.end()))
        # Existing markdown links [..](..)
        for m in re.finditer(r"\[[^\]]*\]\([^)]*\)", text):
            spans.append((m.start(), m.end()))
        spans.sort()
        return spans

    @staticmethod
    def _in_span(pos: int, spans: list[tuple[int, int]]) -> bool:
        for s, e in spans:
            if s <= pos < e:
                return True
        return False

    def auto_link(self, text: str, term_format: str = "[{term}](#{slug})") -> str:
        """Replace term mentions with links.

        Match whole words case-insensitively. Avoids replacing inside code
        blocks, inline code, or existing markdown links. Each term has at
        most one replacement per text.
        """
        if not text:
            return text
        with self._lock:
            targets = self._build_link_targets()

        replaced_terms: set = set()
        out = text

        for display, canonical in targets:
            ckey = canonical.lower()
            if ckey in replaced_terms:
                continue
            if not display.strip():
                continue
            pattern = re.compile(
                r"\b" + re.escape(display) + r"\b", flags=re.IGNORECASE
            )

            # Re-compute protected spans each iteration since `out` changes
            spans = self._protected_spans(out)
            match = None
            for m in pattern.finditer(out):
                if not self._in_span(m.start(), spans):
                    match = m
                    break
            if match is None:
                continue

            link = term_format.format(
                term=match.group(0), slug=_slugify(canonical)
            )
            out = out[: match.start()] + link + out[match.end() :]
            replaced_terms.add(ckey)

        return out

    def extract_mentioned(self, text: str) -> list[str]:
        """Return canonical term names mentioned in the text (deduplicated)."""
        if not text:
            return []
        with self._lock:
            targets = self._build_link_targets()
        spans = self._protected_spans(text)
        found: list[str] = []
        seen: set = set()
        for display, canonical in targets:
            ck = canonical.lower()
            if ck in seen or not display.strip():
                continue
            pattern = re.compile(
                r"\b" + re.escape(display) + r"\b", flags=re.IGNORECASE
            )
            for m in pattern.finditer(text):
                if not self._in_span(m.start(), spans):
                    found.append(canonical)
                    seen.add(ck)
                    break
        return found

    # ---------- Serialization ----------

    def to_markdown(self) -> str:
        """Render the glossary as Markdown grouped by category."""
        with self._lock:
            terms = sorted(self._terms.values(), key=lambda t: t.term.lower())
            if not terms:
                return "# Glossary\n\n_No terms._\n"

            by_cat: dict[str, list[Term]] = {}
            for t in terms:
                cat = t.category or "Uncategorized"
                by_cat.setdefault(cat, []).append(t)

            lines: list[str] = ["# Glossary", ""]
            for cat in sorted(by_cat.keys()):
                lines.append(f"## {cat}")
                lines.append("")
                for t in by_cat[cat]:
                    slug = _slugify(t.term)
                    lines.append(f"### <a id=\"{slug}\"></a>{t.term}")
                    lines.append("")
                    lines.append(t.definition)
                    lines.append("")
                    if t.synonyms:
                        lines.append(
                            "**Synonyms:** " + ", ".join(t.synonyms)
                        )
                        lines.append("")
                    if t.examples:
                        lines.append("**Examples:**")
                        for ex in t.examples:
                            lines.append(f"- {ex}")
                        lines.append("")
                    if t.related:
                        lines.append(
                            "**Related:** " + ", ".join(t.related)
                        )
                        lines.append("")
            return "\n".join(lines).rstrip() + "\n"

    def to_dict(self) -> list[dict]:
        """Serialize all terms to a list of plain dicts."""
        with self._lock:
            return [
                {
                    "term": t.term,
                    "definition": t.definition,
                    "category": t.category,
                    "examples": list(t.examples),
                    "synonyms": list(t.synonyms),
                    "related": list(t.related),
                    "created_at": t.created_at,
                    "updated_at": t.updated_at,
                }
                for t in sorted(
                    self._terms.values(), key=lambda x: x.term.lower()
                )
            ]

    def from_dict(self, data: list[dict]) -> int:
        """Bulk load terms. Returns count loaded. Skips duplicates."""
        if not data:
            return 0
        count = 0
        for entry in data:
            term = entry.get("term")
            definition = entry.get("definition", "")
            if not term:
                continue
            key = self._key(term)
            with self._lock:
                if key in self._terms:
                    continue
                t = Term(
                    term=term.strip(),
                    definition=definition,
                    category=entry.get("category"),
                    examples=list(entry.get("examples") or []),
                    synonyms=list(entry.get("synonyms") or []),
                    related=list(entry.get("related") or []),
                    created_at=float(entry.get("created_at") or 0.0),
                    updated_at=float(entry.get("updated_at") or 0.0),
                )
                self._terms[key] = t
                for syn in t.synonyms:
                    sk = self._key(syn)
                    if sk and sk != key:
                        self._syn_index[sk] = key
            count += 1
        return count

    # ---------- Misc ----------

    def is_term(self, text: str) -> bool:
        """True if text matches a registered term or synonym."""
        return self._resolve(text) is not None

    def stats(self) -> GlossaryStats:
        """Aggregate statistics."""
        with self._lock:
            terms = list(self._terms.values())
            by_cat: dict[str, int] = {}
            with_ex = 0
            total_syn = 0
            for t in terms:
                cat = t.category or "Uncategorized"
                by_cat[cat] = by_cat.get(cat, 0) + 1
                total_syn += len(t.synonyms)
                if t.examples:
                    with_ex += 1
            cats = {t.category for t in terms if t.category}
            return GlossaryStats(
                total_terms=len(terms),
                total_synonyms=total_syn,
                total_categories=len(cats),
                terms_by_category=by_cat,
                terms_with_examples=with_ex,
            )

    @property
    def term_count(self) -> int:
        """Number of registered terms."""
        with self._lock:
            return len(self._terms)

    def clear(self) -> None:
        """Remove all terms and synonyms."""
        with self._lock:
            self._terms.clear()
            self._syn_index.clear()
