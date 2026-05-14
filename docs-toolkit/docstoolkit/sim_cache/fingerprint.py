"""Fingerprinting methods for semantic similarity: TOKEN_HASH, SIMHASH, MINHASH."""
import hashlib
import re
from dataclasses import dataclass
from enum import Enum


class FingerprintMethod(str, Enum):
    TOKEN_HASH = "token_hash"
    MINHASH = "minhash"
    SIMHASH = "simhash"


@dataclass
class Fingerprint:
    """A compact fingerprint of a text document."""
    method: FingerprintMethod
    value: int
    text_len: int

    def similarity(self, other: "Fingerprint") -> float:
        """Compute similarity between two fingerprints.

        - TOKEN_HASH: 1.0 if values are equal, 0.0 otherwise.
        - SIMHASH: Hamming similarity over 64 bits = 1 - hamming_bits/64.
        - MINHASH: uses same Hamming approach as SIMHASH for the packed int.
        """
        if self.method != other.method:
            raise ValueError(
                f"Cannot compare fingerprints of different methods: "
                f"{self.method!r} vs {other.method!r}"
            )
        if self.method == FingerprintMethod.TOKEN_HASH:
            return 1.0 if self.value == other.value else 0.0

        if self.method in (FingerprintMethod.SIMHASH, FingerprintMethod.MINHASH):
            xor = self.value ^ other.value
            hamming_bits = bin(xor).count("1")
            return 1.0 - hamming_bits / 64


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())


def _tokenize(text: str) -> list[str]:
    """Split normalized text into word tokens."""
    return re.findall(r"[a-zа-яёA-ZА-ЯЁ0-9]+", _normalize(text))


def _sha256_int(data: bytes) -> int:
    """Return SHA-256 digest of *data* as a Python int."""
    return int.from_bytes(hashlib.sha256(data).digest(), "big")


class FingerprintBuilder:
    """Factory for building Fingerprint objects from text."""

    # ------------------------------------------------------------------
    # Individual methods
    # ------------------------------------------------------------------

    @staticmethod
    def token_hash(text: str) -> Fingerprint:
        """SHA-256 of normalized text → first 8 bytes → int."""
        normalized = _normalize(text).encode("utf-8")
        digest = hashlib.sha256(normalized).digest()
        value = int.from_bytes(digest[:8], "big")
        return Fingerprint(
            method=FingerprintMethod.TOKEN_HASH,
            value=value,
            text_len=len(text),
        )

    @staticmethod
    def simhash(text: str, bits: int = 64) -> Fingerprint:
        """SimHash: weight each token's SHA-256 bits by +1/-1, take sign.

        The result is packed into a *bits*-wide integer (default 64).
        """
        tokens = _tokenize(text)
        # Accumulate weighted bit counts
        v = [0] * bits
        for token in tokens:
            h = _sha256_int(token.encode("utf-8"))
            for i in range(bits):
                bit = (h >> (255 - i)) & 1  # use the top *bits* bits of SHA-256
                v[i] += 1 if bit else -1

        # Convert sign vector to integer
        fingerprint_int = 0
        for i in range(bits):
            if v[i] > 0:
                fingerprint_int |= 1 << (bits - 1 - i)

        # Mask to *bits* width
        mask = (1 << bits) - 1
        return Fingerprint(
            method=FingerprintMethod.SIMHASH,
            value=fingerprint_int & mask,
            text_len=len(text),
        )

    @staticmethod
    def minhash(text: str, num_hashes: int = 16) -> Fingerprint:
        """MinHash: seed-based hash functions, take min per hash, XOR into int.

        Uses *num_hashes* independent hash functions.  Each hash function is
        simulated by seeding with a different prime and XOR-ing with the token
        hash.  The resulting *num_hashes* min-values are folded into a 64-bit
        integer via XOR with position-dependent shifts.
        """
        tokens = _tokenize(text)
        if not tokens:
            return Fingerprint(
                method=FingerprintMethod.MINHASH,
                value=0,
                text_len=len(text),
            )

        # Pre-compute per-token SHA-256 ints once
        token_hashes = [
            _sha256_int(token.encode("utf-8")) for token in set(tokens)
        ]

        # Primes used as seeds (one per hash function)
        _PRIMES = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
            127, 131,
        ]

        min_hashes: list[int] = []
        for i in range(num_hashes):
            seed = _PRIMES[i % len(_PRIMES)]
            min_val = min(
                (seed * th + seed) & ((1 << 64) - 1) for th in token_hashes
            )
            min_hashes.append(min_val)

        # Fold into 64-bit integer via XOR, spreading each min-hash value
        result = 0
        mask64 = (1 << 64) - 1
        for idx, mh in enumerate(min_hashes):
            # Rotate and XOR to mix bits across the 64-bit space
            shift = (idx * (64 // max(num_hashes, 1))) % 64
            rotated = ((mh << shift) | (mh >> (64 - shift))) & mask64
            result ^= rotated

        return Fingerprint(
            method=FingerprintMethod.MINHASH,
            value=result & mask64,
            text_len=len(text),
        )

    @staticmethod
    def build(
        text: str,
        method: FingerprintMethod = FingerprintMethod.SIMHASH,
    ) -> Fingerprint:
        """Build a fingerprint using the specified method."""
        if method == FingerprintMethod.TOKEN_HASH:
            return FingerprintBuilder.token_hash(text)
        if method == FingerprintMethod.SIMHASH:
            return FingerprintBuilder.simhash(text)
        if method == FingerprintMethod.MINHASH:
            return FingerprintBuilder.minhash(text)
        raise ValueError(f"Unknown fingerprint method: {method!r}")
