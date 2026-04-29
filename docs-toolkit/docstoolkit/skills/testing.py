"""Golden-output tests для скилов.

Скилл — markdown с инструкциями, поэтому «тестировать» нужно структурно
и через assertions на текстовых паттернах.

Формат golden test (`<skill>.test.yaml`):

    skill: search
    cases:
      - name: russian_query
        input:
          query: "найди про память"
        expects:
          mentions: ["search_docs", "passages"]   # должны быть в выводе
          not_mentions: ["DELETE", "DROP"]        # запрещены
          min_length: 200
          max_length: 5000
          required_sections: ["Шаги", "Связанные скилы"]
          regex_match: '\\d+ результатов'

      - name: empty_query
        input:
          query: ""
        expects:
          mentions: ["укажите", "query"]

Запускается:
    docstoolkit skills test                  # все
    docstoolkit skills test --skill search   # один
    docstoolkit skills test --golden-dir custom/path
"""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from docstoolkit.frontmatter import parse_yaml
from docstoolkit.skills.registry import get_skill_path


@dataclass
class TestResult:
    name: str
    skill: str
    status: str  # ok | fail | skip
    failures: list[str] = field(default_factory=list)
    duration_ms: int = 0


@dataclass
class GoldenTest:
    skill: str
    name: str
    inputs: dict
    expects: dict


def load_golden_tests(golden_dir: Path) -> list[GoldenTest]:
    """Загружает все *.test.yaml из директории."""
    if not golden_dir.exists():
        return []

    tests: list[GoldenTest] = []
    for f in golden_dir.glob("*.test.yaml"):
        try:
            text = f.read_text(encoding="utf-8")
            # Простая разбивка yaml: skill: name + cases:
            data = _parse_simple_yaml(text)
        except Exception as e:
            print(f"⚠️ {f.name}: {e}", file=sys.stderr)
            continue

        skill = data.get("skill", f.stem.replace(".test", ""))
        for case in data.get("cases", []):
            tests.append(GoldenTest(
                skill=skill,
                name=case.get("name", "unnamed"),
                inputs=case.get("input", {}),
                expects=case.get("expects", {}),
            ))
    return tests


def _parse_simple_yaml(text: str) -> dict:
    """Минимальный YAML парсер для golden tests:
    skill: name
    cases:
      - name: x
        input: {key: val}
        expects:
          mentions: [a, b]
          min_length: 100
    """
    result: dict = {}
    cases: list[dict] = []
    current_case: dict | None = None
    current_section: str | None = None
    indent_stack = []

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        indent = len(line) - len(line.lstrip())

        # Top-level
        if indent == 0:
            if stripped.startswith("skill:"):
                result["skill"] = stripped.split(":", 1)[1].strip().strip('"\'')
            elif stripped.startswith("cases:"):
                pass
            i += 1
            continue

        # Case start (- name: x)
        if stripped.startswith("- name:") or stripped.startswith("-name:"):
            if current_case:
                cases.append(current_case)
            current_case = {"name": stripped.split(":", 1)[1].strip().strip('"\''),
                            "input": {}, "expects": {}}
            current_section = None
            i += 1
            continue

        if current_case is None:
            i += 1
            continue

        # input: / expects: block
        if stripped.startswith("input:"):
            current_section = "input"
            i += 1
            continue
        if stripped.startswith("expects:"):
            current_section = "expects"
            i += 1
            continue

        # Field
        m = re.match(r'^([\w_]+)\s*:\s*(.*)$', stripped)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                parsed_value = ([s.strip().strip('"\'') for s in inner.split(",")]
                                if inner else [])
            elif value.startswith('"') and value.endswith('"'):
                parsed_value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                parsed_value = value[1:-1]
            elif re.fullmatch(r'\d+', value):
                parsed_value = int(value)
            elif re.fullmatch(r'\d+\.\d+', value):
                parsed_value = float(value)
            else:
                parsed_value = value
            if current_section == "input":
                current_case["input"][key] = parsed_value
            elif current_section == "expects":
                current_case["expects"][key] = parsed_value
        i += 1

    if current_case:
        cases.append(current_case)
    result["cases"] = cases
    return result


def check_assertions(content: str, expects: dict) -> list[str]:
    """Проверяет content против expects, возвращает список нарушений."""
    failures: list[str] = []

    # mentions
    for needed in expects.get("mentions", []):
        if needed.lower() not in content.lower():
            failures.append(f"mentions: missing '{needed}'")

    # not_mentions
    for forbidden in expects.get("not_mentions", []):
        if forbidden.lower() in content.lower():
            failures.append(f"not_mentions: contains forbidden '{forbidden}'")

    # length
    if "min_length" in expects:
        if len(content) < expects["min_length"]:
            failures.append(f"min_length: {len(content)} < {expects['min_length']}")
    if "max_length" in expects:
        if len(content) > expects["max_length"]:
            failures.append(f"max_length: {len(content)} > {expects['max_length']}")

    # required_sections
    for sec in expects.get("required_sections", []):
        if not re.search(rf'^##\s+{re.escape(sec)}', content, re.MULTILINE):
            failures.append(f"missing section '## {sec}'")

    # regex_match
    if expects.get("regex_match"):
        pat = expects["regex_match"]
        if not re.search(pat, content):
            failures.append(f"regex no match: {pat!r}")

    return failures


def run_golden_test(test: GoldenTest) -> TestResult:
    """Применяет тест к скилу.

    «Применяет» здесь = читает текст скила (он markdown с инструкциями)
    и проверяет на наличие упомянутых паттернов / структуры.
    Это структурный тест, не функциональный (для функционального
    нужен LLM или MCP-runtime).
    """
    import time
    t0 = time.time()

    skill_path = get_skill_path(test.skill)
    if not skill_path or not skill_path.exists():
        return TestResult(test.name, test.skill, "skip",
                          [f"skill {test.skill!r} not found"],
                          int((time.time() - t0) * 1000))

    content = skill_path.read_text(encoding="utf-8")
    failures = check_assertions(content, test.expects)
    duration_ms = int((time.time() - t0) * 1000)
    return TestResult(test.name, test.skill,
                      "ok" if not failures else "fail",
                      failures, duration_ms)


def run_golden_tests(golden_dir: Path, skill_filter: str = "") -> list[TestResult]:
    tests = load_golden_tests(golden_dir)
    if skill_filter:
        tests = [t for t in tests if t.skill == skill_filter]
    return [run_golden_test(t) for t in tests]


def render_results(results: list[TestResult]) -> str:
    """Markdown-отчёт."""
    if not results:
        return "_(нет тестов)_"

    by_status = {"ok": 0, "fail": 0, "skip": 0}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1

    icon = "✅" if by_status["fail"] == 0 else "❌"
    lines = [f"{icon} {by_status['ok']} ok, {by_status['fail']} fail, {by_status['skip']} skip\n"]

    for r in results:
        ico = {"ok": "✓", "fail": "✗", "skip": "-"}[r.status]
        lines.append(f"{ico} [{r.skill}] {r.name} ({r.duration_ms}ms)")
        for f in r.failures:
            lines.append(f"    — {f}")
    return "\n".join(lines)
