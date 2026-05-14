"""EmbeddingPersistence: save/load an EmbeddingStore to/from JSON."""

from __future__ import annotations

import json
from pathlib import Path

from docstoolkit.embedding_store.store import EmbeddingStore, StoreConfig
from docstoolkit.embedding_store.vector import EmbeddingVector


class EmbeddingPersistence:
    """Serialise and deserialise an EmbeddingStore as JSON."""

    # Schema version stored in every file so future changes can migrate data.
    _SCHEMA_VERSION = 1

    @staticmethod
    def save(store: EmbeddingStore, path: str | Path) -> None:
        """Serialise *store* to a JSON file at *path*.

        The file contains:
        - schema_version  (int)
        - config          (dict with dimension, metric, normalize_on_add)
        - vectors         (list of dicts with doc_id, vector, metadata, created_at)
        """
        cfg = store._config
        data: dict = {
            "schema_version": EmbeddingPersistence._SCHEMA_VERSION,
            "config": {
                "dimension": cfg.dimension,
                "metric": cfg.metric,
                "normalize_on_add": cfg.normalize_on_add,
            },
            "vectors": [
                {
                    "doc_id": v.doc_id,
                    "vector": v.vector,
                    "metadata": v.metadata,
                    "created_at": v.created_at,
                }
                for v in store._vectors.values()
            ],
        }
        path = Path(path)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def load(path: str | Path) -> EmbeddingStore:
        """Deserialise an EmbeddingStore from the JSON file at *path*."""
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))

        cfg_data = data["config"]
        config = StoreConfig(
            dimension=cfg_data["dimension"],
            metric=cfg_data["metric"],
            normalize_on_add=cfg_data["normalize_on_add"],
        )
        store = EmbeddingStore(config=config)

        for item in data.get("vectors", []):
            vec = EmbeddingVector(
                doc_id=item["doc_id"],
                vector=item["vector"],
                metadata=item.get("metadata", {}),
                created_at=item.get("created_at", 0.0),
            )
            # Vectors were already normalised before saving (if normalize_on_add
            # was True); we bypass normalisation on load to preserve the exact
            # stored values by temporarily disabling normalize_on_add.
            original_flag = store._config.normalize_on_add
            store._config.normalize_on_add = False
            store.add(vec)
            store._config.normalize_on_add = original_flag

        return store
