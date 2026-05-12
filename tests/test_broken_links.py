"""
Тесты для scripts/improve_broken_links.py.

Покрытие:
  - anchor_from_heading() — GitHub-style якорь из заголовка
  - build_anchor_map()    — словарь file → set of valid anchors
  - check_links()         — проверка ссылок в файле
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_broken_links")

# ── anchor_from_heading ───────────────────────────────────────────────────────

def test_anchor_from_heading_returns_string():
    result = mod.anchor_from_heading("My Heading")
    assert isinstance(result, str)


def test_anchor_from_heading_starts_with_hash():
    result = mod.anchor_from_heading("My Heading")
    assert result.startswith("#")


def test_anchor_from_heading_lowercases():
    result = mod.anchor_from_heading("My Heading")
    assert result == result.lower()


def test_anchor_from_heading_replaces_spaces_with_dashes():
    result = mod.anchor_from_heading("My Section Title")
    assert result == "#my-section-title"


def test_anchor_from_heading_removes_special_chars():
    result = mod.anchor_from_heading("Title: With Special Chars!")
    assert ":" not in result
    assert "!" not in result


def test_anchor_from_heading_simple():
    result = mod.anchor_from_heading("hello world")
    assert result == "#hello-world"


def test_anchor_from_heading_preserves_hyphens():
    result = mod.anchor_from_heading("my-already-hyphenated")
    assert result == "#my-already-hyphenated"


def test_anchor_from_heading_cyrillic():
    result = mod.anchor_from_heading("Архитектура системы")
    assert result.startswith("#")
    # Letters preserved, spaces → dashes
    assert " " not in result[1:]


# ── build_anchor_map ──────────────────────────────────────────────────────────

def test_build_anchor_map_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    result = mod.build_anchor_map()
    assert isinstance(result, dict)


def test_build_anchor_map_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    result = mod.build_anchor_map()
    assert result == {}


def test_build_anchor_map_finds_headings(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n## My Section\n\n### Subsection\n", encoding="utf-8")
    result = mod.build_anchor_map()
    assert str(f) in result
    anchors = result[str(f)]
    assert "#my-section" in anchors


def test_build_anchor_map_values_are_sets(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    f = tmp_path / "doc.md"
    f.write_text("# Title\n## Section\n", encoding="utf-8")
    result = mod.build_anchor_map()
    assert isinstance(result[str(f)], set)


# ── check_links ───────────────────────────────────────────────────────────────

def test_check_links_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n\nNo links here.", encoding="utf-8")
    result = mod.check_links(f, {})
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_check_links_no_links_no_errors(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n\nNo links here.", encoding="utf-8")
    broken, ok = mod.check_links(f, {})
    assert broken == []


def test_check_links_valid_link_no_error(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    target = tmp_path / "target.md"
    target.write_text("# Target", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("See [Target](target.md) here.", encoding="utf-8")
    anchor_map = {str(target): set()}
    broken, ok = mod.check_links(source, anchor_map)
    assert broken == []


def test_check_links_missing_file_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("See [Missing](nonexistent.md) here.", encoding="utf-8")
    broken, ok = mod.check_links(source, {})
    assert len(broken) >= 1


def test_check_links_http_links_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("See [External](https://example.com) here.", encoding="utf-8")
    broken, ok = mod.check_links(source, {})
    assert broken == []


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_broken_links_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()
    assert (tmp_path / "BROKEN_LINKS.md").exists()


def test_main_broken_links_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nSee [internal](other.md) here.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()
    assert (tmp_path / "BROKEN_LINKS.md").exists()


def test_main_broken_links_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    mod.main()
    text = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_find_closest_file_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "target.md").write_text("# Target\n\nContent.", encoding="utf-8")
    result = mod._find_closest_file("target.md")
    assert result is not None
    assert result.name == "target.md"


def test_find_closest_file_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_closest_file("nonexistent.md")
    assert result is None


def test_try_fix_link_with_anchor(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "real.md").write_text("# Real\n\nContent.", encoding="utf-8")
    src = tmp_path / "source.md"
    result = mod._try_fix_link(src, "real.md#section")
    # Either returns a fix or None — just should not crash
    assert result is None or isinstance(result, str)


def test_fix_broken_links_empty_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    result = mod.fix_broken_links(f, [])
    assert result == 0


def test_fix_broken_links_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "source.md"
    f.write_text("# Title\n\nSee [link](missing.md).", encoding="utf-8")
    broken = [{"file": "source.md", "text": "link", "target": "missing.md",
               "issue": "файл не существует"}]
    result = mod.fix_broken_links(f, broken)
    assert isinstance(result, int)


def test_check_links_external_link_not_broken(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nSee [link](https://example.com).", encoding="utf-8")
    broken, errors = mod.check_links(f, {})
    assert all(b["target"] != "https://example.com" for b in broken)


def test_check_links_broken_internal(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nSee [link](missing.md).", encoding="utf-8")
    broken, errors = mod.check_links(f, {})
    assert len(broken) > 0
    assert broken[0]["issue"] == "файл не существует"


def test_build_anchor_map_with_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n## Section One\n\n## Section One\n", encoding="utf-8")
    result = mod.build_anchor_map()
    assert str(f) in result
    anchors = result[str(f)]
    assert any("section-one" in a for a in anchors)


def test_safe_exists_returns_false_for_missing():
    result = mod._safe_exists(Path("/nonexistent/path/that/does/not/exist.md"))
    assert result is False


def test_safe_exists_oserror(monkeypatch):
    """Lines 51-52: OSError path in _safe_exists."""
    from unittest.mock import patch
    with patch.object(Path, "exists", side_effect=OSError("too long")):
        result = mod._safe_exists(Path("/some/path.md"))
    assert result is False


def test_safe_exists_returns_true_for_existing(tmp_path):
    f = tmp_path / "real.md"
    f.write_text("# Real", encoding="utf-8")
    assert mod._safe_exists(f) is True


def test_build_anchor_map_oserror(tmp_path, monkeypatch):
    """Lines 64-65: OSError when reading file."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    (tmp_path / "bad.md").write_text("# Title", encoding="utf-8")
    from unittest.mock import patch
    with patch.object(Path, "read_text", side_effect=OSError("cannot read")):
        result = mod.build_anchor_map()
    assert isinstance(result, dict)


