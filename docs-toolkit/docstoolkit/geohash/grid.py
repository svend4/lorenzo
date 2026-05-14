"""A spatial grid that indexes points by geohash cells.

The grid is a thin wrapper around a ``dict[str, list]`` that maps geohashes at a
fixed precision to the points falling inside them. It provides O(1) cell lookup
and an approximate-then-exact radius query.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from docstoolkit.geohash.distance import haversine
from docstoolkit.geohash.hash import encode, neighbors

# Each stored point is a 3-tuple (lat, lon, payload). payload may be None.
Point = Tuple[float, float, Any]


class GeoGrid:
    """An in-memory grid of (lat, lon, payload) points indexed by geohash.

    Examples
    --------
    >>> g = GeoGrid(precision=6)
    >>> gh = g.add(40.7128, -74.0060, payload="NYC")
    >>> g.query_cell(gh)
    [(40.7128, -74.006, 'NYC')]
    """

    def __init__(self, precision: int = 6) -> None:
        if precision < 1:
            raise ValueError("precision must be >= 1")
        self.precision: int = precision
        self.points: Dict[str, List[Point]] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, lat: float, lon: float, payload: Any = None) -> str:
        """Add a point at ``(lat, lon)`` with optional ``payload`` and return its geohash."""
        gh = encode(lat, lon, self.precision)
        self.points.setdefault(gh, []).append((lat, lon, payload))
        return gh

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def query_cell(self, geohash: str) -> List[Point]:
        """Return points stored in the exact cell ``geohash``.

        Returns a copy of the internal list so callers may safely mutate the
        result without affecting the grid.
        """
        return list(self.points.get(geohash, []))

    def query_neighbors(
        self, geohash: str, include_center: bool = True
    ) -> List[Point]:
        """Return all points in the cell ``geohash`` and its 8 neighbours.

        If ``include_center`` is False, the centre cell is omitted.
        """
        result: List[Point] = []
        if include_center:
            result.extend(self.points.get(geohash, []))
        for ngh in neighbors(geohash).values():
            result.extend(self.points.get(ngh, []))
        return result

    def query_radius(
        self, lat: float, lon: float, radius_m: float
    ) -> List[Point]:
        """Return points within ``radius_m`` metres of ``(lat, lon)``.

        The implementation first narrows candidates to the geohash cell of the
        query point plus its 8 neighbours (a coarse but very fast filter), then
        applies the exact haversine distance.

        Notes
        -----
        Using only the cell + 1-ring of neighbours is sufficient when the
        search radius is no larger than roughly half the cell diagonal at the
        grid's precision; for larger radii callers should choose a coarser
        precision when constructing the grid.
        """
        if radius_m < 0:
            raise ValueError("radius_m must be >= 0")
        gh = encode(lat, lon, self.precision)
        candidates: List[Point] = []
        candidates.extend(self.points.get(gh, []))
        for ngh in neighbors(gh).values():
            candidates.extend(self.points.get(ngh, []))
        return [
            p
            for p in candidates
            if haversine(lat, lon, p[0], p[1]) <= radius_m
        ]

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def count(self) -> int:
        """Return the total number of points stored across all cells."""
        return sum(len(v) for v in self.points.values())

    def cells(self) -> List[str]:
        """Return the list of non-empty geohash cells (sorted for determinism)."""
        return sorted(k for k, v in self.points.items() if v)
