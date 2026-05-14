"""Content hashing utilities for documents (E149).

Provides:
- Standard cryptographic hashing (MD5, SHA1, SHA256, SHA512, BLAKE2B)
- Normalized hashing (whitespace + case insensitive)
- Line-by-line and chunk-by-chunk hashing
- SimHash for near-duplicate detection (64-bit)
- Merkle tree root for batch verification
- Hamming distance and digest verification
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import Enum


class HashAlgo(str, Enum):
    """Supported hash algorithms."""

    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"
    BLAKE2B = "blake2b"


@dataclass(frozen=True)
class HashResult:
    """Result of a hashing operation.

    Attributes:
        algo: Algorithm used.
        hex_digest: Hexadecimal digest string.
        byte_size: Input size in bytes (UTF-8 encoded).
    """

    algo: HashAlgo
    hex_digest: str
    byte_size: int


@dataclass(frozen=True)
class SimHashResult:
    """Result of a simhash operation.

    Attributes:
        value: 64-bit simhash fingerprint as integer.
        bin_string: 64-character binary representation.
    """

    value: int
    bin_string: str


def _new_hasher(algo: HashAlgo):
    """Construct a hashlib hasher for the given algorithm."""
    if algo is HashAlgo.MD5:
        return hashlib.md5()
    if algo is HashAlgo.SHA1:
        return hashlib.sha1()
    if algo is HashAlgo.SHA256:
        return hashlib.sha256()
    if algo is HashAlgo.SHA512:
        return hashlib.sha512()
    if algo is HashAlgo.BLAKE2B:
        return hashlib.blake2b()
    raise ValueError(f"Unsupported algorithm: {algo!r}")


class DocHash:
    """Document hashing utilities."""

    # ----- Basic hashing -----

    def hash(self, text: str, algo: HashAlgo = HashAlgo.SHA256) -> HashResult:
        """Compute a hash of the full text."""
        data = text.encode("utf-8")
        h = _new_hasher(algo)
        h.update(data)
        return HashResult(algo=algo, hex_digest=h.hexdigest(), byte_size=len(data))

    def hash_normalized(
        self, text: str, algo: HashAlgo = HashAlgo.SHA256
    ) -> HashResult:
        """Hash after stripping whitespace and lowercasing.

        Collapses all whitespace runs to a single space, strips, lowercases.
        """
        normalized = re.sub(r"\s+", " ", text).strip().lower()
        return self.hash(normalized, algo)

    def hash_lines(
        self, text: str, algo: HashAlgo = HashAlgo.SHA256
    ) -> list[HashResult]:
        """Hash each line of the text separately."""
        # splitlines preserves no trailing empty unless explicit; use split('\n') to keep all
        lines = text.split("\n")
        return [self.hash(line, algo) for line in lines]

    def hash_chunks(
        self,
        text: str,
        chunk_size: int = 1024,
        algo: HashAlgo = HashAlgo.SHA256,
    ) -> list[HashResult]:
        """Hash fixed-size byte chunks of the text."""
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        data = text.encode("utf-8")
        results: list[HashResult] = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            h = _new_hasher(algo)
            h.update(chunk)
            results.append(
                HashResult(algo=algo, hex_digest=h.hexdigest(), byte_size=len(chunk))
            )
        if not results:
            # Empty input — return a single hash of empty bytes
            h = _new_hasher(algo)
            results.append(HashResult(algo=algo, hex_digest=h.hexdigest(), byte_size=0))
        return results

    # ----- Comparison -----

    def compare(
        self, text_a: str, text_b: str, algo: HashAlgo = HashAlgo.SHA256
    ) -> bool:
        """True if both texts have the same hash."""
        return self.hash(text_a, algo).hex_digest == self.hash(text_b, algo).hex_digest

    def compare_normalized(self, text_a: str, text_b: str) -> bool:
        """True if both texts have the same normalized hash."""
        return (
            self.hash_normalized(text_a).hex_digest
            == self.hash_normalized(text_b).hex_digest
        )

    # ----- SimHash -----

    @staticmethod
    def _token_hash64(token: str) -> int:
        """Deterministic 64-bit hash for a token using MD5."""
        digest = hashlib.md5(token.encode("utf-8")).digest()
        # Take first 8 bytes → 64-bit integer
        return int.from_bytes(digest[:8], "big", signed=False)

    def simhash(self, text: str) -> SimHashResult:
        """Compute a 64-bit simhash fingerprint of the text."""
        tokens = re.findall(r"\w+", text.lower())
        if not tokens:
            return SimHashResult(value=0, bin_string="0" * 64)

        counters = [0] * 64
        for tok in tokens:
            h = self._token_hash64(tok)
            for i in range(64):
                if (h >> i) & 1:
                    counters[i] += 1
                else:
                    counters[i] -= 1

        value = 0
        for i in range(64):
            if counters[i] > 0:
                value |= 1 << i

        bin_string = format(value, "064b")
        return SimHashResult(value=value, bin_string=bin_string)

    def hamming_distance(self, hash1: int, hash2: int) -> int:
        """Number of differing bits between two 64-bit integers."""
        x = (hash1 ^ hash2) & ((1 << 64) - 1)
        # Python 3.10+ has int.bit_count
        try:
            return x.bit_count()
        except AttributeError:  # pragma: no cover
            return bin(x).count("1")

    def near_duplicate(
        self, text_a: str, text_b: str, threshold: int = 3
    ) -> bool:
        """True if the two texts' simhashes differ by fewer than `threshold` bits."""
        a = self.simhash(text_a).value
        b = self.simhash(text_b).value
        return self.hamming_distance(a, b) < threshold

    # ----- Merkle tree -----

    def merkle_root(
        self, texts: list[str], algo: HashAlgo = HashAlgo.SHA256
    ) -> str:
        """Compute the Merkle tree root hash of the given texts."""
        if not texts:
            # Conventionally, empty tree → hash of empty bytes
            return _new_hasher(algo).hexdigest()

        level = [self.hash(t, algo).hex_digest for t in texts]
        while len(level) > 1:
            if len(level) % 2 == 1:
                level.append(level[-1])  # duplicate last to make pairs
            next_level: list[str] = []
            for i in range(0, len(level), 2):
                combined = (level[i] + level[i + 1]).encode("utf-8")
                h = _new_hasher(algo)
                h.update(combined)
                next_level.append(h.hexdigest())
            level = next_level
        return level[0]

    # ----- Verification -----

    def verify(
        self, text: str, hex_digest: str, algo: HashAlgo = HashAlgo.SHA256
    ) -> bool:
        """True if `text` hashes to the given `hex_digest`."""
        return self.hash(text, algo).hex_digest.lower() == hex_digest.lower()
