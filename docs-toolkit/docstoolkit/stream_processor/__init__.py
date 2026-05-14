"""Stream processor module — E173.

Composable, fluent, lazy streaming operations over any iterable.
Pure stdlib (``itertools``, ``functools``) — no third-party dependencies.

Quick start::

    from docstoolkit.stream_processor import Stream

    result = (
        Stream(range(100))
        .filter(lambda x: x % 2 == 0)
        .map(lambda x: x * x)
        .take(5)
        .to_list()
    )
    # [0, 4, 16, 36, 64]

Public API
----------
- ``Stream`` — fluent lazy iterable wrapper with map/filter/reduce/window etc.
"""

from docstoolkit.stream_processor.stream import Stream

__all__ = ["Stream"]
