"""Tests for docstoolkit.doc_hash (E149)."""
from __future__ import annotations

import hashlib

import pytest

from docstoolkit.doc_hash import DocHash, HashAlgo, HashResult, SimHashResult


@pytest.fixture
def dh() -> DocHash:
    return DocHash()


class TestHashAlgo:
    def test_members_present(self):
        assert HashAlgo.MD5.value == "md5"
        assert HashAlgo.SHA1.value == "sha1"
        assert HashAlgo.SHA256.value == "sha256"
        assert HashAlgo.SHA512.value == "sha512"
        assert HashAlgo.BLAKE2B.value == "blake2b"

    def test_is_enum(self):
        assert len(list(HashAlgo)) == 5


class TestHashResult:
    def test_fields(self):
        r = HashResult(algo=HashAlgo.SHA256, hex_digest="abc", byte_size=3)
        assert r.algo is HashAlgo.SHA256
        assert r.hex_digest == "abc"
        assert r.byte_size == 3

    def test_frozen(self):
        r = HashResult(algo=HashAlgo.MD5, hex_digest="x", byte_size=1)
        with pytest.raises(Exception):
            r.byte_size = 2  # type: ignore[misc]


class TestSimHashResult:
    def test_fields(self):
        s = SimHashResult(value=0, bin_string="0" * 64)
        assert s.value == 0
        assert len(s.bin_string) == 64

    def test_frozen(self):
        s = SimHashResult(value=1, bin_string="0" * 64)
        with pytest.raises(Exception):
            s.value = 2  # type: ignore[misc]


class TestHash:
    def test_sha256_matches_hashlib(self, dh: DocHash):
        text = "hello world"
        expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
        result = dh.hash(text, HashAlgo.SHA256)
        assert result.hex_digest == expected
        assert result.algo is HashAlgo.SHA256
        assert result.byte_size == len(text.encode("utf-8"))

    def test_md5_matches_hashlib(self, dh: DocHash):
        text = "abc"
        assert dh.hash(text, HashAlgo.MD5).hex_digest == hashlib.md5(b"abc").hexdigest()

    def test_sha1(self, dh: DocHash):
        assert dh.hash("abc", HashAlgo.SHA1).hex_digest == hashlib.sha1(b"abc").hexdigest()

    def test_sha512(self, dh: DocHash):
        assert dh.hash("abc", HashAlgo.SHA512).hex_digest == hashlib.sha512(b"abc").hexdigest()

    def test_blake2b(self, dh: DocHash):
        assert dh.hash("abc", HashAlgo.BLAKE2B).hex_digest == hashlib.blake2b(b"abc").hexdigest()

    def test_deterministic(self, dh: DocHash):
        assert dh.hash("foo").hex_digest == dh.hash("foo").hex_digest

    def test_different_inputs_differ(self, dh: DocHash):
        assert dh.hash("foo").hex_digest != dh.hash("bar").hex_digest

    def test_default_is_sha256(self, dh: DocHash):
        assert dh.hash("x").algo is HashAlgo.SHA256

    def test_byte_size_unicode(self, dh: DocHash):
        text = "ё"  # multi-byte
        r = dh.hash(text)
        assert r.byte_size == len(text.encode("utf-8"))
        assert r.byte_size == 2


class TestHashNormalized:
    def test_whitespace_equivalence(self, dh: DocHash):
        a = dh.hash_normalized("Hello   World")
        b = dh.hash_normalized("hello world")
        assert a.hex_digest == b.hex_digest

    def test_trailing_whitespace(self, dh: DocHash):
        a = dh.hash_normalized("  hello  ")
        b = dh.hash_normalized("hello")
        assert a.hex_digest == b.hex_digest

    def test_newlines_collapsed(self, dh: DocHash):
        a = dh.hash_normalized("hello\nworld")
        b = dh.hash_normalized("hello world")
        assert a.hex_digest == b.hex_digest

    def test_case_insensitive(self, dh: DocHash):
        a = dh.hash_normalized("HELLO")
        b = dh.hash_normalized("hello")
        assert a.hex_digest == b.hex_digest

    def test_different_text_differs(self, dh: DocHash):
        a = dh.hash_normalized("hello")
        b = dh.hash_normalized("world")
        assert a.hex_digest != b.hex_digest


class TestHashLines:
    def test_three_lines(self, dh: DocHash):
        results = dh.hash_lines("a\nb\nc")
        assert len(results) == 3
        assert results[0].hex_digest == hashlib.sha256(b"a").hexdigest()
        assert results[1].hex_digest == hashlib.sha256(b"b").hexdigest()
        assert results[2].hex_digest == hashlib.sha256(b"c").hexdigest()

    def test_empty_text(self, dh: DocHash):
        results = dh.hash_lines("")
        assert len(results) == 1
        assert results[0].hex_digest == hashlib.sha256(b"").hexdigest()

    def test_md5_algo(self, dh: DocHash):
        results = dh.hash_lines("x\ny", HashAlgo.MD5)
        assert all(r.algo is HashAlgo.MD5 for r in results)

    def test_trailing_newline_creates_empty_line(self, dh: DocHash):
        results = dh.hash_lines("a\n")
        assert len(results) == 2


