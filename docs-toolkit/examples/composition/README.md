# Composition examples — docs-toolkit

Runnable scripts that demonstrate every Sprint 54-92 feature in `docstoolkit.rag.ask()`.

| Script | What it shows |
|---|---|
| `01_minimal.py` | The baseline single-call RAG (no extras) |
| `02_personalize.py` | S6 user profile + S7 read-receipts |
| `03_quality.py` | M2 cross-encoder rerank + I3 provenance + M5 online eval |
| `04_reasoning.py` | I1 self-RAG + N3 graph-of-thoughts + I2 multi-agent debate |
| `05_advanced.py` | M3 hierarchical + M4 auto-intent + I10 mapreduce + I8 time-travel |
| `06_path_C.py` | N2 negotiation + N9 personality + I5 MemGPT memory + N1 metabolism |
| `07_standalone.py` | Helpers: PageRank boost, KG, voice, taxonomy, bandit, diff, assets |
| `08_full_stack.py` | All 17 features stacked in one ask() call |

## Running

```bash
cd docs-toolkit
pip install -e .
python examples/composition/01_minimal.py
```

Each script is self-contained: it creates an in-memory corpus, runs the demo,
and prints the result. No real docs required.
