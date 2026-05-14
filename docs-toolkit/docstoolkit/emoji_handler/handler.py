"""Emoji handler — detection, counting, classification, manipulation.

Uses only the Python stdlib. Emoji detection is based on Unicode codepoint
ranges (no external `emoji` library required).
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class EmojiCategory(Enum):
    """High-level emoji categories."""

    SMILEY = "smiley"
    ANIMAL = "animal"
    FOOD = "food"
    OBJECT = "object"
    SYMBOL = "symbol"
    FLAG = "flag"
    ARROW = "arrow"
    OTHER = "other"


@dataclass
class EmojiInfo:
    """Information about a single emoji occurrence in text."""

    char: str
    codepoint: int
    category: EmojiCategory
    position: int


@dataclass
class EmojiStats:
    """Aggregate statistics about emojis found in a text."""

    total: int = 0
    unique: int = 0
    by_category: dict[str, int] = field(default_factory=dict)
    most_common: list[tuple[str, int]] = field(default_factory=list)


# Codepoint ranges that we consider to be emoji characters.
# These are inclusive (low, high) tuples.
_EMOJI_RANGES: tuple[tuple[int, int], ...] = (
    (0x1F600, 0x1F64F),  # emoticons / smileys
    (0x1F300, 0x1F5FF),  # misc symbols and pictographs (objects, weather, etc.)
    (0x1F680, 0x1F6FF),  # transport and map symbols
    (0x1F900, 0x1F9FF),  # supplemental symbols and pictographs
    (0x1F1E6, 0x1F1FF),  # regional indicator symbols (flags)
    (0x2190, 0x21FF),    # arrows
    (0x2700, 0x27BF),    # dingbats
    (0x2600, 0x26FF),    # miscellaneous symbols
    (0x1FA70, 0x1FAFF),  # symbols & pictographs extended-A
    (0x1F400, 0x1F4FF),  # already covered by 1F300-1F5FF but listed for clarity
)

# Combining / modifier codepoints attached to a preceding emoji.
_MODIFIER_RANGES: tuple[tuple[int, int], ...] = (
    (0x1F3FB, 0x1F3FF),  # emoji skin tone modifiers
)

# Special non-spacing characters that extend an emoji sequence.
_ZWJ = 0x200D  # zero-width joiner
_VS16 = 0xFE0F  # variation selector-16 (emoji presentation)


def _in_ranges(cp: int, ranges: Iterable[tuple[int, int]]) -> bool:
    for low, high in ranges:
        if low <= cp <= high:
            return True
    return False


def _is_emoji_base(cp: int) -> bool:
    """Return True if codepoint is a standalone emoji 'base' character."""
    return _in_ranges(cp, _EMOJI_RANGES)


def _is_modifier(cp: int) -> bool:
    return _in_ranges(cp, _MODIFIER_RANGES)


def _categorize_codepoint(cp: int) -> EmojiCategory:
    """Map a base emoji codepoint to a high-level category."""
    # Flags first (regional indicators)
    if 0x1F1E6 <= cp <= 0x1F1FF:
        return EmojiCategory.FLAG
    # Smileys / emoticons
    if 0x1F600 <= cp <= 0x1F64F:
        return EmojiCategory.SMILEY
    # Supplemental — many smiley/people in here too
    if 0x1F900 <= cp <= 0x1F9FF:
        return EmojiCategory.SMILEY
    # Animals (mammals/birds/reptiles range)
    if 0x1F400 <= cp <= 0x1F43F:
        return EmojiCategory.ANIMAL
    # Food and drink range
    if 0x1F345 <= cp <= 0x1F37F:
        return EmojiCategory.FOOD
    # Arrows
    if 0x2190 <= cp <= 0x21FF:
        return EmojiCategory.ARROW
    # Dingbats — symbols
    if 0x2700 <= cp <= 0x27BF:
        return EmojiCategory.SYMBOL
    # Misc symbols
    if 0x2600 <= cp <= 0x26FF:
        return EmojiCategory.SYMBOL
    # Anything else that we still recognize as emoji falls back to OBJECT
    if _is_emoji_base(cp):
        return EmojiCategory.OBJECT
    return EmojiCategory.OTHER


class EmojiHandler:
    """Detect and manipulate emoji characters in text."""

    # ------------------------------------------------------------------ core
    def find_all(self, text: str) -> list[EmojiInfo]:
        """Find every emoji (including multi-codepoint sequences) in `text`.

        Sequences joined with ZWJ, followed by VS16, or with a skin-tone
        modifier are merged into a single EmojiInfo entry. The reported
        position is the character index of the first codepoint of the
        sequence in `text`.
        """
        results: list[EmojiInfo] = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            cp = ord(ch)
            if _is_emoji_base(cp):
                start = i
                seq_chars = [ch]
                first_cp = cp
                j = i + 1
                # Greedy extension: consume VS16, ZWJ-joined bases, modifiers,
                # and chained flag indicators (two regional indicators in a row
                # form one flag).
                while j < n:
                    nxt = text[j]
                    nxt_cp = ord(nxt)
                    if nxt_cp == _VS16:
                        seq_chars.append(nxt)
                        j += 1
                        continue
                    if _is_modifier(nxt_cp):
                        seq_chars.append(nxt)
                        j += 1
                        continue
                    if nxt_cp == _ZWJ and j + 1 < n and _is_emoji_base(ord(text[j + 1])):
                        seq_chars.append(nxt)
                        seq_chars.append(text[j + 1])
                        j += 2
                        continue
                    # Pair regional indicators into a single flag glyph.
                    if (
                        0x1F1E6 <= first_cp <= 0x1F1FF
                        and 0x1F1E6 <= nxt_cp <= 0x1F1FF
                        and len(seq_chars) == 1
                    ):
                        seq_chars.append(nxt)
                        j += 1
                        continue
                    break
                seq = "".join(seq_chars)
                results.append(
                    EmojiInfo(
                        char=seq,
                        codepoint=first_cp,
                        category=_categorize_codepoint(first_cp),
                        position=start,
                    )
                )
                i = j
            else:
                i += 1
        return results

    def count(self, text: str) -> int:
        """Return the total number of emoji occurrences in `text`."""
        return len(self.find_all(text))

    def extract(self, text: str) -> list[str]:
        """Return the emoji characters in `text` in order, with duplicates."""
        return [info.char for info in self.find_all(text)]

    def unique(self, text: str) -> set[str]:
        """Return the set of unique emoji characters in `text`."""
        return {info.char for info in self.find_all(text)}

    def stats(self, text: str) -> EmojiStats:
        """Compute aggregate emoji statistics for `text`."""
        infos = self.find_all(text)
        chars = [info.char for info in infos]
        counter = Counter(chars)
        by_category: dict[str, int] = {}
        for info in infos:
            key = info.category.value
            by_category[key] = by_category.get(key, 0) + 1
        return EmojiStats(
            total=len(infos),
            unique=len(counter),
            by_category=by_category,
            most_common=counter.most_common(10),
        )

    def strip(self, text: str) -> str:
        """Return `text` with all emoji characters removed."""
        return self.replace(text, "")

    def replace(self, text: str, replacement: str = "") -> str:
        """Replace every emoji occurrence in `text` with `replacement`."""
        infos = self.find_all(text)
        if not infos:
            return text
        out: list[str] = []
        last = 0
        for info in infos:
            out.append(text[last:info.position])
            out.append(replacement)
            last = info.position + len(info.char)
        out.append(text[last:])
        return "".join(out)

    def contains(self, text: str) -> bool:
        """Return True if `text` contains at least one emoji."""
        for ch in text:
            if _is_emoji_base(ord(ch)):
                return True
        return False

    def categorize(self, char: str) -> EmojiCategory:
        """Classify a single emoji character (or sequence) into a category."""
        if not char:
            return EmojiCategory.OTHER
        return _categorize_codepoint(ord(char[0]))
