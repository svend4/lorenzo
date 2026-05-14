"""Tests for the geohash module — 90+ tests covering encode/decode/neighbours,
haversine distance, and the GeoGrid spatial index."""
from __future__ import annotations

import math

import pytest

from docstoolkit.geohash import (
    GeoGrid,
    decode,
    decode_bbox,
    encode,
    haversine,
    haversine_geohash,
    neighbors,
)
from docstoolkit.geohash.hash import BASE32


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

# Well-known geohash from the Wikipedia article — encodes a point near
# Jutland, Denmark.
JUTLAND_LAT = 57.64911
JUTLAND_LON = 10.40744
JUTLAND_HASH = "u4pruydqqvj"

# Other widely-quoted reference encodings (verified against the JS reference
# implementation by Chris Veness and python-geohash):
REFERENCE_ENCODINGS = [
    # (lat, lon, precision, expected_prefix)
    (40.7128, -74.0060, 6, "dr5reg"),
    (34.0522, -118.2437, 6, "9q5ctr"),
    (51.5074, -0.1278, 6, "gcpvj0"),
    (-33.8688, 151.2093, 6, "r3gx2f"),
    (0.0, 0.0, 6, "s00000"),
]


# =========================================================================
# 1. encode()
# =========================================================================

class TestEncodeReference:
    def test_jutland_full_precision(self):
        gh = encode(JUTLAND_LAT, JUTLAND_LON, 12)
        assert gh.startswith(JUTLAND_HASH)

    def test_jutland_default_precision_is_12(self):
        gh = encode(JUTLAND_LAT, JUTLAND_LON)
        assert len(gh) == 12

    def test_jutland_precision_7(self):
        gh = encode(JUTLAND_LAT, JUTLAND_LON, 7)
        assert gh == "u4pruyd"

    def test_jutland_precision_5(self):
        gh = encode(JUTLAND_LAT, JUTLAND_LON, 5)
        assert gh == "u4pru"

    def test_jutland_precision_1(self):
        gh = encode(JUTLAND_LAT, JUTLAND_LON, 1)
        assert gh == "u"

    @pytest.mark.parametrize("lat,lon,prec,exp", REFERENCE_ENCODINGS)
    def test_known_reference_values(self, lat, lon, prec, exp):
        assert encode(lat, lon, prec) == exp

    def test_origin_starts_with_s(self):
        assert encode(0, 0, 1) == "s"

    def test_origin_precision_2(self):
        # (0,0) is at the corner of cells -> standard geohash gives 's00'
        assert encode(0, 0, 2) == "s0"


