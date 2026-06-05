"""Multi-modal metadata module for docs-toolkit (E31).

Provides asset type classification, metadata extraction from markdown/HTML,
and an in-memory index for querying multi-modal assets.
"""
from docstoolkit.multimodal_meta.asset import AssetMetadata, AssetType
from docstoolkit.multimodal_meta.extractor import AssetPattern, MetadataExtractor
from docstoolkit.multimodal_meta.index import MultiModalIndex

__all__ = [
    "AssetType",
    "AssetMetadata",
    "AssetPattern",
    "MetadataExtractor",
    "MultiModalIndex",
]
