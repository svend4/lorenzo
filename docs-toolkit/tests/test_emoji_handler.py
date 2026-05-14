"""Tests for docstoolkit.emoji_handler."""
from __future__ import annotations

import pytest

from docstoolkit.emoji_handler import (
    EmojiCategory,
    EmojiHandler,
    EmojiInfo,
    EmojiStats,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def handler() -> EmojiHandler:
    return EmojiHandler()


# ---------------------------------------------------------------------------
# EmojiCategory
# ---------------------------------------------------------------------------
class TestEmojiCategory:
    def test_has_all_expected_members(self):
        names = {c.name for c in EmojiCategory}
        assert names == {
            "SMILEY", "ANIMAL", "FOOD", "OBJECT",
            "SYMBOL", "FLAG", "ARROW", "OTHER",
        }

    def test_values_are_strings(self):
        for c in EmojiCategory:
            assert isinstance(c.value, str)

    def test_distinct_values(self):
        values = [c.value for c in EmojiCategory]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# EmojiInfo
# ---------------------------------------------------------------------------
class TestEmojiInfo:
    def test_construction(self):
        info = EmojiInfo(char="😀", codepoint=0x1F600,
                         category=EmojiCategory.SMILEY, position=3)
        assert info.char == "😀"
        assert info.codepoint == 0x1F600
        assert info.category == EmojiCategory.SMILEY
        assert info.position == 3

    def test_equality(self):
        a = EmojiInfo(char="😀", codepoint=0x1F600,
                      category=EmojiCategory.SMILEY, position=0)
        b = EmojiInfo(char="😀", codepoint=0x1F600,
                      category=EmojiCategory.SMILEY, position=0)
        assert a == b


# ---------------------------------------------------------------------------
# EmojiStats
# ---------------------------------------------------------------------------
class TestEmojiStats:
    def test_default_construction(self):
        s = EmojiStats()
        assert s.total == 0
        assert s.unique == 0
        assert s.by_category == {}
        assert s.most_common == []

    def test_most_common_ordering(self, handler):
        text = "😀😀😀🐶🐶🍕"
        stats = handler.stats(text)
        # most_common returns highest count first
        assert stats.most_common[0] == ("😀", 3)
        assert stats.most_common[1] == ("🐶", 2)
        assert stats.most_common[2] == ("🍕", 1)

    def test_most_common_caps_at_ten(self, handler):
        # eleven unique smileys
        chars = "".join(chr(0x1F600 + i) for i in range(11))
        stats = handler.stats(chars)
        assert len(stats.most_common) == 10


# ---------------------------------------------------------------------------
# find_all
# ---------------------------------------------------------------------------
class TestFindAll:
    def test_finds_single_smiley(self, handler):
        infos = handler.find_all("hello 😀")
        assert len(infos) == 1
        assert infos[0].char == "😀"
        assert infos[0].codepoint == 0x1F600
        assert infos[0].category == EmojiCategory.SMILEY
        assert infos[0].position == 6

    def test_finds_multiple_smileys(self, handler):
        infos = handler.find_all("😀😃😄")
        assert [i.char for i in infos] == ["😀", "😃", "😄"]
        assert [i.position for i in infos] == [0, 1, 2]

    def test_mixed_text(self, handler):
        infos = handler.find_all("a😀b🐶c🍕d")
        assert [i.char for i in infos] == ["😀", "🐶", "🍕"]
        assert [i.position for i in infos] == [1, 3, 5]

    def test_no_emojis(self, handler):
        assert handler.find_all("plain text only") == []

    def test_empty_string(self, handler):
        assert handler.find_all("") == []

    def test_flag_sequence(self, handler):
        infos = handler.find_all("🇺🇸")
        assert len(infos) == 1
        assert infos[0].char == "🇺🇸"
        assert infos[0].category == EmojiCategory.FLAG

    def test_vs16_attached(self, handler):
        # arrow + variation selector → single emoji
        infos = handler.find_all("➡️")
        assert len(infos) == 1
        assert "➡" in infos[0].char


# ---------------------------------------------------------------------------
# count
# ---------------------------------------------------------------------------
class TestCount:
    def test_count_zero(self, handler):
        assert handler.count("no emoji here") == 0

    def test_count_one(self, handler):
        assert handler.count("hi 😀") == 1

    def test_count_many(self, handler):
        assert handler.count("😀😃😄🐶🍕") == 5

    def test_count_empty(self, handler):
        assert handler.count("") == 0


# ---------------------------------------------------------------------------
# extract
# ---------------------------------------------------------------------------
class TestExtract:
    def test_preserves_duplicates(self, handler):
        assert handler.extract("😀x😀y😀") == ["😀", "😀", "😀"]

    def test_order_preserved(self, handler):
        assert handler.extract("🐶🍕😀") == ["🐶", "🍕", "😀"]

    def test_empty(self, handler):
        assert handler.extract("plain") == []


# ---------------------------------------------------------------------------
# unique
# ---------------------------------------------------------------------------
class TestUnique:
    def test_unique_set(self, handler):
        assert handler.unique("😀😀🐶") == {"😀", "🐶"}

    def test_returns_set(self, handler):
        assert isinstance(handler.unique("😀"), set)

    def test_empty(self, handler):
        assert handler.unique("nothing") == set()


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_basic_totals(self, handler):
        s = handler.stats("😀😀🐶🍕🚀")
        assert s.total == 5
        assert s.unique == 4

    def test_by_category(self, handler):
        s = handler.stats("😀🐶🍕🚀")
        assert s.by_category["smiley"] == 1
        assert s.by_category["animal"] == 1
        assert s.by_category["food"] == 1
        # 🚀 is in 0x1F680-0x1F6FF, transport → OBJECT
        assert s.by_category["object"] == 1

    def test_empty_stats(self, handler):
        s = handler.stats("")
        assert s.total == 0
        assert s.unique == 0
        assert s.by_category == {}
        assert s.most_common == []

    def test_no_emoji_text(self, handler):
        s = handler.stats("just words and 123")
        assert s.total == 0
        assert s.unique == 0


# ---------------------------------------------------------------------------
# strip
# ---------------------------------------------------------------------------
class TestStrip:
    def test_removes_all(self, handler):
        assert handler.strip("hi 😀 there 🐶!") == "hi  there !"

    def test_no_change_when_no_emojis(self, handler):
        assert handler.strip("plain") == "plain"

    def test_strip_only_emojis(self, handler):
        assert handler.strip("😀🐶🍕") == ""

    def test_strip_empty(self, handler):
        assert handler.strip("") == ""

    def test_preserves_unicode_text(self, handler):
        assert handler.strip("Привет 😀 мир") == "Привет  мир"


# ---------------------------------------------------------------------------
# replace
# ---------------------------------------------------------------------------
class TestReplace:
    def test_replace_default_is_strip(self, handler):
        assert handler.replace("a😀b") == "ab"

    def test_replace_custom(self, handler):
        assert handler.replace("a😀b", "[E]") == "a[E]b"

    def test_replace_many(self, handler):
        assert handler.replace("😀😀😀", "X") == "XXX"

    def test_replace_no_match(self, handler):
        assert handler.replace("nothing", "X") == "nothing"

    def test_replace_empty_text(self, handler):
        assert handler.replace("", "X") == ""


# ---------------------------------------------------------------------------
# contains
# ---------------------------------------------------------------------------
class TestContains:
    def test_contains_true(self, handler):
        assert handler.contains("hello 😀")

    def test_contains_false(self, handler):
        assert not handler.contains("hello world")

    def test_contains_empty(self, handler):
        assert not handler.contains("")

    def test_contains_flag(self, handler):
        assert handler.contains("🇺🇸")


# ---------------------------------------------------------------------------
# categorize
# ---------------------------------------------------------------------------
class TestCategorize:
    def test_smiley(self, handler):
        assert handler.categorize("😀") == EmojiCategory.SMILEY

    def test_supplemental_smiley(self, handler):
        # 0x1F970 (smiling face with hearts) is in 0x1F900-0x1F9FF
        assert handler.categorize("\U0001F970") == EmojiCategory.SMILEY

    def test_animal(self, handler):
        assert handler.categorize("🐶") == EmojiCategory.ANIMAL

    def test_food(self, handler):
        assert handler.categorize("🍕") == EmojiCategory.FOOD

    def test_flag_component(self, handler):
        # single regional indicator is still classified FLAG
        assert handler.categorize("\U0001F1FA") == EmojiCategory.FLAG

    def test_arrow(self, handler):
        assert handler.categorize("←") == EmojiCategory.ARROW

    def test_symbol_dingbat(self, handler):
        # ✂ U+2702 is in dingbats range
        assert handler.categorize("✂") == EmojiCategory.SYMBOL

    def test_symbol_misc(self, handler):
        # ⚡ U+26A1 is in misc symbols
        assert handler.categorize("⚡") == EmojiCategory.SYMBOL

    def test_object_transport(self, handler):
        # 🚀 U+1F680 is in transport range → OBJECT
        assert handler.categorize("🚀") == EmojiCategory.OBJECT

    def test_other_for_non_emoji(self, handler):
        assert handler.categorize("a") == EmojiCategory.OTHER

    def test_empty_string_other(self, handler):
        assert handler.categorize("") == EmojiCategory.OTHER


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_only_emojis(self, handler):
        text = "😀🐶🍕🚀"
        assert handler.count(text) == 4
        assert handler.strip(text) == ""

    def test_mixed_unicode(self, handler):
        text = "Hello мир 你好 😀"
        assert handler.count(text) == 1
        assert handler.strip(text) == "Hello мир 你好 "

    def test_emoji_at_boundaries(self, handler):
        text = "😀hello😀"
        infos = handler.find_all(text)
        assert len(infos) == 2
        assert infos[0].position == 0
        # one BMP-pair char (len 2 in Python? no, str is unicode-aware)
        # 😀 is a single code point above BMP — in Python 3 len("😀")==1
        assert infos[1].position == 6

    def test_handles_newlines_and_punctuation(self, handler):
        text = "line1 😀\nline2 🐶! end."
        assert handler.count(text) == 2

    def test_long_text(self, handler):
        text = ("hello " * 100) + "😀" + (" world" * 100)
        assert handler.count(text) == 1
        assert handler.contains(text)

    def test_replace_preserves_surrounding(self, handler):
        text = "start 😀 middle 🐶 end"
        assert handler.replace(text, "*") == "start * middle * end"

    def test_stats_unique_smaller_or_equal_total(self, handler):
        text = "😀😀😀🐶🐶🍕🍕🚀"
        s = handler.stats(text)
        assert s.unique <= s.total
        assert s.unique == 4
        assert s.total == 8

    def test_find_all_returns_emoji_info_instances(self, handler):
        infos = handler.find_all("😀")
        assert all(isinstance(i, EmojiInfo) for i in infos)
