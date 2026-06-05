"""IndexPersistence: save and load SearchIndexManager to/from JSON (E62)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Union

from docstoolkit.search_index_mgr.index import IndexEntry
from docstoolkit.search_index_mgr.manager import IndexConfig, SearchIndexManager


class IndexPersistence:
    """Serialize and deserialize a SearchIndexManager to/from a JSON file."""

    @staticmethod
    def save(manager: SearchIndexManager, path: Union[str, Path]) -> None:
        """Serialize the manager's entries and inverted index to a JSON file.

        The saved JSON has two top-level keys:
        - ``entries``: list of serialized IndexEntry dicts.
        - ``inverted``: the term -> {doc_id: tf} mapping.
        """
        path = Path(path)
        entries_data = []
        for entry in manager._entries.values():
            entries_data.append({
                "doc_id": entry.doc_id,
                "title": entry.title,
                "content": entry.content,
                "tags": entry.tags,
                "metadata": entry.metadata,
                "indexed_at": entry.indexed_at,
            })

        payload = {
            "entries": entries_data,
            "inverted": manager._inverted,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def load(
        path: Union[str, Path],
        config: Optional[IndexConfig] = None,
    ) -> SearchIndexManager:
        """Reconstruct a SearchIndexManager from a JSON file.

        The inverted index and doc_terms are rebuilt from the saved data so
        that search works immediately after loading.
        """
        path = Path(path)
        payload = json.loads(path.read_text(encoding="utf-8"))

        manager = SearchIndexManager(config=config)

        # Restore entries and build doc_terms / tag_index
        for e in payload.get("entries", []):
            entry = IndexEntry(
                doc_id=e["doc_id"],
                title=e["title"],
                content=e["content"],
                tags=e.get("tags", []),
                metadata=e.get("metadata", {}),
                indexed_at=e.get("indexed_at", 0.0),
            )
            manager._entries[entry.doc_id] = entry
            manager._tag_index[entry.doc_id] = set(entry.tags)

            # Rebuild doc_terms from the restored inverted index (done below),
            # but we need tokens now for doc_terms.  Re-tokenise from content.
            from docstoolkit.search_index_mgr.manager import _tokenize
            raw_tokens = _tokenize(entry.title + " " + entry.content)
            filtered = manager._filter_tokens(raw_tokens)
            filtered = filtered[: manager._config.max_terms_per_doc]
            manager._doc_terms[entry.doc_id] = filtered

        # Restore the inverted index directly (preserves tf values exactly)
        for term, postings in payload.get("inverted", {}).items():
            manager._inverted[term] = dict(postings)

        return manager
