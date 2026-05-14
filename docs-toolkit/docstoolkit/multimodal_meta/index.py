"""In-memory index for multi-modal asset metadata."""
from __future__ import annotations

from docstoolkit.multimodal_meta.asset import AssetMetadata, AssetType


class MultiModalIndex:
    """Stores and queries :class:`AssetMetadata` objects."""

    def __init__(self) -> None:
        self._store: dict[str, AssetMetadata] = {}

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def add(self, asset: AssetMetadata) -> None:
        """Add *asset* to the index (overwrites if same asset_id)."""
        self._store[asset.asset_id] = asset

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get(self, asset_id: str) -> AssetMetadata | None:
        """Return asset by its unique *asset_id*, or ``None`` if absent."""
        return self._store.get(asset_id)

    def by_type(self, asset_type: AssetType) -> list[AssetMetadata]:
        """Return all assets of the given *asset_type*."""
        return [a for a in self._store.values() if a.asset_type == asset_type]

    def by_doc(self, doc_id: str) -> list[AssetMetadata]:
        """Return all assets that belong to document *doc_id*."""
        return [a for a in self._store.values() if a.source_doc == doc_id]

    def search_by_tag(self, tag: str) -> list[AssetMetadata]:
        """Return assets whose tag list contains *tag* (case-insensitive)."""
        tag_lower = tag.lower()
        return [
            a for a in self._store.values()
            if any(t.lower() == tag_lower for t in a.tags)
        ]

    def search_by_text(self, query: str) -> list[AssetMetadata]:
        """Return assets whose alt_text or caption contains all query tokens.

        The match is case-insensitive and requires every whitespace-separated
        token in *query* to appear in the combined ``alt_text + caption`` text.
        """
        tokens = [t.lower() for t in query.split() if t]
        if not tokens:
            return list(self._store.values())
        result = []
        for asset in self._store.values():
            combined = (asset.alt_text + " " + asset.caption).lower()
            if all(tok in combined for tok in tokens):
                result.append(asset)
        return result

    # ------------------------------------------------------------------
    # Aggregates
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return a dict with total count and per-type breakdown."""
        by_type: dict[str, int] = {}
        for asset in self._store.values():
            key = asset.asset_type.value
            by_type[key] = by_type.get(key, 0) + 1
        return {
            "total": len(self._store),
            "by_type": by_type,
        }

    def asset_count(self) -> int:
        """Return the total number of assets in the index."""
        return len(self._store)
