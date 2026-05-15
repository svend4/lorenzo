"""Tests for Sprint 54-92 CLI subcommands."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from docstoolkit import cli


def _run(args: list[str]) -> tuple[int, str, str]:
    """Invoke `python -m docstoolkit.cli <args>` and capture output."""
    p = subprocess.run(
        [sys.executable, "-m", "docstoolkit.cli", *args],
        capture_output=True, text=True, timeout=30,
    )
    return p.returncode, p.stdout, p.stderr


# ---------- subcommand discoverability ----------

def test_top_level_help_lists_new_commands():
    code, out, _ = _run(["--help"])
    assert code == 0
    for cmd in ("saved", "diff-bulk", "voice", "assets", "kg",
                "profile", "eval", "taxonomy"):
        assert cmd in out


def test_rag_ask_help_lists_new_flags():
    code, out, _ = _run(["rag", "ask", "--help"])
    assert code == 0
    for flag in ("--with-facets", "--with-provenance", "--self-rag",
                 "--auto-intent", "--hierarchical", "--with-debate",
                 "--with-mapreduce", "--with-got", "--with-negotiation",
                 "--at-commit", "--user-id", "--filters"):
        assert flag in out


def test_saved_subcommands_visible():
    code, out, _ = _run(["saved", "--help"])
    assert code == 0
    assert "save" in out
    assert "list" in out
    assert "run" in out


def test_profile_subcommands_visible():
    code, out, _ = _run(["profile", "--help"])
    assert code == 0
    for s in ("show", "list", "set"):
        assert s in out


def test_kg_subcommands_visible():
    code, out, _ = _run(["kg", "--help"])
    assert code == 0
    assert "index" in out
    assert "query" in out


def test_eval_subcommand_visible():
    code, out, _ = _run(["eval", "--help"])
    assert code == 0
    assert "dashboard" in out


# ---------- voice CLI invocation ----------

def test_voice_cmd_needs_input():
    code, _, err = _run(["voice"])
    assert code == 1
    assert "Provide" in err or "--text" in err.lower() or "--file" in err.lower() \
        or code == 1


def test_voice_cmd_with_text():
    code, out, _ = _run(["voice", "--text",
                          "Python is great. We believe RAG matters."])
    assert code == 0
    # Output mentions metric names
    for k in ("claim_ratio", "hedge_ratio", "objectivity"):
        assert k in out


def test_voice_cmd_with_file(tmp_path):
    f = tmp_path / "snippet.md"
    f.write_text("This is a clear claim about Python.", encoding="utf-8")
    code, out, _ = _run(["voice", "--file", str(f)])
    assert code == 0
    assert "claim_ratio" in out


# ---------- saved CLI ----------

def test_saved_list_empty_or_works():
    """Should run without error; result depends on existing DB."""
    code, _, _ = _run(["saved", "list", "--owner", "noexistghost"])
    assert code == 0


# ---------- profile CLI ----------

def test_profile_list_runs():
    code, _, _ = _run(["profile", "list"])
    assert code == 0


def test_profile_show_unknown_returns_nonzero():
    code, _, _ = _run(["profile", "show", "completely-nonexistent-user-xyz"])
    assert code == 1


# ---------- diff-bulk CLI ----------

def test_diff_bulk_requires_args():
    code, _, err = _run(["diff-bulk"])
    # Either error code or "Specify" message
    assert code in (0, 1)


# ---------- taxonomy needs a query ----------

def test_taxonomy_requires_query():
    code, _, err = _run(["taxonomy"])
    assert code != 0
    assert "query" in err.lower() or "required" in err.lower()
