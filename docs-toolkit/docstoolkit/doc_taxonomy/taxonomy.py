"""Document taxonomy: hierarchical terms, categories, and rule-based classification.

This module provides:
- ``TaxonomyTerm``: a node in a taxonomy tree.
- ``Classification``: a binding between a doc and a term.
- ``ClassificationRule``: a callable-based rule that classifies docs.
- ``DocTaxonomy``: a thread-safe container for multiple taxonomies.

All operations are protected by a single ``threading.Lock``.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class TaxonomyTerm:
    """A single term in a taxonomy hierarchy."""

    term_id: str
    name: str
    parent_id: Optional[str] = None
    taxonomy: str = "default"
    synonyms: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class Classification:
    """A binding between a document and a taxonomy term."""

    doc_id: str
    term_id: str
    confidence: float = 1.0
    assigned_by: Optional[str] = None
    assigned_at: float = 0.0


@dataclass
class ClassificationRule:
    """A rule that classifies documents based on a callable condition."""

    rule_id: str
    name: str
    term_id: str
    condition: Callable[[dict], bool]
    enabled: bool = True
    confidence: float = 1.0


class DocTaxonomy:
    """Thread-safe document taxonomy manager."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._terms: dict[str, TaxonomyTerm] = {}
        # (doc_id, term_id) -> Classification
        self._classifications: dict[tuple[str, str], Classification] = {}
        self._rules: dict[str, ClassificationRule] = {}
        self._term_counter = 0
        self._rule_counter = 0

    # ------------------------------------------------------------------ #
    # Term management                                                    #
    # ------------------------------------------------------------------ #
    def add_term(
        self,
        name: str,
        parent_id: Optional[str] = None,
        taxonomy: str = "default",
        synonyms: Optional[list[str]] = None,
        metadata: Optional[dict] = None,
    ) -> TaxonomyTerm:
        """Add a new term and return it."""
        with self._lock:
            if parent_id is not None and parent_id not in self._terms:
                raise ValueError(f"parent term '{parent_id}' does not exist")
            if parent_id is not None:
                parent = self._terms[parent_id]
                if parent.taxonomy != taxonomy:
                    raise ValueError(
                        f"parent taxonomy '{parent.taxonomy}' does not match '{taxonomy}'"
                    )
            self._term_counter += 1
            term_id = f"term_{self._term_counter}"
            term = TaxonomyTerm(
                term_id=term_id,
                name=name,
                parent_id=parent_id,
                taxonomy=taxonomy,
                synonyms=list(synonyms) if synonyms else [],
                metadata=dict(metadata) if metadata else {},
            )
            self._terms[term_id] = term
            return term

    def remove_term(self, term_id: str) -> bool:
        """Remove a term, all descendants and any related classifications."""
        with self._lock:
            if term_id not in self._terms:
                return False
            to_remove = {term_id}
            # collect all descendants
            stack = [term_id]
            while stack:
                current = stack.pop()
                for tid, term in self._terms.items():
                    if term.parent_id == current and tid not in to_remove:
                        to_remove.add(tid)
                        stack.append(tid)
            # drop terms
            for tid in to_remove:
                self._terms.pop(tid, None)
            # drop classifications referencing any removed term
            keys_to_drop = [
                key for key in self._classifications if key[1] in to_remove
            ]
            for key in keys_to_drop:
                self._classifications.pop(key, None)
            return True

    def move_term(self, term_id: str, new_parent_id: Optional[str] = None) -> bool:
        """Move a term to a new parent. Returns False on missing term or cycle."""
        with self._lock:
            if term_id not in self._terms:
                return False
            if new_parent_id is not None and new_parent_id not in self._terms:
                return False
            if new_parent_id == term_id:
                return False
            term = self._terms[term_id]
            if new_parent_id is not None:
                new_parent = self._terms[new_parent_id]
                if new_parent.taxonomy != term.taxonomy:
                    return False
                # cycle detection: new_parent cannot be a descendant of term
                cursor = new_parent
                while cursor.parent_id is not None:
                    if cursor.parent_id == term_id:
                        return False
                    cursor = self._terms[cursor.parent_id]
            term.parent_id = new_parent_id
            return True

    def get_term(self, term_id: str) -> Optional[TaxonomyTerm]:
        """Return the term, or None."""
        with self._lock:
            return self._terms.get(term_id)

    def find_by_name(
        self, name: str, taxonomy: Optional[str] = None
    ) -> Optional[TaxonomyTerm]:
        """Find a term by exact name (within a taxonomy if specified)."""
        with self._lock:
            for term in self._terms.values():
                if term.name != name:
                    continue
                if taxonomy is not None and term.taxonomy != taxonomy:
                    continue
                return term
            return None

    def find_by_synonym(self, synonym: str) -> Optional[TaxonomyTerm]:
        """Find the first term that lists ``synonym`` in its synonyms."""
        with self._lock:
            for term in self._terms.values():
                if synonym in term.synonyms:
                    return term
            return None

    def add_synonym(self, term_id: str, synonym: str) -> bool:
        with self._lock:
            term = self._terms.get(term_id)
            if term is None:
                return False
            if synonym in term.synonyms:
                return False
            term.synonyms.append(synonym)
            return True

    def remove_synonym(self, term_id: str, synonym: str) -> bool:
        with self._lock:
            term = self._terms.get(term_id)
            if term is None:
                return False
            if synonym not in term.synonyms:
                return False
            term.synonyms.remove(synonym)
            return True

    def children(self, term_id: str) -> list[TaxonomyTerm]:
        with self._lock:
            if term_id not in self._terms:
                return []
            return [t for t in self._terms.values() if t.parent_id == term_id]

    def descendants(self, term_id: str) -> list[TaxonomyTerm]:
        with self._lock:
            if term_id not in self._terms:
                return []
            result: list[TaxonomyTerm] = []
            stack = [term_id]
            while stack:
                current = stack.pop()
                for t in self._terms.values():
                    if t.parent_id == current:
                        result.append(t)
                        stack.append(t.term_id)
            return result

    def ancestors(self, term_id: str) -> list[TaxonomyTerm]:
        with self._lock:
            term = self._terms.get(term_id)
            if term is None:
                return []
            result: list[TaxonomyTerm] = []
            cursor_id = term.parent_id
            seen: set[str] = set()
            while cursor_id is not None and cursor_id not in seen:
                seen.add(cursor_id)
                parent = self._terms.get(cursor_id)
                if parent is None:
                    break
                result.append(parent)
                cursor_id = parent.parent_id
            return result

    def root_terms(self, taxonomy: str = "default") -> list[TaxonomyTerm]:
        with self._lock:
            return [
                t
                for t in self._terms.values()
                if t.parent_id is None and t.taxonomy == taxonomy
            ]

    def all_terms(self, taxonomy: Optional[str] = None) -> list[TaxonomyTerm]:
        with self._lock:
            if taxonomy is None:
                return list(self._terms.values())
            return [t for t in self._terms.values() if t.taxonomy == taxonomy]

    def taxonomies(self) -> list[str]:
        with self._lock:
            return sorted({t.taxonomy for t in self._terms.values()})

    # ------------------------------------------------------------------ #
    # Classification                                                     #
    # ------------------------------------------------------------------ #
    def classify(
        self,
        doc_id: str,
        term_id: str,
        confidence: float = 1.0,
        assigned_by: str = "manual",
        now: float = 0.0,
    ) -> Optional[Classification]:
        """Bind ``doc_id`` to ``term_id``. Returns the Classification or None if term missing."""
        with self._lock:
            if term_id not in self._terms:
                return None
            classification = Classification(
                doc_id=doc_id,
                term_id=term_id,
                confidence=confidence,
                assigned_by=assigned_by,
                assigned_at=now,
            )
            self._classifications[(doc_id, term_id)] = classification
            return classification

    def unclassify(self, doc_id: str, term_id: str) -> bool:
        with self._lock:
            key = (doc_id, term_id)
            if key not in self._classifications:
                return False
            del self._classifications[key]
            return True

    def classifications_for_doc(self, doc_id: str) -> list[Classification]:
        with self._lock:
            return [c for c in self._classifications.values() if c.doc_id == doc_id]

    def docs_for_term(
        self, term_id: str, include_descendants: bool = False
    ) -> list[str]:
        with self._lock:
            if term_id not in self._terms:
                return []
            target_terms = {term_id}
            if include_descendants:
                stack = [term_id]
                while stack:
                    current = stack.pop()
                    for t in self._terms.values():
                        if t.parent_id == current and t.term_id not in target_terms:
                            target_terms.add(t.term_id)
                            stack.append(t.term_id)
            seen: list[str] = []
            seen_set: set[str] = set()
            for c in self._classifications.values():
                if c.term_id in target_terms and c.doc_id not in seen_set:
                    seen.append(c.doc_id)
                    seen_set.add(c.doc_id)
            return seen

    # ------------------------------------------------------------------ #
    # Rules                                                              #
    # ------------------------------------------------------------------ #
    def add_rule(
        self,
        name: str,
        term_id: str,
        condition: Callable[[dict], bool],
        confidence: float = 1.0,
    ) -> ClassificationRule:
        with self._lock:
            if term_id not in self._terms:
                raise ValueError(f"term '{term_id}' does not exist")
            self._rule_counter += 1
            rule_id = f"rule_{self._rule_counter}"
            rule = ClassificationRule(
                rule_id=rule_id,
                name=name,
                term_id=term_id,
                condition=condition,
                enabled=True,
                confidence=confidence,
            )
            self._rules[rule_id] = rule
            return rule

    def remove_rule(self, rule_id: str) -> bool:
        with self._lock:
            if rule_id not in self._rules:
                return False
            del self._rules[rule_id]
            return True

    def apply_rules(
        self, doc_id: str, doc_data: dict, now: float = 0.0
    ) -> list[Classification]:
        """Apply all enabled rules to ``doc_data``; return the produced classifications."""
        # Build list of rules under lock, then evaluate conditions without lock,
        # then re-acquire to apply classifications.
        with self._lock:
            rules_snapshot = [r for r in self._rules.values() if r.enabled]

        produced: list[Classification] = []
        for rule in rules_snapshot:
            try:
                matched = bool(rule.condition(doc_data))
            except Exception:
                matched = False
            if not matched:
                continue
            with self._lock:
                if rule.term_id not in self._terms:
                    continue
                classification = Classification(
                    doc_id=doc_id,
                    term_id=rule.term_id,
                    confidence=rule.confidence,
                    assigned_by=rule.rule_id,
                    assigned_at=now,
                )
                self._classifications[(doc_id, rule.term_id)] = classification
                produced.append(classification)
        return produced

    # ------------------------------------------------------------------ #
    # Aggregates                                                         #
    # ------------------------------------------------------------------ #
    @property
    def term_count(self) -> int:
        with self._lock:
            return len(self._terms)

    def doc_count(self) -> int:
        with self._lock:
            return len({c.doc_id for c in self._classifications.values()})

    def clear(self) -> None:
        with self._lock:
            self._terms.clear()
            self._classifications.clear()
            self._rules.clear()
            self._term_counter = 0
            self._rule_counter = 0
