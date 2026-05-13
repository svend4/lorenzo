"""Standard geohash encode/decode/neighbors using stdlib only.

Geohash is a public-domain geocoding system invented by Gustavo Niemeyer that
encodes a (lat, lon) pair as a base32 string by interleaving the binary
subdivisions of latitude (-90..90) and longitude (-180..180).
"""
from __future__ import annotations

from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Alphabet
# ---------------------------------------------------------------------------

BASE32: str = "0123456789bcdefghjkmnpqrstuvwxyz"
_BASE32_INDEX: Dict[str, int] = {c: i for i, c in enumerate(BASE32)}

# ---------------------------------------------------------------------------
# Neighbour substitution tables (standard geohash algorithm)
# ---------------------------------------------------------------------------

# For each direction (n,s,e,w) and parity (even/odd index from the right),
# NEIGHBOR maps each base32 character to its neighbour character.
# BORDER lists characters which sit on the border of a 4×8 sub-grid; for those
# the parent geohash has to be adjusted recursively.

_NEIGHBOR = {
    "n": {
        "even": "p0r21436x8zb9dcf5h7kjnmqesgutwvy",
        "odd":  "bc01fg45238967deuvhjyznpkmstqrwx",
    },
    "s": {
        "even": "14365h7k9dcfesgujnmqp0r2twvyx8zb",
        "odd":  "238967debc01fg45kmstqrwxuvhjyznp",
    },
    "e": {
        "even": "bc01fg45238967deuvhjyznpkmstqrwx",
        "odd":  "p0r21436x8zb9dcf5h7kjnmqesgutwvy",
    },
    "w": {
        "even": "238967debc01fg45kmstqrwxuvhjyznp",
        "odd":  "14365h7k9dcfesgujnmqp0r2twvyx8zb",
    },
}

_BORDER = {
    "n": {"even": "prxz",     "odd": "bcfguvyz"},
    "s": {"even": "028b",     "odd": "0145hjnp"},
    "e": {"even": "bcfguvyz", "odd": "prxz"},
    "w": {"even": "0145hjnp", "odd": "028b"},
}


# ---------------------------------------------------------------------------
# Encoding
# ---------------------------------------------------------------------------

def encode(lat: float, lon: float, precision: int = 12) -> str:
    """Encode a (lat, lon) pair as a geohash string.

    Parameters
    ----------
    lat : float
        Latitude in degrees (-90..90).
    lon : float
        Longitude in degrees (-180..180).
    precision : int
        Number of base32 characters in the output (1..). Default 12 ≈ <1 m.

    Returns
    -------
    str
        Geohash string of length ``precision``.
    """
    if precision < 1:
        raise ValueError("precision must be >= 1")
    if not (-90.0 <= lat <= 90.0):
        raise ValueError("lat must be in [-90, 90]")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError("lon must be in [-180, 180]")

    lat_lo, lat_hi = -90.0, 90.0
    lon_lo, lon_hi = -180.0, 180.0

    out_chars = []
    bit = 0          # which of the 5 bits in the current char we're filling
    ch = 0           # current 5-bit accumulator
    even = True      # alternate between longitude (even) and latitude (odd)

    while len(out_chars) < precision:
        if even:
            mid = (lon_lo + lon_hi) / 2.0
            if lon >= mid:
                ch = (ch << 1) | 1
                lon_lo = mid
            else:
                ch = ch << 1
                lon_hi = mid
        else:
            mid = (lat_lo + lat_hi) / 2.0
            if lat >= mid:
                ch = (ch << 1) | 1
                lat_lo = mid
            else:
                ch = ch << 1
                lat_hi = mid
        even = not even
        bit += 1
        if bit == 5:
            out_chars.append(BASE32[ch])
            bit = 0
            ch = 0

    return "".join(out_chars)


# ---------------------------------------------------------------------------
# Decoding
# ---------------------------------------------------------------------------

def decode_bbox(geohash: str) -> Tuple[float, float, float, float]:
    """Return the bounding box ``(lat_min, lat_max, lon_min, lon_max)`` of the
    cell named by ``geohash``."""
    if not geohash:
        raise ValueError("geohash must be non-empty")

    lat_lo, lat_hi = -90.0, 90.0
    lon_lo, lon_hi = -180.0, 180.0
    even = True

    for c in geohash:
        c = c.lower()
        if c not in _BASE32_INDEX:
            raise ValueError(f"invalid geohash character: {c!r}")
        cd = _BASE32_INDEX[c]
        # iterate from MSB to LSB of the 5-bit char
        for mask in (16, 8, 4, 2, 1):
            bit = 1 if (cd & mask) else 0
            if even:
                mid = (lon_lo + lon_hi) / 2.0
                if bit:
                    lon_lo = mid
                else:
                    lon_hi = mid
            else:
                mid = (lat_lo + lat_hi) / 2.0
                if bit:
                    lat_lo = mid
                else:
                    lat_hi = mid
            even = not even

    return lat_lo, lat_hi, lon_lo, lon_hi


def decode(geohash: str) -> Tuple[float, float]:
    """Decode a geohash to its centre ``(lat, lon)``."""
    lat_lo, lat_hi, lon_lo, lon_hi = decode_bbox(geohash)
    return (lat_lo + lat_hi) / 2.0, (lon_lo + lon_hi) / 2.0


# ---------------------------------------------------------------------------
# Neighbours
# ---------------------------------------------------------------------------

def _adjacent(geohash: str, direction: str) -> str:
    """Return the geohash cell adjacent to ``geohash`` in ``direction``
    (one of 'n', 's', 'e', 'w')."""
    if not geohash:
        raise ValueError("geohash must be non-empty")
    if direction not in _NEIGHBOR:
        raise ValueError(f"invalid direction: {direction!r}")

    gh = geohash.lower()
    last = gh[-1]
    parent = gh[:-1]
    # Standard geohash convention: type is 'even' when length is even,
    # 'odd' when length is odd. Geohash chars at even index (0-based) encode
    # 3 lon + 2 lat bits; odd-index chars encode 2 lon + 3 lat bits.
    typ = "odd" if (len(gh) % 2) == 1 else "even"

    if last in _BORDER[direction][typ] and parent != "":
        parent = _adjacent(parent, direction)
    elif last in _BORDER[direction][typ] and parent == "":
        # Border of world: there is no parent. Standard geohash libraries
        # typically return an empty string here, but for our 'neighbors' API
        # we still want a usable cell, so we return the substituted char alone.
        nb_pos = _NEIGHBOR[direction][typ].index(last)
        return BASE32[nb_pos]

    # Standard algorithm: position of last char within neighbour table → base32 char.
    nb_pos = _NEIGHBOR[direction][typ].index(last)
    return parent + BASE32[nb_pos]


def neighbors(geohash: str) -> Dict[str, str]:
    """Return all 8 neighbours of ``geohash`` as a dict keyed by direction.

    Keys: ``"n", "ne", "e", "se", "s", "sw", "w", "nw"``.
    """
    n = _adjacent(geohash, "n")
    s = _adjacent(geohash, "s")
    e = _adjacent(geohash, "e")
    w = _adjacent(geohash, "w")
    ne = _adjacent(n, "e")
    nw = _adjacent(n, "w")
    se = _adjacent(s, "e")
    sw = _adjacent(s, "w")
    return {
        "n": n,
        "ne": ne,
        "e": e,
        "se": se,
        "s": s,
        "sw": sw,
        "w": w,
        "nw": nw,
    }