def test_try_fix_link_finds_file_in_subdir(tmp_path, monkeypatch):
    """Lines 103-104: _try_fix_link returns relative path when found elsewhere."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "real.md").write_text("# Real", encoding="utf-8")
    src = tmp_path / "source.md"
    result = mod._try_fix_link(src, "real.md")
    assert result is not None
    assert "real.md" in result


def test_fix_broken_links_skips_wrong_issue(tmp_path, monkeypatch):
    """Line 117: continue when issue is not 'файл не существует'."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nSee [link](#section).", encoding="utf-8")
    broken = [{"file": "doc.md", "text": "link", "target": "#section",
               "issue": "якорь не найден"}]
    result = mod.fix_broken_links(f, broken)
    assert result == 0


def test_fix_broken_links_with_fixable_link(tmp_path, monkeypatch):
    """Lines 120-127: fix_broken_links applies a fix."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "real.md").write_text("# Real", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("# Source\n\nSee [link](real.md).", encoding="utf-8")
    broken = [{"file": "source.md", "text": "link", "target": "real.md",
               "issue": "файл не существует"}]
    result = mod.fix_broken_links(source, broken)
    assert result >= 1


def test_fix_broken_links_dry_run_with_fixable(tmp_path, monkeypatch, capsys):
    """Line 124: dry-run print in fix_broken_links."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "real.md").write_text("# Real", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("# Source\n\nSee [link](real.md).", encoding="utf-8")
    broken = [{"file": "source.md", "text": "link", "target": "real.md",
               "issue": "файл не существует"}]
    result = mod.fix_broken_links(source, broken)
    assert result >= 1
    out = capsys.readouterr().out
    assert "dry" in out


def test_check_links_oserror(tmp_path, monkeypatch):
    """Lines 143-144: OSError when reading file in check_links."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "bad.md"
    f.write_text("# Title", encoding="utf-8")
    from unittest.mock import patch
    with patch.object(Path, "read_text", side_effect=OSError("cannot read")):
        broken, errs = mod.check_links(f, {})
    assert broken == []
    assert errs == []


def test_check_links_anchor_only_missing(tmp_path, monkeypatch):
    """Lines 160-162: anchor-only link not in map → broken."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("# Title\n\nSee [Section](#missing-section) here.", encoding="utf-8")
    broken, _ = mod.check_links(source, {})
    targets = [b["target"] for b in broken]
    assert "#missing-section" in targets


def test_check_links_absolute_path(tmp_path, monkeypatch):
    """Line 173: absolute link starting with '/'."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    source = tmp_path / "source.md"
    source.write_text("See [link](/nonexistent/path.md).", encoding="utf-8")
    broken, _ = mod.check_links(source, {})
    assert len(broken) >= 1


def test_check_links_link_with_anchor_existing_file(tmp_path, monkeypatch):
    """Relative link to existing file with anchor — file exists so no 'file not found' error."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    target = tmp_path / "target.md"
    target.write_text("# Target\n\n## Real Section\n", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("See [link](target.md#nonexistent-anchor).", encoding="utf-8")
    anchor_map = {str(target): {"#real-section"}}
    broken, _ = mod.check_links(source, anchor_map)
    # File exists → no "файл не существует" error for this link
    assert not any(b.get("issue") == "файл не существует" and "target.md" in b.get("target", "") for b in broken)


def test_check_links_too_long_path(tmp_path, monkeypatch):
    """Lines 188-193: path longer than MAX_PATH_LEN → os_errors."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "MAX_PATH_LEN", 10)
    source = tmp_path / "source.md"
    source.write_text("See [link](some/very/long/path/to/missing.md).", encoding="utf-8")
    _, os_errs = mod.check_links(source, {})
    assert len(os_errs) >= 1


def test_main_with_section(tmp_path, monkeypatch, capsys):
    """Line 218: print section name when SECTION is set."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "01-test")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    (tmp_path / "01-test").mkdir()
    mod.main()
    out = capsys.readouterr().out
    assert "01-test" in out


def test_main_fix_mode(tmp_path, monkeypatch, capsys):
    """Line 220: print fix mode info."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", True)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()
    out = capsys.readouterr().out
    assert "dry" in out.lower() or "fix" in out.lower() or "исправ" in out.lower()


def test_main_fix_applies_to_broken(tmp_path, monkeypatch):
    """Lines 240-242, 247: FIX=True with actual broken links."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", True)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    (tmp_path / "doc.md").write_text("# Title\n\nSee [link](missing.md).", encoding="utf-8")
    mod.main()
    assert (tmp_path / "BROKEN_LINKS.md").exists()


