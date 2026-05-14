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


def test_analyze_script_syntax_error(tmp_path):
    """Line 129-130: SyntaxError during parse → returns basic info."""
    script = _write_script(tmp_path, "s.py", "def foo(:\n    pass\n")
    result = mod.analyze_script(script)
    assert isinstance(result, mod.ScriptInfo)
    assert result.lines > 0


def test_analyze_script_from_import(tmp_path):
    """Line 108: ImportFrom node → module added to imports."""
    script = _write_script(tmp_path, "s.py", "from pathlib import Path\n")
    result = mod.analyze_script(script)
    assert "pathlib" in result.imports


def test_analyze_script_assigns_group(tmp_path):
    """Lines 205-209: group assignment via stem keyword matching."""
    script = _write_script(tmp_path, "improve_auto_toc.py", textwrap.dedent("""\
        \"\"\"TOC script.\"\"\"
        def main(): pass
        if __name__ == "__main__":
            main()
    """))
    result = mod.analyze_script(script)
    assert result.group == "deeptext"


# ── cmd_audit ─────────────────────────────────────────────────────────────────

def test_cmd_audit_no_crash(tmp_path, monkeypatch):
    """Lines 220-258: cmd_audit with temp SCRIPTS dir."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    # Create a few test scripts
    (tmp_path / "improve_a.py").write_text('"""Docstring."""\nprint("hi")\n', encoding="utf-8")
    (tmp_path / "improve_b.py").write_text("print('no doc')\n", encoding="utf-8")
    mod.cmd_audit()


def test_cmd_audit_many_no_doc(tmp_path, monkeypatch):
    """Lines 241-244: truncation when > 20 no-doc scripts."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    for i in range(25):
        (tmp_path / f"improve_{i:02d}.py").write_text(f"print({i})\n", encoding="utf-8")
    mod.cmd_audit()


# ── cmd_catalog ───────────────────────────────────────────────────────────────

def test_cmd_catalog_creates_file(tmp_path, monkeypatch):
    """Lines 267-295: cmd_catalog writes JSON file."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CATALOG_PATH", tmp_path / "catalog.json")
    (tmp_path / "improve_test.py").write_text('"""Test script."""\nprint("hi")\n', encoding="utf-8")
    mod.cmd_catalog()
    assert (tmp_path / "catalog.json").exists()


def test_cmd_catalog_counts_risk(tmp_path, monkeypatch):
    """Lines 291-295: risk counts printed."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CATALOG_PATH", tmp_path / "catalog.json")
    (tmp_path / "improve_green.py").write_text('"""Read-only."""\nprint("hi")\n', encoding="utf-8")
    (tmp_path / "improve_yellow.py").write_text(textwrap.dedent("""\
        \"\"\"Writer.\"\"\"
        from pathlib import Path
        DOCS = Path("docs")
        data = []
        for f in DOCS.rglob("*.md"):
            data.append(f.read_text())
        out = DOCS / "OUT.md"
        out.write_text("\\n".join(data))
    """), encoding="utf-8")
    mod.cmd_catalog()


# ── cmd_enrich ────────────────────────────────────────────────────────────────

def test_cmd_enrich_file_not_found(tmp_path, monkeypatch):
    """Lines 313-317: file not found → sys.exit(1)."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    with pytest.raises(SystemExit):
        mod.cmd_enrich("nonexistent_file.py", dry_run=True)


def test_cmd_enrich_adds_docstring_dry_run(tmp_path, monkeypatch):
    """Lines 325-338, 359-360: adds docstring in dry-run mode."""
    script = tmp_path / "improve_test.py"
    script.write_text("def main(): pass\n", encoding="utf-8")
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    mod.cmd_enrich(str(script), dry_run=True)
    # Should not have changed the file in dry-run mode
    assert "def main" in script.read_text(encoding="utf-8")


def test_cmd_enrich_writes_no_dry_run_warning(tmp_path, monkeypatch):
    """Line 348: script writes files but no dry-run → warning added."""
    script = tmp_path / "improve_writer.py"
    # Script that writes files but has no dry-run flag (no --dry-run arg)
    script.write_text(textwrap.dedent("""\
        \"\"\"Has docstring.\"\"\"
        from pathlib import Path
        DOCS = Path("docs")
        data = []
        for f in DOCS.rglob("*.md"):
            data.append(f.read_text())
        out = DOCS / "OUT.md"
        out.write_text("\\n".join(data))
        if __name__ == "__main__":
            pass
    """), encoding="utf-8")
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    mod.cmd_enrich(str(script), dry_run=True)


def test_cmd_enrich_adds_main_block_dry_run(tmp_path, monkeypatch):
    """Line 341-344: adds main block if no __main__ in dry-run."""
    script = tmp_path / "improve_test.py"
    script.write_text('"""Has docstring."""\ndef main(): pass\n', encoding="utf-8")
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    mod.cmd_enrich(str(script), dry_run=True)


def test_cmd_enrich_no_changes_needed(tmp_path, monkeypatch):
    """Lines 350-352: already in good state → no changes."""
    script = tmp_path / "improve_test.py"
    script.write_text(textwrap.dedent("""\
        \"\"\"Has docstring.\"\"\"
        def main(): pass
        if __name__ == "__main__":
            main()
    """), encoding="utf-8")
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    mod.cmd_enrich(str(script), dry_run=True)


def test_cmd_enrich_applies_changes(tmp_path, monkeypatch):
    """Lines 363-364: apply=True writes changes."""
    script = tmp_path / "improve_test.py"
    script.write_text("def main(): pass\n", encoding="utf-8")
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    mod.cmd_enrich(str(script), dry_run=False)
    content = script.read_text(encoding="utf-8")
    assert '"""' in content  # docstring added


