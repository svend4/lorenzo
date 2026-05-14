"""Faceted search with filter aggregation, drill-down, and hierarchical facets."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class FacetType(Enum):
    SINGLE = "single"
    MULTI = "multi"
    HIERARCHICAL = "hierarchical"
    RANGE = "range"
    DATE = "date"


@dataclass
class FacetField:
    name: str
    facet_type: FacetType
    display_name: Optional[str] = None
    hierarchical_separator: str = "/"

    def __post_init__(self):
        if self.display_name is None:
            self.display_name = self.name


@dataclass
class FacetValue:
    value: Any
    count: int
    selected: bool = False
    children: list = field(default_factory=list)


@dataclass
class FacetResult:
    field: FacetField
    values: list
    selected_values: list = field(default_factory=list)


@dataclass
class FacetedQuery:
    filters: dict = field(default_factory=dict)
    text_query: Optional[str] = None


@dataclass
class FacetedSearchResult:
    matching_docs: list
    total_count: int
    facets: list


class DocSearchFacets:
    """Faceted search engine with drill-down and hierarchical aggregation."""

    def __init__(self):
        self._lock = threading.Lock()
        self._facets: dict[str, FacetField] = {}
        # doc_id -> {field_name -> list of values}
        self._doc_fields: dict[str, dict[str, list]] = {}
        # doc_id -> content (lowercased) for text search
        self._doc_content: dict[str, str] = {}

    def register_facet(
        self,
        name: str,
        facet_type: FacetType,
        display_name: Optional[str] = None,
        hierarchical_separator: str = "/",
    ) -> FacetField:
        if not name:
            raise ValueError("Facet name must be non-empty")
        if not isinstance(facet_type, FacetType):
            raise TypeError("facet_type must be a FacetType")
        with self._lock:
            f = FacetField(
                name=name,
                facet_type=facet_type,
                display_name=display_name,
                hierarchical_separator=hierarchical_separator,
            )
            self._facets[name] = f
            return f

    def get_facet(self, name: str) -> Optional[FacetField]:
        with self._lock:
            return self._facets.get(name)

    def all_field_names(self) -> list:
        with self._lock:
            return list(self._facets.keys())

    @property
    def total_docs(self) -> int:
        with self._lock:
            return len(self._doc_fields)

    def index_doc(self, doc_id: str, fields: dict, content: str = "") -> None:
        if not doc_id:
            raise ValueError("doc_id must be non-empty")
        if not isinstance(fields, dict):
            raise TypeError("fields must be a dict")
        with self._lock:
            stored: dict[str, list] = {}
            for fname, value in fields.items():
                if fname not in self._facets:
                    # ignore unregistered fields silently? Better: store anyway as MULTI-style
                    # We'll require facet registered for indexing to be meaningful but won't fail.
                    if isinstance(value, list):
                        stored[fname] = list(value)
                    else:
                        stored[fname] = [value]
                    continue
                facet = self._facets[fname]
                if facet.facet_type == FacetType.MULTI:
                    if isinstance(value, (list, tuple, set)):
                        stored[fname] = list(value)
                    else:
                        stored[fname] = [value]
                elif facet.facet_type in (FacetType.SINGLE, FacetType.RANGE, FacetType.DATE):
                    if isinstance(value, (list, tuple)):
                        if len(value) == 0:
                            stored[fname] = []
                        else:
                            stored[fname] = [value[0]]
                    else:
                        stored[fname] = [value]
                elif facet.facet_type == FacetType.HIERARCHICAL:
                    if isinstance(value, (list, tuple, set)):
                        stored[fname] = [str(v) for v in value]
                    else:
                        stored[fname] = [str(value)]
                else:
                    stored[fname] = [value] if not isinstance(value, list) else list(value)
            self._doc_fields[doc_id] = stored
            self._doc_content[doc_id] = (content or "").lower()

    def unindex_doc(self, doc_id: str) -> bool:
        with self._lock:
            if doc_id in self._doc_fields:
                del self._doc_fields[doc_id]
                self._doc_content.pop(doc_id, None)
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._facets.clear()
            self._doc_fields.clear()
            self._doc_content.clear()

    # --------------------- searching ---------------------

    def _doc_matches_filter(self, doc_id: str, field_name: str, selected: list) -> bool:
        """Check if a single doc passes filter for one field (OR within values)."""
        if not selected:
            return True
        doc_vals = self._doc_fields.get(doc_id, {}).get(field_name, [])
        if not doc_vals:
            return False
        facet = self._facets.get(field_name)
        if facet and facet.facet_type == FacetType.HIERARCHICAL:
            sep = facet.hierarchical_separator
            for sel in selected:
                sel_str = str(sel)
                for dv in doc_vals:
                    dv_str = str(dv)
                    if dv_str == sel_str or dv_str.startswith(sel_str + sep):
                        return True
            return False
        if facet and facet.facet_type == FacetType.RANGE:
            # selected: list of (low, high) tuples or single values
            for sel in selected:
                for dv in doc_vals:
                    if isinstance(sel, (tuple, list)) and len(sel) == 2:
                        low, high = sel
                        try:
                            if (low is None or dv >= low) and (high is None or dv <= high):
                                return True
                        except TypeError:
                            pass
                    else:
                        if dv == sel:
                            return True
            return False
        # SINGLE / MULTI / DATE / other: exact match OR semantics
        for sel in selected:
            if sel in doc_vals:
                return True
        return False

    def _docs_matching_query(self, query: FacetedQuery) -> list:
        out = []
        text = (query.text_query or "").strip().lower()
        for doc_id, stored in self._doc_fields.items():
            ok = True
            for fname, sel in query.filters.items():
                if not self._doc_matches_filter(doc_id, fname, sel or []):
                    ok = False
                    break
            if not ok:
                continue
            if text:
                content = self._doc_content.get(doc_id, "")
                if text not in content:
                    # also search across stored values' string form
                    found = False
                    for vlist in stored.values():
                        for v in vlist:
                            if text in str(v).lower():
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        continue
            out.append(doc_id)
        return out

    def search(self, query: FacetedQuery) -> FacetedSearchResult:
        if not isinstance(query, FacetedQuery):
            raise TypeError("query must be a FacetedQuery")
        with self._lock:
            matching = self._docs_matching_query(query)
            facets = self._facets_for_locked(matching, None, query.filters)
            return FacetedSearchResult(
                matching_docs=list(matching),
                total_count=len(matching),
                facets=facets,
            )

    # --------------------- facets aggregation ---------------------

    def _facets_for_locked(
        self,
        doc_ids: Optional[list],
        field_names: Optional[list],
        selected_filters: Optional[dict] = None,
    ) -> list:
        if doc_ids is None:
            ids = list(self._doc_fields.keys())
        else:
            ids = [d for d in doc_ids if d in self._doc_fields]
        names = field_names if field_names is not None else list(self._facets.keys())
        selected_filters = selected_filters or {}
        results = []
        for fname in names:
            facet = self._facets.get(fname)
            if facet is None:
                continue
            selected_vals = list(selected_filters.get(fname, []) or [])
            if facet.facet_type == FacetType.HIERARCHICAL:
                values = self._aggregate_hierarchical(facet, ids, selected_vals)
            else:
                values = self._aggregate_flat(facet, ids, selected_vals)
            results.append(
                FacetResult(field=facet, values=values, selected_values=selected_vals)
            )
        return results

    def _aggregate_flat(
        self, facet: FacetField, doc_ids: list, selected_vals: list
    ) -> list:
        counts: dict = {}
        for doc_id in doc_ids:
            vals = self._doc_fields.get(doc_id, {}).get(facet.name, [])
            seen_in_doc = set()
            for v in vals:
                key = self._hashable(v)
                if key in seen_in_doc:
                    continue
                seen_in_doc.add(key)
                counts[key] = counts.get(key, 0) + 1
        sel_set = {self._hashable(s) for s in selected_vals}
        out = []
        # original_value mapping
        for doc_id in doc_ids:
            for v in self._doc_fields.get(doc_id, {}).get(facet.name, []):
                k = self._hashable(v)
                if k in counts and k not in {self._hashable(x.value) for x in out}:
                    out.append(
                        FacetValue(
                            value=v,
                            count=counts[k],
                            selected=k in sel_set,
                        )
                    )
        # sort by count desc, then by value str
        out.sort(key=lambda fv: (-fv.count, str(fv.value)))
        return out

    def _aggregate_hierarchical(
        self, facet: FacetField, doc_ids: list, selected_vals: list
    ) -> list:
        sep = facet.hierarchical_separator
        # path -> count of docs containing this path or any descendant
        path_counts: dict[str, int] = {}
        # tree: parent_path -> set of immediate child paths
        children_map: dict[str, set] = {}

        for doc_id in doc_ids:
            paths = self._doc_fields.get(doc_id, {}).get(facet.name, [])
            covered = set()
            for raw in paths:
                p = str(raw)
                parts = [x for x in p.split(sep) if x != ""]
                cumulative = ""
                parent = ""
                for i, part in enumerate(parts):
                    cumulative = sep.join(parts[: i + 1])
                    if cumulative not in covered:
                        covered.add(cumulative)
                    children_map.setdefault(parent, set()).add(cumulative)
                    parent = cumulative
            for c in covered:
                path_counts[c] = path_counts.get(c, 0) + 1

        sel_set = {str(s) for s in selected_vals}

        def build(parent_path: str) -> list:
            kids = sorted(children_map.get(parent_path, set()))
            out = []
            for k in kids:
                fv = FacetValue(
                    value=k,
                    count=path_counts.get(k, 0),
                    selected=k in sel_set,
                    children=build(k),
                )
                out.append(fv)
            out.sort(key=lambda fv: (-fv.count, str(fv.value)))
            return out

        return build("")

    def _hashable(self, v: Any):
        try:
            hash(v)
            return v
        except TypeError:
            return repr(v)

    def facets_for(
        self,
        doc_ids: Optional[list] = None,
        field_names: Optional[list] = None,
    ) -> list:
        with self._lock:
            return self._facets_for_locked(doc_ids, field_names)

    def top_values(
        self,
        field_name: str,
        top_k: int = 10,
        doc_ids: Optional[list] = None,
    ) -> list:
        with self._lock:
            facet = self._facets.get(field_name)
            if facet is None:
                return []
            ids = list(self._doc_fields.keys()) if doc_ids is None else [
                d for d in doc_ids if d in self._doc_fields
            ]
            if facet.facet_type == FacetType.HIERARCHICAL:
                values = self._aggregate_hierarchical(facet, ids, [])
            else:
                values = self._aggregate_flat(facet, ids, [])
            return values[: max(0, top_k)]

    def drill_down(
        self,
        field_name: str,
        parent_path: str = "",
        doc_ids: Optional[list] = None,
    ) -> list:
        with self._lock:
            facet = self._facets.get(field_name)
            if facet is None or facet.facet_type != FacetType.HIERARCHICAL:
                return []
            sep = facet.hierarchical_separator
            ids = list(self._doc_fields.keys()) if doc_ids is None else [
                d for d in doc_ids if d in self._doc_fields
            ]
            # Build children counts directly for parent_path
            child_counts: dict[str, int] = {}
            children_set: dict[str, None] = {}
            for doc_id in ids:
                paths = self._doc_fields.get(doc_id, {}).get(facet.name, [])
                child_seen = set()
                for raw in paths:
                    p = str(raw)
                    parts = [x for x in p.split(sep) if x != ""]
                    if parent_path == "":
                        if not parts:
                            continue
                        child = parts[0]
                    else:
                        parent_parts = [x for x in parent_path.split(sep) if x != ""]
                        if len(parts) <= len(parent_parts):
                            continue
                        if parts[: len(parent_parts)] != parent_parts:
                            continue
                        child = sep.join(parts[: len(parent_parts) + 1])
                    if child not in child_seen:
                        child_seen.add(child)
                for c in child_seen:
                    child_counts[c] = child_counts.get(c, 0) + 1
                    children_set[c] = None
            out = []
            for c in children_set.keys():
                out.append(FacetValue(value=c, count=child_counts[c]))
            out.sort(key=lambda fv: (-fv.count, str(fv.value)))
            return out

    def count_for_value(
        self,
        field_name: str,
        value: Any,
        doc_ids: Optional[list] = None,
    ) -> int:
        with self._lock:
            facet = self._facets.get(field_name)
            if facet is None:
                return 0
            ids = list(self._doc_fields.keys()) if doc_ids is None else [
                d for d in doc_ids if d in self._doc_fields
            ]
            cnt = 0
            for doc_id in ids:
                if self._doc_matches_filter(doc_id, field_name, [value]):
                    cnt += 1
            return cnt