def test_main_many_broken_links(tmp_path, monkeypatch):
    """Line 280: more than 50 broken links → truncation message."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    links = "\n".join(f"- [link{i}](missing{i}.md)" for i in range(60))
    (tmp_path / "doc.md").write_text(f"# Title\n\n{links}", encoding="utf-8")
    mod.main()
    content = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert "ещё" in content


def test_main_with_os_errors(tmp_path, monkeypatch):
    """Lines 283-290, 333-337: OS errors in broken links report."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "MAX_PATH_LEN", 10)
    (tmp_path / "doc.md").write_text("See [link](some/long/path/to/file.md).", encoding="utf-8")
    mod.main()
    content = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert "путь" in content.lower() or "Пропущено" in content


def test_main_with_external_urls(tmp_path, monkeypatch):
    """Lines 299-304, 311: External URLs extracted and listed."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nSee https://github.com/test/repo for details.\n",
        encoding="utf-8"
    )
    mod.main()
    content = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert "github.com" in content


def test_main_skips_broken_links_md(tmp_path, monkeypatch):
    """Line 235: BROKEN_LINKS.md is skipped during scan."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    # Pre-create BROKEN_LINKS.md with a broken link inside it
    (tmp_path / "BROKEN_LINKS.md").write_text("See [skip](missing_skip.md).", encoding="utf-8")
    (tmp_path / "doc.md").write_text("# Normal doc\n\nNo links.", encoding="utf-8")
    mod.main()
    content = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    # missing_skip.md should NOT appear (BROKEN_LINKS.md was skipped)
    assert "missing_skip" not in content


def test_main_skips_obsidian_dir(tmp_path, monkeypatch):
    """Line 237: files in SKIP_DIRS (obsidian) are skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    obsidian_dir = tmp_path / "obsidian"
    obsidian_dir.mkdir()
    (obsidian_dir / "note.md").write_text("See [link](skipped_file.md).", encoding="utf-8")
    (tmp_path / "normal.md").write_text("# Normal\n\nNo links.", encoding="utf-8")
    mod.main()
    content = (tmp_path / "BROKEN_LINKS.md").read_text(encoding="utf-8")
    assert "skipped_file" not in content


def test_fix_broken_links_write_oserror(tmp_path, monkeypatch, capsys):
    """Lines 131-132: OSError when writing fixed file is caught and printed."""
    from pathlib import Path as _Path
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    # Put real.md in subdir so _try_fix_link can find it at a different location
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "real.md").write_text("# Real", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("# Source\n\nSee [link](real.md).", encoding="utf-8")
    # The broken target "real.md" resolves to tmp_path/real.md (doesn't exist there)
    # _try_fix_link will find subdir/real.md and propose a fix
    broken = [{"file": "source.md", "text": "link", "target": "real.md",
               "issue": "файл не существует"}]
    original_write_text = _Path.write_text
    def fake_write_text(self, *args, **kwargs):
        if self.name == "source.md":
            raise OSError("permission denied")
        return original_write_text(self, *args, **kwargs)
    monkeypatch.setattr(_Path, "write_text", fake_write_text)
    result = mod.fix_broken_links(source, broken)
    out = capsys.readouterr().out
    assert "ошибка записи" in out


def test_main_external_urls_oserror(tmp_path, monkeypatch):
    """Lines 299-300: OSError when reading file for external URLs is silently skipped."""
    from pathlib import Path as _Path
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION", "")
    monkeypatch.setattr(mod, "FIX", False)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    problem = tmp_path / "problem.md"
    problem.write_text("# OK\n\nSee https://example.com for info.", encoding="utf-8")
    original_read_text = _Path.read_text
    read_count = [0]
    def fake_read_text(self, *args, **kwargs):
        if self == problem:
            read_count[0] += 1
            if read_count[0] > 1:
                raise OSError("read error")
        return original_read_text(self, *args, **kwargs)
    monkeypatch.setattr(_Path, "read_text", fake_read_text)
    mod.main()
    assert (tmp_path / "BROKEN_LINKS.md").exists()
