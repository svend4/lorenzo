# Test Suite Baseline — Phase I.2

Snapshot at branch `claude/continue-development-BrDvi`, HEAD `06e1e8e4`,
date 2026-05-15.

## Counts

| Metric | Value |
|---|---|
| Test files | **538** (`ls tests/test_*.py`) |
| Tests collected | **38 352** (`pytest --collect-only -q`) |
| Collection time | ~9 seconds |
| Full-suite runtime | > 20 minutes single-threaded |

## Notes

- The full pytest takes too long for an interactive baseline (single
  process exceeded 22 min wall-clock with `--timeout=30`). CI runs with
  `pytest -n auto` (xdist) and parallelises across cores.
- The new tests added in this branch (~25 across `test_version`,
  `test_bench_new_suites`, `test_rag_presets`, `test_self_rag_composition`,
  `test_answer_result_trace`) run in <1 second together.
- Subsets of interest, all green at HEAD `06e1e8e4`:
  - `tests/test_rag*.py`, `tests/test_self_rag*.py`,
    `tests/test_answerers.py`, `tests/test_clarifier.py`,
    `tests/test_counterfactual.py`, `tests/test_debate.py`,
    `tests/test_bench*.py` — **371 passed in 2.16s**
  - `tests/test_provenance*.py`, `tests/test_negotiation*.py`,
    `tests/test_self_rag_composition.py` — **148 passed in 0.44s**
  - `tests/test_self_rag.py`, `tests/test_rag_self_rag_integration.py`
    — **75 passed in 0.23s**

## How to refresh this baseline

```bash
# Count
python -m pytest --collect-only -q | tail -3

# Run focused subset (under 5 s)
python -m pytest tests/test_rag_presets.py tests/test_self_rag_composition.py \
                 tests/test_answer_result_trace.py tests/test_bench_new_suites.py \
                 tests/test_version.py -q

# Full suite (CI only; needs -n auto in practice)
python -m pytest -q -n auto --timeout=30
```

## Phase I.2 — exit criteria status

| Criterion | Status |
|---|---|
| Test count documented | ✓ 38 352 |
| Focused subsets green | ✓ all subsets pass |
| Slow tests identified | △ — full `--durations=20` run timed out at 22 min and was killed; can be re-attempted on CI with `-n auto` |
| `test.yml` adds `-n auto` if > 5 min | Not yet — needs CI Actions budget |
