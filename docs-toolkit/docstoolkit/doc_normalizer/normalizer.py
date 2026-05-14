"""Document normalizer — configurable pipeline of normalization steps with presets."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class NormalizerStep(Enum):
    """Individual normalizer steps that can be combined into a pipeline."""

    LOWERCASE = "LOWERCASE"
    STRIP = "STRIP"
    COLLAPSE_WS = "COLLAPSE_WS"
    EXPAND_CONTRACTIONS = "EXPAND_CONTRACTIONS"
    REMOVE_PUNCTUATION = "REMOVE_PUNCTUATION"
    REMOVE_DIGITS = "REMOVE_DIGITS"
    FIX_UNICODE = "FIX_UNICODE"
    NORMALIZE_QUOTES = "NORMALIZE_QUOTES"
    REMOVE_DIACRITICS = "REMOVE_DIACRITICS"
    EXPAND_ABBREVIATIONS = "EXPAND_ABBREVIATIONS"


class Preset(Enum):
    """Named presets that bundle commonly-used step sequences."""

    MINIMAL = "MINIMAL"
    STANDARD = "STANDARD"
    AGGRESSIVE = "AGGRESSIVE"
    SEARCH = "SEARCH"


@dataclass
class NormalizeConfig:
    """Configuration for a document normalization pipeline."""

    steps: list[NormalizerStep] = field(default_factory=list)
    preserve_newlines: bool = True
    custom_replacements: list[tuple[str, str]] = field(default_factory=list)
    custom_contractions: dict[str, str] = field(default_factory=dict)
    custom_abbreviations: dict[str, str] = field(default_factory=dict)


@dataclass
class NormalizeResult:
    """Result of applying a normalization pipeline to a text."""

    original: str
    normalized: str
    applied_steps: list[NormalizerStep] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        """True when the normalized text differs from the original."""
        return self.original != self.normalized

    @property
    def length_delta(self) -> int:
        """Signed character-length difference (normalized - original)."""
        return len(self.normalized) - len(self.original)


# --- built-in data tables ---------------------------------------------------

_SMART_QUOTES = {
    "“": '"',  # LEFT DOUBLE QUOTATION MARK
    "”": '"',  # RIGHT DOUBLE QUOTATION MARK
    "„": '"',  # DOUBLE LOW-9 QUOTATION MARK
    "‟": '"',  # DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    "«": '"',  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    "»": '"',  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    "‘": "'",  # LEFT SINGLE QUOTATION MARK
    "’": "'",  # RIGHT SINGLE QUOTATION MARK
    "‚": "'",  # SINGLE LOW-9 QUOTATION MARK
    "‛": "'",  # SINGLE HIGH-REVERSED-9 QUOTATION MARK
}

_QUOTE_TRANSLATE = str.maketrans(_SMART_QUOTES)

_DEFAULT_CONTRACTIONS: dict[str, str] = {
    "don't": "do not",
    "won't": "will not",
    "can't": "can not",
    "i'm": "i am",
    "it's": "it is",
    "you're": "you are",
    "they're": "they are",
    "we're": "we are",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "doesn't": "does not",
    "didn't": "did not",
    "shouldn't": "should not",
    "wouldn't": "would not",
    "couldn't": "could not",
    "i've": "i have",
    "you've": "you have",
    "we've": "we have",
    "they've": "they have",
    "i'll": "i will",
    "you'll": "you will",
    "he'll": "he will",
    "she'll": "she will",
    "we'll": "we will",
    "they'll": "they will",
    "i'd": "i would",
    "you'd": "you would",
    "he'd": "he would",
    "she'd": "she would",
    "we'd": "we would",
    "they'd": "they would",
    "let's": "let us",
    "that's": "that is",
    "what's": "what is",
    "there's": "there is",
    "here's": "here is",
    "who's": "who is",
    "he's": "he is",
    "she's": "she is",
}

_DEFAULT_ABBREVIATIONS: dict[str, str] = {
    "Mr.": "Mister",
    "Mrs.": "Missus",
    "Ms.": "Miss",
    "Dr.": "Doctor",
    "St.": "Saint",
    "Prof.": "Professor",
    "Jr.": "Junior",
    "Sr.": "Senior",
    "e.g.": "for example",
    "i.e.": "that is",
    "etc.": "et cetera",
    "vs.": "versus",
}


# --- regexes ---------------------------------------------------------------

_RE_INLINE_WS = re.compile(r"[ \t\f\v\r\xa0]+")
_RE_ANY_WS = re.compile(r"\s+")
_RE_MULTI_NEWLINE = re.compile(r"\n+")
_RE_AROUND_NEWLINE = re.compile(r"[ \t]*\n[ \t]*")
_RE_DIGITS = re.compile(r"\d+")
# Punctuation: ASCII punctuation set.
_PUNCTUATION_CHARS = r"""!"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~"""
_RE_PUNCTUATION = re.compile(f"[{_PUNCTUATION_CHARS}]")


