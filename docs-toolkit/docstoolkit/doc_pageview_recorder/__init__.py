"""E375 DocPageviewRecorder — track page views and metrics per document.

Public API
----------
:class:`Pageview`            — a single pageview event
:class:`DocViewStats`        — pageview statistics for a single doc
:class:`RecorderStats`       — aggregate recorder statistics
:class:`DocPageviewRecorder` — main interface for pageview tracking
"""

from .recorder import Pageview, DocViewStats, RecorderStats, DocPageviewRecorder

__all__ = ["Pageview", "DocViewStats", "RecorderStats", "DocPageviewRecorder"]