# ── cmd_enrich_batch ──────────────────────────────────────────────────────────

def test_cmd_enrich_batch_dry_run(tmp_path, monkeypatch):
    """Lines 373-460: batch enrich in dry-run mode."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    (tmp_path / "improve_a.py").write_text("def main(): pass\n", encoding="utf-8")
    (tmp_path / "improve_b.py").write_text('"""Good."""\ndef main(): pass\nif __name__ == "__main__":\n    main()\n', encoding="utf-8")
    mod.cmd_enrich_batch(dry_run=True)


def test_cmd_enrich_batch_with_writer_script(tmp_path, monkeypatch):
    """Lines 385, 438: script with writes but no dry-run → ⚠ нет --dry-run in missing."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    # Script that writes files but has no dry-run and has docstring+main → only warning
    (tmp_path / "improve_writer.py").write_text(textwrap.dedent("""\
        \"\"\"Has docstring.\"\"\"
        from pathlib import Path
        DOCS = Path("docs")
        data = []
        for f in DOCS.rglob("*.md"):
            data.append(f.read_text())
        out = DOCS / "OUT.md"
        out.write_text("\\n".join(data))
        if __name__ == "__main__":
            pass
    """), encoding="utf-8")
    mod.cmd_enrich_batch(dry_run=True)


def test_cmd_enrich_batch_apply_with_changes(tmp_path, monkeypatch):
    """Lines 450-452: apply batch mode with real changes writes file."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    # Script without docstring, so it needs changes
    script = tmp_path / "improve_needs_doc.py"
    script.write_text("def main(): pass\n", encoding="utf-8")
    mod.cmd_enrich_batch(dry_run=False)
    content = script.read_text(encoding="utf-8")
    # Should have docstring or main block added
    assert '"""' in content or "__main__" in content


def test_cmd_enrich_batch_apply_warnings_only(tmp_path, monkeypatch):
    """Line 454: apply batch with only ⚠ warning (no + changes) → skipped."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    # Script that has docstring+main but writes without dry-run → only warning
    script = tmp_path / "improve_writer_ok.py"
    script.write_text(textwrap.dedent("""\
        \"\"\"Has docstring.\"\"\"
        from pathlib import Path
        DOCS = Path("docs")
        data = []
        for f in DOCS.rglob("*.md"):
            data.append(f.read_text())
        out = DOCS / "OUT.md"
        out.write_text("\\n".join(data))
        if __name__ == "__main__":
            pass
    """), encoding="utf-8")
    mod.cmd_enrich_batch(dry_run=False)  # should skip (only ⚠ warning, no real changes)


def test_cmd_enrich_batch_all_good(tmp_path, monkeypatch):
    """Lines 393-395: all scripts already good."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    (tmp_path / "improve_good.py").write_text(textwrap.dedent("""\
        \"\"\"Good docstring.\"\"\"
        def main(): pass
        if __name__ == "__main__":
            main()
    """), encoding="utf-8")
    mod.cmd_enrich_batch(dry_run=True)


def test_cmd_enrich_batch_apply(tmp_path, monkeypatch):
    """Lines 448-454: apply=False (dry_run=False) writes changes."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    script = tmp_path / "improve_needs_work.py"
    script.write_text("def main(): pass\n", encoding="utf-8")
    mod.cmd_enrich_batch(dry_run=False)
    content = script.read_text(encoding="utf-8")
    assert '"""' in content or "__main__" in content


# ── cmd_generate ──────────────────────────────────────────────────────────────

def test_cmd_generate_list_patterns(tmp_path, monkeypatch):
    """Lines 828-832: list patterns."""
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    mod.cmd_generate("_list_", "list", "", dry_run=True)


def test_cmd_generate_unknown_pattern(tmp_path, monkeypatch):
    """Lines 833-838: unknown pattern → sys.exit(1)."""
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    with pytest.raises(SystemExit):
        mod.cmd_generate("my_script", "UNKNOWN_PATTERN", "description", dry_run=True)


def test_cmd_generate_dry_run(tmp_path, monkeypatch):
    """Lines 840-863: generate with dry-run → no file created."""
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    mod.cmd_generate("my_report", "REPORT", "My custom report script", dry_run=True)
    assert not (tmp_path / "generated" / "improve_my_report.py").exists()


