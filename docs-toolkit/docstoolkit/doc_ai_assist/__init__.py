"""E211 Document AI Assist — pluggable interface for AI-assisted document operations.

Public API
----------
:class:`AssistAction`   — enum of supported assist actions
:class:`AssistRequest`  — request dataclass for an assist operation
:class:`AssistResult`   — result dataclass with output and metrics
:class:`AssistProvider` — protocol for pluggable providers
:class:`StubProvider`   — deterministic stub provider for tests
:class:`DocAiAssist`    — main facade class
"""
from .assist import (
    AssistAction,
    AssistProvider,
    AssistRequest,
    AssistResult,
    DocAiAssist,
    StubProvider,
)

__all__ = [
    "AssistAction",
    "AssistProvider",
    "AssistRequest",
    "AssistResult",
    "DocAiAssist",
    "StubProvider",
]
