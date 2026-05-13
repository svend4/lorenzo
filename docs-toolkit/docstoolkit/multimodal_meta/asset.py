"""Asset types and metadata dataclass for multi-modal documents."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class AssetType(Enum):
    TEXT = "text"
    IMAGE = "image"
    TABLE = "table"
    CODE = "code"
    DIAGRAM = "diagram"
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"


def _auto_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class AssetMetadata:
    """Metadata for a single multi-modal asset within a document."""

    source_doc: str
    asset_type: AssetType
    asset_id: str = field(default_factory=_auto_id)
    mime_type: str = ""
    width: int = 0
    height: int = 0
    duration_sec: float = 0.0
    language: str = ""
    alt_text: str = ""
    caption: str = ""
    tags: list[str] = field(default_factory=list)
    created_ts: float = field(default_factory=time.time)

    def is_visual(self) -> bool:
        """Return True for visually rendered asset types (IMAGE, DIAGRAM)."""
        return self.asset_type in (AssetType.IMAGE, AssetType.DIAGRAM)

    def is_temporal(self) -> bool:
        """Return True for time-based asset types (AUDIO, VIDEO)."""
        return self.asset_type in (AssetType.AUDIO, AssetType.VIDEO)

    def word_count(self) -> int:
        """Count words in alt_text and caption combined."""
        alt_words = len(self.alt_text.split()) if self.alt_text.strip() else 0
        cap_words = len(self.caption.split()) if self.caption.strip() else 0
        return alt_words + cap_words