class TestHashChunks:
    def test_chunks_of_size_two(self, dh: DocHash):
        results = dh.hash_chunks("abcd", chunk_size=2)
        assert len(results) == 2
        assert results[0].hex_digest == hashlib.sha256(b"ab").hexdigest()
        assert results[1].hex_digest == hashlib.sha256(b"cd").hexdigest()

    def test_byte_sizes_correct(self, dh: DocHash):
        results = dh.hash_chunks("abcde", chunk_size=2)
        assert len(results) == 3
        assert [r.byte_size for r in results] == [2, 2, 1]

    def test_empty_text_returns_single(self, dh: DocHash):
        results = dh.hash_chunks("", chunk_size=10)
        assert len(results) == 1
        assert results[0].byte_size == 0

    def test_invalid_chunk_size(self, dh: DocHash):
        with pytest.raises(ValueError):
            dh.hash_chunks("abc", chunk_size=0)
        with pytest.raises(ValueError):
            dh.hash_chunks("abc", chunk_size=-1)

    def test_chunk_larger_than_text(self, dh: DocHash):
        results = dh.hash_chunks("abc", chunk_size=1024)
        assert len(results) == 1
        assert results[0].hex_digest == hashlib.sha256(b"abc").hexdigest()


class TestCompare:
    def test_equal_texts(self, dh: DocHash):
        assert dh.compare("hello", "hello") is True

    def test_different_texts(self, dh: DocHash):
        assert dh.compare("hello", "world") is False

    def test_case_sensitive(self, dh: DocHash):
        assert dh.compare("Hello", "hello") is False

    def test_alternate_algo(self, dh: DocHash):
        assert dh.compare("a", "a", HashAlgo.MD5) is True


class TestCompareNormalized:
    def test_whitespace_equivalence(self, dh: DocHash):
        assert dh.compare_normalized("hello world", "  hello   world  ") is True

    def test_case_equivalence(self, dh: DocHash):
        assert dh.compare_normalized("Hello", "HELLO") is True

    def test_genuinely_different(self, dh: DocHash):
        assert dh.compare_normalized("hello", "world") is False


class TestSimHash:
    def test_returns_simhashresult(self, dh: DocHash):
        s = dh.simhash("hello world")
        assert isinstance(s, SimHashResult)
        assert 0 <= s.value < (1 << 64)
        assert len(s.bin_string) == 64
        assert set(s.bin_string).issubset({"0", "1"})

    def test_deterministic(self, dh: DocHash):
        a = dh.simhash("the quick brown fox")
        b = dh.simhash("the quick brown fox")
        assert a.value == b.value
        assert a.bin_string == b.bin_string

    def test_bin_string_matches_value(self, dh: DocHash):
        s = dh.simhash("some text here for hashing")
        assert int(s.bin_string, 2) == s.value

    def test_empty_text(self, dh: DocHash):
        s = dh.simhash("")
        assert s.value == 0
        assert s.bin_string == "0" * 64

    def test_whitespace_only_text(self, dh: DocHash):
        s = dh.simhash("   \n\t  ")
        assert s.value == 0

    def test_similar_texts_close(self, dh: DocHash):
        a = dh.simhash(
            "the quick brown fox jumps over the lazy dog in the morning sunshine"
        )
        b = dh.simhash(
            "the quick brown fox jumps over the lazy dog in the morning sunlight"
        )
        dist = DocHash().hamming_distance(a.value, b.value)
        assert dist < 20

    def test_different_texts_farther(self, dh: DocHash):
        a = dh.simhash(
            "the quick brown fox jumps over the lazy dog in the morning sunshine"
        )
        b = dh.simhash(
            "completely unrelated content about machine learning and artificial intelligence research"
        )
        dist = DocHash().hamming_distance(a.value, b.value)
        assert dist > 5

    def test_case_insensitive(self, dh: DocHash):
        a = dh.simhash("Hello World Hello World")
        b = dh.simhash("hello world hello world")
        assert a.value == b.value


class TestHammingDistance:
    def test_zero_distance(self, dh: DocHash):
        assert dh.hamming_distance(0, 0) == 0
        assert dh.hamming_distance(0xFFFF, 0xFFFF) == 0

    def test_single_bit_diff(self, dh: DocHash):
        assert dh.hamming_distance(0b0000, 0b0001) == 1
        assert dh.hamming_distance(0b1010, 0b1011) == 1

    def test_all_bits_diff_64(self, dh: DocHash):
        all_ones = (1 << 64) - 1
        assert dh.hamming_distance(0, all_ones) == 64

    def test_known_distances(self, dh: DocHash):
        assert dh.hamming_distance(0b1100, 0b0011) == 4
        assert dh.hamming_distance(0b1111, 0b0000) == 4


