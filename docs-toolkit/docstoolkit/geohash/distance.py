"""Great-circle distance calculations using the haversine formula."""
from __future__ import annotations

import math

from docstoolkit.geohash.hash import decode

# Mean Earth radius in metres (IUGG / WGS-84 spherical approximation).
EARTH_RADIUS_M: float = 6_371_000.0


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance in metres between two points.

    Uses the haversine formula on a sphere of radius :data:`EARTH_RADIUS_M`.

    Parameters
    ----------
    lat1, lon1 : float
        First point in degrees.
    lat2, lon2 : float
        Second point in degrees.

    Returns
    -------
    float
        Distance in metres (always >= 0).
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2.0) ** 2
    )
    # Clamp a to [0, 1] to defend against tiny FP overshoots near antipodes.
    a = min(1.0, max(0.0, a))
    c = 2.0 * math.asin(math.sqrt(a))
    return EARTH_RADIUS_M * c


def haversine_geohash(gh1: str, gh2: str) -> float:
    """Convenience: distance in metres between the centres of two geohash cells."""
    lat1, lon1 = decode(gh1)
    lat2, lon2 = decode(gh2)
    return haversine(lat1, lon1, lat2, lon2)
