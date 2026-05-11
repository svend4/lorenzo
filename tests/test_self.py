"""
Тесты для scripts/improve_self.py.

Покрытие:
  - _is_inplace_writer()  — определение скриптов, модифицирующих входные файлы
  - analyze_script()      — AST-анализ: функции, импорты, риск, docstring
"""

import importlib
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_self")

# ── _is_inplace_writer ────────────────────────────────────────────────────────

def test_inplace_writer_basic_red():
    source = textwrap.dedent("""\
        from pathlib import Path
        DOCS = Path("docs")
        for f in DOCS.rglob("*.md"):
            text = f.read_text()
            f.write_text(text + "\\n")
    """)
    assert mod._is_inplace_writer(source) is True


def test_inplace_writer_yellow_safe():
    source = textwrap.dedent("""\
        from pathlib import Path
        DOCS = Path("docs")
        data = []
        for f in DOCS.rglob("*.md"):
            data.append(f.read_text())
        out = DOCS / "REPORT.md"
        out.write_text("\\n".join(data))
    """)
    assert mod._is_inplace_writer(source) is False


def test_inplace_writer_no_write():
    source = textwrap.dedent("""\
        from pathlib import Path
        DOCS = Path("docs")
        for f in DOCS.rglob("*.md"):
            print(f.read_text())
    """)
    assert mod._is_inplace_writer(source) is False


def test_inplace_writer_returns_bool():
    result = mod._is_inplace_writer("print('hello')")
    assert isinstance(result, bool)


def test_inplace_writer_empty_source():
    assert mod._is_inplace_writer("") is False


def test_inplace_writer_marker_constant_red():
    source = textwrap.dedent("""\
        ALREADY_HAS_TOC = "<!-- toc -->"
        for f in DOCS.rglob("*.md"):
            text = f.read_text()
            if ALREADY_HAS_TOC in text:
                continue
            f.write_text(text)
    """)
    assert mod._is_inplace_writer(source) is True


def test_inplace_writer_glob_no_write():
    source = textwrap.dedent("""\
        from pathlib import Path
        results = []
        for f in Path("docs").glob("*.md"):
            results.append(f.stem)
        print(results)
    """)
    assert mod._is_inplace_writer(source) is False

# ── analyze_script ────────────────────────────────────────────────────────────

def _write_script(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def test_analyze_script_returns_scriptinfo(tmp_path):
    script = _write_script(tmp_path, "test_s.py", 'print("hi")')
    result = mod.analyze_script(script)
    assert isinstance(result, mod.ScriptInfo)


def test_analyze_script_captures_name(tmp_path):
    script = _write_script(tmp_path, "improve_test.py", "")
    result = mod.analyze_script(script)
    assert result.name == "improve_test.py"


def test_analyze_script_captures_docstring(tmp_path):
    script = _write_script(tmp_path, "s.py",
        '"""This is a module docstring."""\nprint("hi")\n')
    result = mod.analyze_script(script)
    assert result.doc == "This is a module docstring."


def test_analyze_script_no_docstring(tmp_path):
    script = _write_script(tmp_path, "s.py", "import os\nprint('hi')\n")
    result = mod.analyze_script(script)
    assert result.doc == ""


def test_analyze_script_counts_functions(tmp_path):
    script = _write_script(tmp_path, "s.py", textwrap.dedent("""\
        def foo(): pass
        def bar(): pass
        def baz(): pass
    """))
    result = mod.analyze_script(script)
    assert len(result.functions) == 3
    assert "foo" in result.functions


def test_analyze_script_detects_imports(tmp_path):
    script = _write_script(tmp_path, "s.py", "import json\nimport re\n")
    result = mod.analyze_script(script)
    assert "json" in result.imports
    assert "re" in result.imports


def test_analyze_script_detects_reads(tmp_path):
    script = _write_script(tmp_path, "s.py",
        'from pathlib import Path\nPath("x").read_text()\n')
    result = mod.analyze_script(script)
    assert "read_text" in result.reads


def test_analyze_script_detects_writes(tmp_path):
    script = _write_script(tmp_path, "s.py",
        'from pathlib import Path\nPath("x").write_text("hi")\n')
    result = mod.analyze_script(script)
    assert "write_text" in result.writes


def test_analyze_script_green_risk_no_writes(tmp_path):
    script = _write_script(tmp_path, "s.py",
        '"""Report script."""\nimport json\nprint(json.dumps({}))\n')
    result = mod.analyze_script(script)
    assert result.risk == "green"


def test_analyze_script_yellow_risk_output_file(tmp_path):
    script = _write_script(tmp_path, "s.py", textwrap.dedent("""\
        from pathlib import Path
        DOCS = Path("docs")
        data = []
        for f in DOCS.rglob("*.md"):
            data.append(f.read_text())
        out = DOCS / "REPORT.md"
        out.write_text("\\n".join(data))
    """))
    result = mod.analyze_script(script)
    assert result.risk == "yellow"


def test_analyze_script_red_risk_inplace(tmp_path):
    script = _write_script(tmp_path, "s.py", textwrap.dedent("""\
        from pathlib import Path
        DOCS = Path("docs")
        for f in DOCS.rglob("*.md"):
            text = f.read_text()
            f.write_text(text + "\\n")
    """))
    result = mod.analyze_script(script)
    assert result.risk == "red"


def test_analyze_script_detects_dry_run_arg(tmp_path):
    script = _write_script(tmp_path, "s.py",
        'import argparse\np = argparse.ArgumentParser()\np.add_argument("--dry-run")\n')
    result = mod.analyze_script(script)
    assert result.has_dry_run is True


def test_analyze_script_detects_main_block(tmp_path):
    script = _write_script(tmp_path, "s.py",
        'def main(): pass\nif __name__ == "__main__":\n    main()\n')
    result = mod.analyze_script(script)
    assert result.has_main_block is True


def test_analyze_script_no_main_block(tmp_path):
    script = _write_script(tmp_path, "s.py", "print('hi')\n")
    result = mod.analyze_script(script)
    assert result.has_main_block is False


def test_analyze_script_counts_lines(tmp_path):
    lines = ["print('line %d')" % i for i in range(10)]
    script = _write_script(tmp_path, "s.py", "\n".join(lines) + "\n")
    result = mod.analyze_script(script)
    assert result.lines >= 10


def test_analyze_script_missing_file():
    result = mod.analyze_script(Path("/nonexistent/path/script.py"))
    assert isinstance(result, mod.ScriptInfo)
    assert result.functions == []


def test_analyze_script_real_script():
    # Analyze a real script from the project
    metrics = ROOT / "scripts" / "improve_metrics.py"
    if not metrics.exists():
        pytest.skip("improve_metrics.py not found")
    result = mod.analyze_script(metrics)
    assert result.name == "improve_metrics.py"
    assert len(result.functions) > 0
    assert result.lines > 50