# --- presets ---------------------------------------------------------------

_PRESET_STEPS: dict[Preset, list[NormalizerStep]] = {
    Preset.MINIMAL: [
        NormalizerStep.STRIP,
        NormalizerStep.COLLAPSE_WS,
    ],
    Preset.STANDARD: [
        NormalizerStep.STRIP,
        NormalizerStep.COLLAPSE_WS,
        NormalizerStep.FIX_UNICODE,
        NormalizerStep.NORMALIZE_QUOTES,
    ],
    Preset.AGGRESSIVE: [
        NormalizerStep.FIX_UNICODE,
        NormalizerStep.NORMALIZE_QUOTES,
        NormalizerStep.EXPAND_CONTRACTIONS,
        NormalizerStep.EXPAND_ABBREVIATIONS,
        NormalizerStep.LOWERCASE,
        NormalizerStep.REMOVE_DIACRITICS,
        NormalizerStep.REMOVE_PUNCTUATION,
        NormalizerStep.STRIP,
        NormalizerStep.COLLAPSE_WS,
    ],
    Preset.SEARCH: [
        NormalizerStep.LOWERCASE,
        NormalizerStep.STRIP,
        NormalizerStep.COLLAPSE_WS,
        NormalizerStep.REMOVE_PUNCTUATION,
        NormalizerStep.REMOVE_DIACRITICS,
    ],
}