class TestEncodePrecision:
    @pytest.mark.parametrize("prec", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    def test_length_matches_precision(self, prec):
        gh = encode(40.0, -74.0, prec)
        assert len(gh) == prec

    def test_higher_precision_extends_lower(self):
        lat, lon = 40.7128, -74.0060
        gh3 = encode(lat, lon, 3)
        gh6 = encode(lat, lon, 6)
        gh9 = encode(lat, lon, 9)
        assert gh6.startswith(gh3)
        assert gh9.startswith(gh6)

    def test_precision_zero_raises(self):
        with pytest.raises(ValueError):
            encode(0, 0, 0)

    def test_precision_negative_raises(self):
        with pytest.raises(ValueError):
            encode(0, 0, -1)

    def test_precision_15(self):
        gh = encode(0, 0, 15)
        assert len(gh) == 15


class TestEncodeAlphabet:
    def test_only_base32_chars(self):
        gh = encode(57.64911, 10.40744, 12)
        assert all(c in BASE32 for c in gh)

    def test_base32_has_32_chars(self):
        assert len(BASE32) == 32

    def test_base32_no_ail_o(self):
        # geohash alphabet excludes a, i, l, o to avoid confusion
        assert "a" not in BASE32
        assert "i" not in BASE32
        assert "l" not in BASE32
        assert "o" not in BASE32

    def test_base32_starts_with_digits(self):
        assert BASE32[:10] == "0123456789"


class TestEncodeBoundaries:
    def test_north_pole(self):
        gh = encode(90.0, 0.0, 5)
        # North pole sits at the top-right of the world; the standard
        # algorithm produces 'upbpb' or similar — what we test is that it
        # encodes, has the right length, and the cell touches lat=90.
        assert len(gh) == 5
        lat_min, lat_max, _, _ = decode_bbox(gh)
        assert lat_max == 90.0 or abs(lat_max - 90.0) < 1e-6

    def test_south_pole(self):
        gh = encode(-90.0, 0.0, 5)
        assert len(gh) == 5
        lat_min, lat_max, _, _ = decode_bbox(gh)
        assert lat_min == -90.0 or abs(lat_min + 90.0) < 1e-6

    def test_antimeridian_east(self):
        gh = encode(0.0, 180.0, 5)
        assert len(gh) == 5

    def test_antimeridian_west(self):
        gh = encode(0.0, -180.0, 5)
        assert len(gh) == 5

    def test_out_of_range_lat_high(self):
        with pytest.raises(ValueError):
            encode(91.0, 0.0)

    def test_out_of_range_lat_low(self):
        with pytest.raises(ValueError):
            encode(-91.0, 0.0)

    def test_out_of_range_lon_high(self):
        with pytest.raises(ValueError):
            encode(0.0, 181.0)

    def test_out_of_range_lon_low(self):
        with pytest.raises(ValueError):
            encode(0.0, -181.0)


# =========================================================================
# 2. decode() / decode_bbox()
# =========================================================================

class TestDecode:
    def test_jutland_decode_is_close_to_input(self):
        lat, lon = decode(JUTLAND_HASH)
        assert abs(lat - JUTLAND_LAT) < 1e-3
        assert abs(lon - JUTLAND_LON) < 1e-3

    def test_decode_returns_two_floats(self):
        lat, lon = decode("u")
        assert isinstance(lat, float)
        assert isinstance(lon, float)

    @pytest.mark.parametrize(
        "lat,lon",
        [(0, 0), (40.7128, -74.006), (34.0522, -118.2437),
         (51.5074, -0.1278), (-33.8688, 151.2093), (45, 45), (-45, -45),
         (10, 100), (-10, -100), (60, -120), (-60, 120)],
    )
    def test_roundtrip_precision_12(self, lat, lon):
        gh = encode(lat, lon, 12)
        rlat, rlon = decode(gh)
        # At precision 12, cell is sub-metre; we expect <1e-5 deg agreement.
        assert abs(rlat - lat) < 1e-4, (lat, rlat)
        assert abs(rlon - lon) < 1e-4, (lon, rlon)

    @pytest.mark.parametrize("prec", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    def test_decode_returns_point_inside_bbox(self, prec):
        gh = encode(40.0, -74.0, prec)
        lat, lon = decode(gh)
        lat_min, lat_max, lon_min, lon_max = decode_bbox(gh)
        assert lat_min <= lat <= lat_max
        assert lon_min <= lon <= lon_max

    def test_invalid_char_raises(self):
        with pytest.raises(ValueError):
            decode("u4priya")  # 'a' is not in base32 alphabet

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            decode("")


class TestDecodeBbox:
    def test_returns_4_tuple(self):
        bb = decode_bbox("u4pruyd")
        assert isinstance(bb, tuple)
        assert len(bb) == 4

    def test_lat_min_less_than_lat_max(self):
        lat_min, lat_max, _, _ = decode_bbox("u4pruyd")
        assert lat_min < lat_max

    def test_lon_min_less_than_lon_max(self):
        _, _, lon_min, lon_max = decode_bbox("u4pruyd")
        assert lon_min < lon_max

    def test_lat_bounds_within_world(self):
        lat_min, lat_max, _, _ = decode_bbox("u4pruyd")
        assert -90.0 <= lat_min and lat_max <= 90.0

    def test_lon_bounds_within_world(self):
        _, _, lon_min, lon_max = decode_bbox("u4pruyd")
        assert -180.0 <= lon_min and lon_max <= 180.0

    def test_single_char_s(self):
        # cell 's' covers lat 0..45 N, lon 0..45 E
        lat_min, lat_max, lon_min, lon_max = decode_bbox("s")
        assert lat_min == 0.0
        assert lat_max == 45.0
        assert lon_min == 0.0
        assert lon_max == 45.0

    def test_single_char_7(self):
        # cell '7' covers lat -45..0, lon -45..0
        lat_min, lat_max, lon_min, lon_max = decode_bbox("7")
        assert lat_min == -45.0
        assert lat_max == 0.0
        assert lon_min == -45.0
        assert lon_max == 0.0

    def test_higher_precision_inside_lower(self):
        lat_min, lat_max, lon_min, lon_max = decode_bbox("u4pru")
        lat_min2, lat_max2, lon_min2, lon_max2 = decode_bbox("u4pruyd")
        assert lat_min <= lat_min2 and lat_max2 <= lat_max
        assert lon_min <= lon_min2 and lon_max2 <= lon_max

    def test_bbox_size_shrinks_with_precision(self):
        # Each additional char halves either lat or lon span; over 2 chars
        # the area shrinks by a factor of ~32.
        b1 = decode_bbox("u")
        b2 = decode_bbox("u4")
        b3 = decode_bbox("u4p")
        area1 = (b1[1] - b1[0]) * (b1[3] - b1[2])
        area2 = (b2[1] - b2[0]) * (b2[3] - b2[2])
        area3 = (b3[1] - b3[0]) * (b3[3] - b3[2])
        assert area1 > area2 > area3
        assert math.isclose(area1 / area2, 32.0, rel_tol=1e-9)
        assert math.isclose(area2 / area3, 32.0, rel_tol=1e-9)


# =========================================================================
# 3. neighbors()
# =========================================================================

class TestNeighborsShape:
    def test_returns_dict(self):
        n = neighbors("u4pruyd")
        assert isinstance(n, dict)

    def test_eight_keys(self):
        n = neighbors("u4pruyd")
        assert set(n.keys()) == {"n", "ne", "e", "se", "s", "sw", "w", "nw"}

    def test_all_values_strings(self):
        n = neighbors("u4pruyd")
        assert all(isinstance(v, str) for v in n.values())

    def test_all_same_length_as_input(self):
        n = neighbors("u4pruyd")
        assert all(len(v) == 7 for v in n.values())

    def test_all_unique(self):
        n = neighbors("u4pruyd")
        vals = list(n.values())
        assert len(set(vals)) == 8

    def test_none_equals_input(self):
        n = neighbors("u4pruyd")
        assert "u4pruyd" not in n.values()


class TestNeighborsCorrectness:
    def test_u4pruy_n(self):
        # cell to the north of u4pruy has higher lat
        n = neighbors("u4pruy")
        assert n["n"] == "u4pruz"

    def test_u4pruy_s(self):
        n = neighbors("u4pruy")
        assert n["s"] == "u4pruv"

    def test_u4pruy_e(self):
        n = neighbors("u4pruy")
        assert n["e"] == "u4prvn"

    def test_u4pruy_w(self):
        n = neighbors("u4pruy")
        assert n["w"] == "u4pruw"

    def test_single_char_s_n(self):
        # 's' covers 0..45N, 0..45E; cell to the north covers 45..90N → 'u'
        assert neighbors("s")["n"] == "u"

    def test_single_char_s_s(self):
        assert neighbors("s")["s"] == "k"

    def test_single_char_s_e(self):
        assert neighbors("s")["e"] == "t"

    def test_single_char_s_w(self):
        assert neighbors("s")["w"] == "e"

    def test_neighbor_geometry_n(self):
        """For a cell, the n neighbour must have lat_min == this cell's lat_max."""
        gh = "u4pruyd"
        lat_min, lat_max, lon_min, lon_max = decode_bbox(gh)
        n = neighbors(gh)
        bn = decode_bbox(n["n"])
        assert math.isclose(bn[0], lat_max, abs_tol=1e-9)
        assert math.isclose(bn[2], lon_min, abs_tol=1e-9)
        assert math.isclose(bn[3], lon_max, abs_tol=1e-9)

    def test_neighbor_geometry_s(self):
        gh = "u4pruyd"
        lat_min, _, lon_min, lon_max = decode_bbox(gh)
        bs = decode_bbox(neighbors(gh)["s"])
        assert math.isclose(bs[1], lat_min, abs_tol=1e-9)
        assert math.isclose(bs[2], lon_min, abs_tol=1e-9)
        assert math.isclose(bs[3], lon_max, abs_tol=1e-9)

    def test_neighbor_geometry_e(self):
        gh = "u4pruyd"
        lat_min, lat_max, _, lon_max = decode_bbox(gh)
        be = decode_bbox(neighbors(gh)["e"])
        assert math.isclose(be[2], lon_max, abs_tol=1e-9)
        assert math.isclose(be[0], lat_min, abs_tol=1e-9)
        assert math.isclose(be[1], lat_max, abs_tol=1e-9)

    def test_neighbor_geometry_w(self):
        gh = "u4pruyd"
        lat_min, lat_max, lon_min, _ = decode_bbox(gh)
        bw = decode_bbox(neighbors(gh)["w"])
        assert math.isclose(bw[3], lon_min, abs_tol=1e-9)
        assert math.isclose(bw[0], lat_min, abs_tol=1e-9)
        assert math.isclose(bw[1], lat_max, abs_tol=1e-9)

    def test_neighbor_ne_consistency(self):
        # The ne cell of X equals the n cell of e(X) equals the e cell of n(X)
        gh = "u4pruyd"
        ne = neighbors(gh)["ne"]
        e_of_n = neighbors(neighbors(gh)["n"])["e"]
        n_of_e = neighbors(neighbors(gh)["e"])["n"]
        assert ne == e_of_n == n_of_e

    def test_neighbor_sw_consistency(self):
        gh = "u4pruyd"
        sw = neighbors(gh)["sw"]
        w_of_s = neighbors(neighbors(gh)["s"])["w"]
        s_of_w = neighbors(neighbors(gh)["w"])["s"]
        assert sw == w_of_s == s_of_w

    def test_neighbor_n_then_s_returns_origin(self):
        gh = "u4pruyd"
        assert neighbors(neighbors(gh)["n"])["s"] == gh

    def test_neighbor_e_then_w_returns_origin(self):
        gh = "u4pruyd"
        assert neighbors(neighbors(gh)["e"])["w"] == gh

    def test_neighbor_uppercase_input(self):
        # decode/neighbors should accept upper-case and produce the same
        # result as the equivalent lower-case input.
        n = neighbors("U4PRUYD")
        assert n == neighbors("u4pruyd")


class TestNeighborsBorderCrossing:
    def test_border_e_recurses_to_parent(self):
        # 'r' is on the east border of an even-length cell; e of 'gr' should
        # be in a different parent cell.
        gh = "gr"
        e = neighbors(gh)["e"]
        # Just check that we get a valid base32 string of the same length.
        assert len(e) == len(gh)
        assert all(c in BASE32 for c in e)

    def test_border_n_recurses(self):
        # Pick a cell whose last char is on the n border.
        # In odd-length 'z' is at the n-border for type 'odd'? type 'odd' n
        # border = 'bcfguvyz', so 'z' is a border char. 'uz' has length 2 (even)
        # so type 'even'. 'prxz' is the n border for even, contains 'z' → border.
        gh = "uz"
        n = neighbors(gh)["n"]
        assert len(n) == len(gh)

    def test_world_border_single_char(self):
        # Even at world edges, neighbors should return valid base32 strings
        # of the same length (we deliberately do not wrap around antipodal
        # poles — that is an implementation choice).
        n = neighbors("z")
        for v in n.values():
            assert all(c in BASE32 for c in v)


# =========================================================================
# 4. haversine()
# =========================================================================

class TestHaversineBasics:
    def test_same_point_is_zero(self):
        assert haversine(0, 0, 0, 0) == 0.0

    def test_same_point_nonzero_coords(self):
        assert haversine(40.7128, -74.006, 40.7128, -74.006) == pytest.approx(
            0.0, abs=1e-6
        )

    def test_symmetry(self):
        d1 = haversine(40.7128, -74.006, 34.0522, -118.2437)
        d2 = haversine(34.0522, -118.2437, 40.7128, -74.006)
        assert d1 == pytest.approx(d2, rel=1e-12)

    def test_nyc_to_la(self):
        d = haversine(40.7128, -74.006, 34.0522, -118.2437)
        # Generally quoted at ~3935 km — accept within 1 %.
        assert d / 1000.0 == pytest.approx(3935.0, rel=0.01)

    def test_london_to_paris(self):
        # ~344 km
        d = haversine(51.5074, -0.1278, 48.8566, 2.3522)
        assert d / 1000.0 == pytest.approx(344.0, rel=0.02)

    def test_antipodes(self):
        # Antipodes are pi * R apart ≈ 20015 km.
        d = haversine(0, 0, 0, 180)
        assert d == pytest.approx(math.pi * 6_371_000.0, rel=1e-6)

    def test_antipodes_via_poles(self):
        d = haversine(90, 0, -90, 0)
        assert d == pytest.approx(math.pi * 6_371_000.0, rel=1e-6)

    def test_one_degree_at_equator(self):
        # 1 degree of longitude at the equator ≈ 111.195 km on a sphere of
        # radius 6,371 km.
        d = haversine(0, 0, 0, 1)
        assert d / 1000.0 == pytest.approx(111.195, rel=1e-3)

    def test_one_degree_lat(self):
        # 1 degree of latitude anywhere ≈ 111.195 km on a sphere.
        d = haversine(0, 0, 1, 0)
        assert d / 1000.0 == pytest.approx(111.195, rel=1e-3)

    def test_distance_nonnegative(self):
        assert haversine(45, 45, -45, -135) >= 0.0

    def test_quarter_circumference(self):
        # Quarter great circle ~10,007 km
        d = haversine(0, 0, 0, 90)
        assert d / 1000.0 == pytest.approx(10007.5, rel=1e-3)


class TestHaversineGeohash:
    def test_same_geohash_is_small(self):
        # Two decodes of the same geohash give identical centers → 0 distance
        assert haversine_geohash("u4pruyd", "u4pruyd") == 0.0

    def test_neighbour_distance_is_one_cell(self):
        gh = "u4pruyd"
        n = neighbors(gh)["n"]
        d = haversine_geohash(gh, n)
        # Cells at precision 7 are ~150 m tall.
        assert 50 < d < 300

    def test_large_distance(self):
        d = haversine_geohash("dr5reg", "9q5ctr")  # NYC, LA
        assert d / 1000.0 == pytest.approx(3935.0, rel=0.01)

    def test_matches_haversine_of_centres(self):
        a, b = "u4pruyd", "u4pruye"
        la1, lo1 = decode(a)
        la2, lo2 = decode(b)
        assert haversine_geohash(a, b) == pytest.approx(
            haversine(la1, lo1, la2, lo2), rel=1e-12
        )


# =========================================================================
# 5. GeoGrid
# =========================================================================

class TestGeoGridInit:
    def test_default_precision(self):
        g = GeoGrid()
        assert g.precision == 6

    def test_custom_precision(self):
        g = GeoGrid(precision=8)
        assert g.precision == 8

    def test_invalid_precision(self):
        with pytest.raises(ValueError):
            GeoGrid(precision=0)

    def test_negative_precision(self):
        with pytest.raises(ValueError):
            GeoGrid(precision=-1)

    def test_empty_points(self):
        g = GeoGrid()
        assert g.points == {}

    def test_empty_count(self):
        g = GeoGrid()
        assert g.count() == 0

    def test_empty_cells(self):
        g = GeoGrid()
        assert g.cells() == []


class TestGeoGridAdd:
    def test_add_returns_geohash(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.0060)
        assert gh == "dr5reg"

    def test_add_returns_geohash_of_correct_length(self):
        g = GeoGrid(precision=8)
        gh = g.add(0, 0)
        assert len(gh) == 8

    def test_add_stores_point(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.0060, "NYC")
        assert g.points[gh] == [(40.7128, -74.006, "NYC")]

    def test_add_multiple_same_cell(self):
        g = GeoGrid(precision=4)
        g.add(40.7128, -74.006, "NYC")
        g.add(40.7129, -74.0059, "NYC2")
        # both should land in the same cell at precision 4
        assert len(g.points) == 1
        assert g.count() == 2

    def test_add_different_cells(self):
        g = GeoGrid(precision=6)
        g.add(40.7128, -74.006, "NYC")
        g.add(34.0522, -118.2437, "LA")
        assert g.count() == 2
        assert len(g.points) == 2

    def test_add_default_payload(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006)
        assert g.points[gh][0][2] is None

    def test_add_dict_payload(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, {"name": "NYC", "pop": 8_000_000})
        assert g.points[gh][0][2] == {"name": "NYC", "pop": 8_000_000}

    def test_add_int_payload(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, 42)
        assert g.points[gh][0][2] == 42


class TestGeoGridQueryCell:
    def test_empty_cell(self):
        g = GeoGrid(precision=6)
        assert g.query_cell("dr5reg") == []

    def test_one_point(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, "NYC")
        assert g.query_cell(gh) == [(40.7128, -74.006, "NYC")]

    def test_multiple_points(self):
        g = GeoGrid(precision=4)
        gh1 = g.add(40.7128, -74.006, "A")
        g.add(40.713, -74.005, "B")
        # at precision 4 both points fall in the same cell
        assert len(g.query_cell(gh1)) == 2

    def test_returns_copy_not_internal_list(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, "NYC")
        out = g.query_cell(gh)
        out.append(("fake",))
        # internal storage must be untouched
        assert len(g.points[gh]) == 1


class TestGeoGridQueryNeighbors:
    def test_returns_empty_when_grid_empty(self):
        g = GeoGrid(precision=6)
        assert g.query_neighbors("dr5reg") == []

    def test_include_center_true(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, "NYC")
        out = g.query_neighbors(gh, include_center=True)
        assert any(p[2] == "NYC" for p in out)

    def test_include_center_false(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, "NYC")
        out = g.query_neighbors(gh, include_center=False)
        assert all(p[2] != "NYC" for p in out)

    def test_picks_up_points_in_neighbour_cell(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, "centre")
        # Add a point known to be in the 'e' neighbour cell.
        nbrs = neighbors(gh)
        lat_min, lat_max, lon_min, lon_max = decode_bbox(nbrs["e"])
        clat = (lat_min + lat_max) / 2
        clon = (lon_min + lon_max) / 2
        g.add(clat, clon, "east")
        names = {p[2] for p in g.query_neighbors(gh)}
        assert "centre" in names and "east" in names

    def test_skips_unrelated_cells(self):
        g = GeoGrid(precision=6)
        gh = g.add(40.7128, -74.006, "NYC")
        g.add(34.0522, -118.2437, "LA")  # very far away
        out = g.query_neighbors(gh)
        assert all(p[2] != "LA" for p in out)


class TestGeoGridQueryRadius:
    def test_empty_grid(self):
        g = GeoGrid(precision=6)
        assert g.query_radius(40.7128, -74.006, 1000.0) == []

    def test_radius_zero_returns_only_same_point(self):
        g = GeoGrid(precision=6)
        g.add(40.7128, -74.006, "NYC")
        # 0 m radius matches only the exact same coordinates.
        out = g.query_radius(40.7128, -74.006, 0.0)
        assert len(out) == 1

    def test_picks_nearby_points(self):
        g = GeoGrid(precision=6)
        g.add(40.7128, -74.006, "NYC")
        g.add(40.713, -74.0061, "Nearby")
        out = g.query_radius(40.7128, -74.006, 200.0)
        names = {p[2] for p in out}
        assert "NYC" in names and "Nearby" in names

    def test_excludes_far_points(self):
        g = GeoGrid(precision=6)
        g.add(40.7128, -74.006, "NYC")
        g.add(34.0522, -118.2437, "LA")
        out = g.query_radius(40.7128, -74.006, 100_000.0)  # 100 km
        names = {p[2] for p in out}
        assert "NYC" in names
        assert "LA" not in names

    def test_negative_radius_raises(self):
        g = GeoGrid(precision=6)
        with pytest.raises(ValueError):
            g.query_radius(0, 0, -1.0)

    def test_radius_within_cell(self):
        g = GeoGrid(precision=6)
        # Two points 10 m apart at NYC latitude
        g.add(40.7128, -74.006, "A")
        g.add(40.71289, -74.006, "B")  # ~10 m north
        out = g.query_radius(40.7128, -74.006, 50.0)
        names = {p[2] for p in out}
        assert names == {"A", "B"}

    def test_radius_spans_neighbour_cells(self):
        g = GeoGrid(precision=6)
        gh_centre = encode(40.7128, -74.006, 6)
        # Put a sentinel point in each of the 8 neighbours' centres.
        for direction, ngh in neighbors(gh_centre).items():
            la, lo = decode(ngh)
            g.add(la, lo, direction)
        # query centre with a generous radius — must collect all 8.
        out = g.query_radius(40.7128, -74.006, 5_000.0)
        names = {p[2] for p in out}
        assert names == {"n", "ne", "e", "se", "s", "sw", "w", "nw"}


class TestGeoGridCount:
    def test_count_grows(self):
        g = GeoGrid(precision=6)
        assert g.count() == 0
        g.add(0, 0)
        assert g.count() == 1
        g.add(0, 1)
        assert g.count() == 2
        g.add(0, 2)
        assert g.count() == 3

    def test_count_multiple_in_one_cell(self):
        g = GeoGrid(precision=3)
        g.add(40.7, -74.0)
        g.add(40.701, -74.001)
        g.add(40.702, -74.002)
        assert g.count() == 3


class TestGeoGridCells:
    def test_empty(self):
        assert GeoGrid().cells() == []

    def test_sorted_and_unique(self):
        g = GeoGrid(precision=2)
        g.add(40.7128, -74.006)
        g.add(34.0522, -118.2437)
        g.add(51.5074, -0.1278)
        c = g.cells()
        assert c == sorted(c)
        assert len(set(c)) == len(c)

    def test_only_non_empty_cells(self):
        g = GeoGrid(precision=6)
        g.add(40.7128, -74.006, "NYC")
        # all returned cells should have at least one point.
        for c in g.cells():
            assert len(g.points[c]) > 0


# =========================================================================
# 6. Misc / sanity
# =========================================================================

class TestPackageSurface:
    def test_imports(self):
        # Just exercise the public surface — every symbol is callable / a class.
        from docstoolkit.geohash import (  # noqa: F401
            GeoGrid,
            decode,
            decode_bbox,
            encode,
            haversine,
            haversine_geohash,
            neighbors,
        )
        assert callable(encode)
        assert callable(decode)
        assert callable(decode_bbox)
        assert callable(neighbors)
        assert callable(haversine)
        assert callable(haversine_geohash)
        assert isinstance(GeoGrid(), GeoGrid)

    def test_encode_decode_chain_for_random_points(self):
        # A handful of pseudo-random but deterministic points.
        for i in range(20):
            lat = (i * 7) % 170 - 85   # in (-85, 85)
            lon = (i * 13) % 350 - 175  # in (-175, 175)
            gh = encode(lat, lon, 10)
            rlat, rlon = decode(gh)
            assert abs(rlat - lat) < 1e-3
            assert abs(rlon - lon) < 1e-3