def test_cmd_generate_apply(tmp_path, monkeypatch):
    """Lines 866-869: apply → file created."""
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_generate("my_report", "REPORT", "My custom report script", dry_run=False)
    assert (tmp_path / "generated" / "improve_my_report.py").exists()


def test_cmd_generate_enricher_pattern(tmp_path, monkeypatch):
    """Test ENRICHER pattern generation."""
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_generate("my_enricher", "ENRICHER", "My enricher", dry_run=False)
    assert (tmp_path / "generated" / "improve_my_enricher.py").exists()


def test_cmd_generate_analyzer_pattern(tmp_path, monkeypatch):
    """Test ANALYZER pattern generation."""
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.cmd_generate("my_analyzer", "ANALYZER", "My analyzer", dry_run=False)
    assert (tmp_path / "generated" / "improve_my_analyzer.py").exists()


# ── cmd_cross_read ────────────────────────────────────────────────────────────

def test_cmd_cross_read_no_crash(tmp_path, monkeypatch):
    """Lines 878-924: cmd_cross_read with temp paths."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(mod, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts" / "improve_test.py").write_text("# test\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("improve_test.py improve_missing.py\n", encoding="utf-8")
    mod.cmd_cross_read()


def test_cmd_cross_read_with_docs(tmp_path, monkeypatch):
    """Lines 893-900: reads docs/ .md files for mentions."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(mod, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts" / "improve_health.py").write_text("# health\n", encoding="utf-8")
    (tmp_path / "docs" / "doc.md").write_text(
        "Use improve_health.py and improve_missing.py.\n", encoding="utf-8"
    )
    (tmp_path / "CLAUDE.md").write_text("improve_health.py\n", encoding="utf-8")
    mod.cmd_cross_read()


def test_cmd_cross_read_unregistered_script(tmp_path, monkeypatch):
    """Line 918: script exists but not in CLAUDE.md → printed in exist_not_in_claude."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(mod, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts" / "improve_unregistered.py").write_text("# unregistered\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("nothing here\n", encoding="utf-8")
    mod.cmd_cross_read()


def test_cmd_cross_read_read_exception(tmp_path, monkeypatch):
    """Lines 899-900: exception reading docs/*.md → caught silently."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(mod, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs").mkdir()
    bad = tmp_path / "docs" / "bad.md"
    bad.write_text("content", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.cmd_cross_read()


# ── main() ────────────────────────────────────────────────────────────────────

def test_main_audit_default(tmp_path, monkeypatch):
    """Lines 932-958: main() with no args defaults to audit."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog"])
    mod.main()


def test_main_audit_flag(tmp_path, monkeypatch):
    """Lines 957-958: --audit flag runs cmd_audit."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--audit"])
    mod.main()


def test_main_catalog_flag(tmp_path, monkeypatch):
    """Lines 960-961: --catalog flag runs cmd_catalog."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CATALOG_PATH", tmp_path / "catalog.json")
    monkeypatch.setattr(sys, "argv", ["prog", "--catalog"])
    mod.main()


def test_main_batch_flag(tmp_path, monkeypatch):
    """Lines 963-964: --batch flag runs cmd_enrich_batch."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    (tmp_path / "improve_x.py").write_text("print('x')\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["prog", "--batch", "--dry-run"])
    mod.main()


def test_main_enrich_flag(tmp_path, monkeypatch):
    """Lines 965-966: --enrich FILE flag runs cmd_enrich."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    script = tmp_path / "improve_test.py"
    script.write_text("def main(): pass\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["prog", "--enrich", str(script), "--dry-run"])
    mod.main()


def test_main_cross_read_flag(tmp_path, monkeypatch):
    """Lines 968-969: --cross-read flag runs cmd_cross_read."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path / "docs")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "CLAUDE.md").write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["prog", "--cross-read"])
    mod.main()


def test_main_generate_no_name_exits(tmp_path, monkeypatch):
    """Lines 972-975: --generate without --name → sys.exit(1)."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(sys, "argv", ["prog", "--generate"])
    with pytest.raises(SystemExit):
        mod.main()


def test_main_generate_with_list(tmp_path, monkeypatch):
    """Line 976-978: --generate --pattern list."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    monkeypatch.setattr(sys, "argv", ["prog", "--generate", "--pattern", "list"])
    mod.main()


def test_main_generate_with_name(tmp_path, monkeypatch):
    """Lines 976-978: --generate --name my_script --dry-run."""
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    monkeypatch.setattr(mod, "GENERATED_DIR", tmp_path / "generated")
    monkeypatch.setattr(sys, "argv", ["prog", "--generate", "--name", "my_script", "--dry-run"])
    mod.main()


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 982: __main__ block."""
    import runpy
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--audit"]
        monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
        script_path = str(ROOT / "scripts" / "improve_self.py")
        runpy.run_path(script_path, run_name="__main__")
    finally:
        sys.argv = orig_argv
