"""Smoke tests: each example script in examples/composition/ runs end-to-end
without errors."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).resolve().parent.parent / "examples" / "composition"


def _scripts():
    return sorted(EXAMPLES.glob("*.py"))


@pytest.mark.parametrize("script", _scripts(), ids=lambda p: p.name)
def test_example_runs(script):
    """Each .py example script should exit 0 within 30 seconds."""
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        print("STDOUT:", result.stdout[-500:])
        print("STDERR:", result.stderr[-500:])
    assert result.returncode == 0, f"{script.name} failed"
