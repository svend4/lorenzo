"""Doc clip module for docs-toolkit.

Public API
----------
- ``Clip``           — a single text clip from a document
- ``ClipCollection`` — named collection of clip ids
- ``DocClip``        — manager for clips and collections
"""

from docstoolkit.doc_clip.clip import (
    Clip,
    ClipCollection,
    DocClip,
)

__all__ = [
    "Clip",
    "ClipCollection",
    "DocClip",
]
