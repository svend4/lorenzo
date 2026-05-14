"""Metadata extractor for docs-toolkit — stdlib only."""
from docstoolkit.metadata_extractor.document import (
    DocumentMetadata,
    DocumentMetadataExtractor,
)
from docstoolkit.metadata_extractor.extractor import MetadataExtractor
from docstoolkit.metadata_extractor.fields import (
    ExtractionSchema,
    ExtractedField,
    FieldType,
)

__all__ = [
    "FieldType",
    "ExtractedField",
    "ExtractionSchema",
    "MetadataExtractor",
    "DocumentMetadata",
    "DocumentMetadataExtractor",
]
