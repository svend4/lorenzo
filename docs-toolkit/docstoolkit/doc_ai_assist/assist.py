"""AI-assisted document operations with pluggable provider.

This module provides a small, dependency-free facade for AI-assisted text
operations such as summarising, rewriting, explaining, translating and so on.
Actual LLM integration is intentionally out of scope — the module ships with a
deterministic :class:`StubProvider` suitable for tests and offline use, and
accepts any callable conforming to :class:`AssistProvider`.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional, Protocol


class AssistAction(str, Enum):
    """Enumeration of supported assist actions."""

    SUMMARIZE = "summarize"
    REWRITE = "rewrite"
    EXPLAIN = "explain"
    TRANSLATE = "translate"
    EXPAND = "expand"
    SHORTEN = "shorten"
    FORMALIZE = "formalize"
    SIMPLIFY = "simplify"


@dataclass
class AssistRequest:
    """Request to perform an :class:`AssistAction` on ``text``."""

    text: str
    action: AssistAction
    params: dict = field(default_factory=dict)


@dataclass
class AssistResult:
    """Result of an assist operation."""

    input: str
    output: str
    action: AssistAction
    tokens_used: int = 0
    latency_ms: float = 0.0
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """Return True when no error was reported."""
        return self.error is None


class AssistProvider(Protocol):
    """Callable protocol for assist providers."""

    def __call__(self, request: AssistRequest) -> AssistResult:  # pragma: no cover - protocol
        ...


# ---------------------------------------------------------------------------
# Stub provider — deterministic implementations for tests
# ---------------------------------------------------------------------------


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _first_sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    parts = _SENTENCE_SPLIT_RE.split(text, maxsplit=1)
    return parts[0].strip()


def _reverse_words(text: str) -> str:
    return " ".join(reversed(text.split()))


def _formalize(text: str) -> str:
    replacements = {
        "don't": "do not",
        "won't": "will not",
        "can't": "cannot",
        "it's": "it is",
        "I'm": "I am",
        "you're": "you are",
        "they're": "they are",
        "we're": "we are",
        "isn't": "is not",
        "aren't": "are not",
        "doesn't": "does not",
        "didn't": "did not",
        "haven't": "have not",
        "hasn't": "has not",
        "shouldn't": "should not",
        "wouldn't": "would not",
        "couldn't": "could not",
    }
    out = text
    for src, dst in replacements.items():
        out = out.replace(src, dst)
        out = out.replace(src.capitalize(), dst.capitalize())
    return out


def _simplify(text: str) -> str:
    """Replace the three longest 3+-letter words with placeholders.

    The replacement is deterministic: among words of length >= 3, pick the
    three longest (ties broken by first occurrence) and replace each
    occurrence with ``<word>``.
    """
    word_re = re.compile(r"\b[A-Za-zА-Яа-яЁё]+\b")
    seen: List[str] = []
    for match in word_re.finditer(text):
        word = match.group(0)
        if len(word) >= 3 and word not in seen:
            seen.append(word)
    # Sort by length desc, then by first-occurrence index (stable)
    seen_sorted = sorted(seen, key=lambda w: -len(w))
    targets = seen_sorted[:3]
    out = text
    for word in targets:
        out = re.sub(r"\b" + re.escape(word) + r"\b", "<word>", out)
    return out


class StubProvider:
    """Deterministic test provider implementing :class:`AssistProvider`.

    Behaviour per action:

    * ``SUMMARIZE`` — first sentence of the input.
    * ``REWRITE``   — input with word order reversed.
    * ``EXPLAIN``   — prefixed with ``"EXPLAIN: "``.
    * ``TRANSLATE`` — uppercase form of the input.
    * ``EXPAND``    — input duplicated (or by ``factor`` from params).
    * ``SHORTEN``   — first ``max_chars`` characters (default 200).
    * ``FORMALIZE`` — common contractions expanded (``don't`` → ``do not``).
    * ``SIMPLIFY``  — three longest words replaced with ``<word>``.

    ``tokens_used`` is always ``len(input.split())``.
    """

    def __call__(self, request: AssistRequest) -> AssistResult:
        start = time.perf_counter()
        text = request.text
        action = request.action
        params = request.params or {}
        error: Optional[str] = None
        output = ""
        try:
            if action is AssistAction.SUMMARIZE:
                output = _first_sentence(text)
            elif action is AssistAction.REWRITE:
                output = _reverse_words(text)
            elif action is AssistAction.EXPLAIN:
                output = "EXPLAIN: " + text
            elif action is AssistAction.TRANSLATE:
                output = text.upper()
            elif action is AssistAction.EXPAND:
                factor = params.get("factor", 2.0)
                try:
                    factor = float(factor)
                except (TypeError, ValueError):
                    factor = 2.0
                # Doubled by default; for arbitrary factors, repeat int(factor) times
                # and append a fractional remainder.
                whole = int(factor)
                if whole < 1:
                    whole = 1
                output = (text + " ") * (whole - 1) + text
            elif action is AssistAction.SHORTEN:
                max_chars = params.get("max_chars", 200)
                try:
                    max_chars = int(max_chars)
                except (TypeError, ValueError):
                    max_chars = 200
                if max_chars < 0:
                    max_chars = 0
                output = text[:max_chars]
            elif action is AssistAction.FORMALIZE:
                output = _formalize(text)
            elif action is AssistAction.SIMPLIFY:
                output = _simplify(text)
            else:  # pragma: no cover - exhaustive enum
                error = f"unsupported action: {action!r}"
        except Exception as exc:  # pragma: no cover - defensive
            error = str(exc)
            output = ""

        latency_ms = (time.perf_counter() - start) * 1000.0
        tokens_used = len(text.split())
        return AssistResult(
            input=text,
            output=output,
            action=action,
            tokens_used=tokens_used,
            latency_ms=latency_ms,
            error=error,
        )


# ---------------------------------------------------------------------------
# Facade
# ---------------------------------------------------------------------------


class DocAiAssist:
    """Facade for AI-assisted document operations.

    Parameters
    ----------
    provider:
        Any callable matching :class:`AssistProvider`. When omitted, a
        :class:`StubProvider` is used.
    """

    def __init__(self, provider: Optional[Callable[[AssistRequest], AssistResult]] = None) -> None:
        self.provider: Callable[[AssistRequest], AssistResult] = provider or StubProvider()
        self._calls: int = 0
        self._tokens: int = 0

    # -- convenience action methods ----------------------------------------
    def summarize(self, text: str, max_words: int = 100) -> AssistResult:
        return self.process(
            AssistRequest(text=text, action=AssistAction.SUMMARIZE, params={"max_words": max_words})
        )

    def rewrite(self, text: str, style: str = "neutral") -> AssistResult:
        return self.process(
            AssistRequest(text=text, action=AssistAction.REWRITE, params={"style": style})
        )

    def explain(self, text: str) -> AssistResult:
        return self.process(AssistRequest(text=text, action=AssistAction.EXPLAIN))

    def translate(self, text: str, target_language: str = "en") -> AssistResult:
        return self.process(
            AssistRequest(
                text=text,
                action=AssistAction.TRANSLATE,
                params={"target_language": target_language},
            )
        )

    def expand(self, text: str, factor: float = 2.0) -> AssistResult:
        return self.process(
            AssistRequest(text=text, action=AssistAction.EXPAND, params={"factor": factor})
        )

    def shorten(self, text: str, max_chars: int = 200) -> AssistResult:
        return self.process(
            AssistRequest(text=text, action=AssistAction.SHORTEN, params={"max_chars": max_chars})
        )

    def formalize(self, text: str) -> AssistResult:
        return self.process(AssistRequest(text=text, action=AssistAction.FORMALIZE))

    def simplify(self, text: str) -> AssistResult:
        return self.process(AssistRequest(text=text, action=AssistAction.SIMPLIFY))

    # -- core --------------------------------------------------------------
    def process(self, request: AssistRequest) -> AssistResult:
        """Send ``request`` to the underlying provider and track metrics."""
        result = self.provider(request)
        self._calls += 1
        if result and result.tokens_used:
            self._tokens += int(result.tokens_used)
        return result

    def batch(self, requests: List[AssistRequest]) -> List[AssistResult]:
        """Process a list of requests, returning a parallel list of results."""
        return [self.process(req) for req in requests]

    # -- metrics -----------------------------------------------------------
    @property
    def total_calls(self) -> int:
        return self._calls

    @property
    def total_tokens(self) -> int:
        return self._tokens