class TestNearDuplicate:
    def test_identical_texts(self, dh: DocHash):
        assert dh.near_duplicate("hello world", "hello world") is True

    def test_completely_different(self, dh: DocHash):
        assert (
            dh.near_duplicate(
                "machine learning and neural networks are transforming AI research",
                "the cat sat on the mat in the warm afternoon sun by the window",
                threshold=3,
            )
            is False
        )

    def test_threshold_strictly_less_than(self, dh: DocHash):
        # Two identical texts have distance 0; threshold=1 → 0 < 1 → True
        assert dh.near_duplicate("a b c", "a b c", threshold=1) is True
        # threshold=0 → 0 < 0 → False
        assert dh.near_duplicate("a b c", "a b c", threshold=0) is False

    def test_high_threshold(self, dh: DocHash):
        assert (
            dh.near_duplicate(
                "alpha beta gamma", "delta epsilon zeta", threshold=100
            )
            is True
        )


class TestMerkleRoot:
    def test_single_text(self, dh: DocHash):
        root = dh.merkle_root(["hello"])
        assert root == hashlib.sha256(b"hello").hexdigest()

    def test_deterministic(self, dh: DocHash):
        texts = ["a", "b", "c", "d"]
        assert dh.merkle_root(texts) == dh.merkle_root(texts)

    def test_different_inputs_differ(self, dh: DocHash):
        assert dh.merkle_root(["a", "b"]) != dh.merkle_root(["a", "c"])

    def test_order_matters(self, dh: DocHash):
        assert dh.merkle_root(["a", "b"]) != dh.merkle_root(["b", "a"])

    def test_odd_count_duplicates_last(self, dh: DocHash):
        # 3-leaf tree: c is duplicated, so root == merkle_root([a,b,c,c])
        root_3 = dh.merkle_root(["a", "b", "c"])
        root_4 = dh.merkle_root(["a", "b", "c", "c"])
        assert root_3 == root_4

    def test_empty_list(self, dh: DocHash):
        root = dh.merkle_root([])
        assert root == hashlib.sha256(b"").hexdigest()

    def test_alternate_algo(self, dh: DocHash):
        root = dh.merkle_root(["x"], HashAlgo.MD5)
        assert root == hashlib.md5(b"x").hexdigest()

    def test_two_text_structure(self, dh: DocHash):
        h1 = hashlib.sha256(b"a").hexdigest()
        h2 = hashlib.sha256(b"b").hexdigest()
        expected = hashlib.sha256((h1 + h2).encode("utf-8")).hexdigest()
        assert dh.merkle_root(["a", "b"]) == expected


class TestVerify:
    def test_correct_digest(self, dh: DocHash):
        text = "hello"
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert dh.verify(text, digest) is True

    def test_incorrect_digest(self, dh: DocHash):
        assert dh.verify("hello", "deadbeef") is False

    def test_case_insensitive_digest(self, dh: DocHash):
        text = "hello"
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert dh.verify(text, digest.upper()) is True

    def test_md5_verification(self, dh: DocHash):
        text = "abc"
        digest = hashlib.md5(text.encode("utf-8")).hexdigest()
        assert dh.verify(text, digest, HashAlgo.MD5) is True

    def test_mismatched_algo(self, dh: DocHash):
        text = "abc"
        md5_digest = hashlib.md5(text.encode("utf-8")).hexdigest()
        # Trying to verify with sha256 against an md5 digest → False
        assert dh.verify(text, md5_digest, HashAlgo.SHA256) is False


class TestEdgeCases:
    def test_empty_string_hash(self, dh: DocHash):
        r = dh.hash("")
        assert r.byte_size == 0
        assert r.hex_digest == hashlib.sha256(b"").hexdigest()

    def test_single_char(self, dh: DocHash):
        r = dh.hash("x")
        assert r.byte_size == 1
        assert r.hex_digest == hashlib.sha256(b"x").hexdigest()

    def test_very_long_text(self, dh: DocHash):
        text = "a" * 100_000
        r = dh.hash(text)
        assert r.byte_size == 100_000
        assert r.hex_digest == hashlib.sha256(text.encode("utf-8")).hexdigest()

    def test_unicode_normalized(self, dh: DocHash):
        # Lowercasing turns Ё → ё; whitespace collapse handles spaces
        a = dh.hash_normalized("Привет   МИР")
        b = dh.hash_normalized("привет мир")
        assert a.hex_digest == b.hex_digest

    def test_simhash_single_token(self, dh: DocHash):
        s = dh.simhash("hello")
        assert isinstance(s.value, int)
        assert 0 <= s.value < (1 << 64)

    def test_hash_chunks_long_text(self, dh: DocHash):
        text = "x" * 5000
        results = dh.hash_chunks(text, chunk_size=1024)
        assert len(results) == 5  # 4 of 1024 + 1 of 904
        assert results[-1].byte_size == 5000 - 4 * 1024

    def test_merkle_root_single_repeated(self, dh: DocHash):
        # [a, a] should differ from [a]
        assert dh.merkle_root(["a", "a"]) != dh.merkle_root(["a"])