class DocNormalizer:
    """Configurable pipeline of normalizers for document content."""

    def __init__(self, config: Optional[NormalizeConfig] = None) -> None:
        self.config = config or NormalizeConfig()

    # --- individual operations ---------------------------------------------

    def lowercase(self, text: str) -> str:
        """Return lowercased text."""
        return text.lower()

    def strip(self, text: str) -> str:
        """Trim whitespace and tighten whitespace around newlines."""
        # Strip overall, then collapse spaces around newlines.
        stripped = text.strip()
        return _RE_AROUND_NEWLINE.sub("\n", stripped)

    def collapse_whitespace(self, text: str, preserve_newlines: bool = True) -> str:
        """Collapse runs of whitespace into single spaces (or newlines)."""
        if preserve_newlines:
            collapsed = _RE_INLINE_WS.sub(" ", text)
            collapsed = _RE_MULTI_NEWLINE.sub("\n", collapsed)
            collapsed = _RE_AROUND_NEWLINE.sub("\n", collapsed)
            return collapsed
        return _RE_ANY_WS.sub(" ", text)

    def expand_contractions(self, text: str, extra: Optional[dict] = None) -> str:
        """Replace English contractions with their expanded forms."""
        table: dict[str, str] = dict(_DEFAULT_CONTRACTIONS)
        if extra:
            for k, v in extra.items():
                table[k.lower()] = v
        # Case-insensitive word-boundary replacement.
        for contraction, expansion in sorted(
            table.items(), key=lambda kv: -len(kv[0])
        ):
            pattern = re.compile(
                r"\b" + re.escape(contraction) + r"\b", flags=re.IGNORECASE
            )
            text = pattern.sub(expansion, text)
        return text

    def remove_punctuation(self, text: str) -> str:
        """Strip ASCII punctuation characters."""
        return _RE_PUNCTUATION.sub("", text)

    def remove_digits(self, text: str) -> str:
        """Strip digit characters."""
        return _RE_DIGITS.sub("", text)

    def fix_unicode(self, text: str) -> str:
        """Apply NFKC unicode normalization."""
        return unicodedata.normalize("NFKC", text)

    def normalize_quotes(self, text: str) -> str:
        """Replace smart quotes with ASCII equivalents."""
        return text.translate(_QUOTE_TRANSLATE)

    def remove_diacritics(self, text: str) -> str:
        """Remove combining diacritical marks (café -> cafe)."""
        decomposed = unicodedata.normalize("NFD", text)
        return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")

    def expand_abbreviations(self, text: str, extra: Optional[dict] = None) -> str:
        """Replace common abbreviations with their expanded forms."""
        table: dict[str, str] = dict(_DEFAULT_ABBREVIATIONS)
        if extra:
            table.update(extra)
        # Replace longest keys first to avoid partial overlaps.
        for abbr, expansion in sorted(table.items(), key=lambda kv: -len(kv[0])):
            text = text.replace(abbr, expansion)
        return text

    def apply_replacements(
        self, text: str, replacements: list[tuple[str, str]]
    ) -> str:
        """Apply ordered list of literal find/replace pairs."""
        for needle, replacement in replacements:
            text = text.replace(needle, replacement)
        return text

    # --- presets / step dispatch -------------------------------------------

    def apply_preset(self, preset: Preset) -> NormalizeConfig:
        """Return a config populated with the steps for a preset."""
        steps = list(_PRESET_STEPS.get(preset, []))
        return NormalizeConfig(steps=steps)

    def apply_step(self, text: str, step: NormalizerStep) -> str:
        """Apply a single normalizer step to text."""
        cfg = self.config
        if step == NormalizerStep.LOWERCASE:
            return self.lowercase(text)
        if step == NormalizerStep.STRIP:
            return self.strip(text)
        if step == NormalizerStep.COLLAPSE_WS:
            return self.collapse_whitespace(text, cfg.preserve_newlines)
        if step == NormalizerStep.EXPAND_CONTRACTIONS:
            return self.expand_contractions(text, cfg.custom_contractions or None)
        if step == NormalizerStep.REMOVE_PUNCTUATION:
            return self.remove_punctuation(text)
        if step == NormalizerStep.REMOVE_DIGITS:
            return self.remove_digits(text)
        if step == NormalizerStep.FIX_UNICODE:
            return self.fix_unicode(text)
        if step == NormalizerStep.NORMALIZE_QUOTES:
            return self.normalize_quotes(text)
        if step == NormalizerStep.REMOVE_DIACRITICS:
            return self.remove_diacritics(text)
        if step == NormalizerStep.EXPAND_ABBREVIATIONS:
            return self.expand_abbreviations(text, cfg.custom_abbreviations or None)
        raise ValueError(f"Unknown step: {step!r}")

    # --- pipeline ----------------------------------------------------------

    def normalize(
        self, text: str, config: Optional[NormalizeConfig] = None
    ) -> NormalizeResult:
        """Apply the configured pipeline to `text`."""
        cfg = config if config is not None else self.config
        # Temporarily swap config so per-step helpers see the right settings.
        prev_config = self.config
        self.config = cfg
        try:
            original = text
            current = text
            applied: list[NormalizerStep] = []

            for step in cfg.steps:
                new = self.apply_step(current, step)
                if new != current:
                    applied.append(step)
                    current = new

            if cfg.custom_replacements:
                new = self.apply_replacements(current, cfg.custom_replacements)
                current = new

            return NormalizeResult(
                original=original,
                normalized=current,
                applied_steps=applied,
            )
        finally:
            self.config = prev_config

    def normalize_batch(
        self, texts: list[str], config: Optional[NormalizeConfig] = None
    ) -> list[NormalizeResult]:
        """Apply the configured pipeline to a batch of texts."""
        return [self.normalize(t, config) for t in texts]
