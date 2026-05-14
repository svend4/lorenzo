#!/usr/bin/env python3
"""
verify_all_workflows.py — локальная симуляция каждого GitHub Actions workflow.

Цель: проверить, что workflows СМОГУТ работать в CI, не сжигая минуты Actions
и не дожидаясь очереди.

Что делает:
  - Парсит каждый .github/workflows/*.yml
  - Для каждого workflow определяет: какие скрипты/тесты он запускает
  - Воспроизводит ключевые шаги локально (компиляция Python, pytest, validation)
  - Отчитывается о результате: ✅ pass / ❌ fail / ⚠️ skip / ⏸ manual-only

Запуск:
    python scripts/verify_all_workflows.py              # все workflows
    python scripts/verify_all_workflows.py --only test  # только test.yml
    python scripts/verify_all_workflows.py --quick      # пропустить медленные шаги (pytest)
    python scripts/verify_all_workflows.py --json       # JSON-вывод

Ограничения:
  - Не запускает workflow на GitHub runner'е — только локальная симуляция
  - Не воспроизводит matrix-конфигурации (только linux ubuntu-latest)
  - Не воспроизводит actions/checkout (мы уже в чекауте)
"""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = ROOT / ".github" / "workflows"


# ── Status enum ───────────────────────────────────────────────────────────────

class Status:
    PASS = "✅ pass"
    FAIL = "❌ fail"
    SKIP = "⚠️  skip"
    MANUAL = "⏸  manual-only"


# ── YAML mini-parser (без PyYAML — чтобы не тащить зависимость) ───────────────

def parse_workflow_yaml(path: Path) -> dict:
    """Извлекает ключевые поля из workflow YAML без PyYAML.

    Возвращает: {name, triggers: [push|pull_request|schedule|workflow_dispatch],
                 jobs: [name], paths: [...], cron: [...]}
    """
    text = path.read_text(encoding="utf-8")
    info: dict = {
        "file": path.name,
        "name": None,
        "triggers": [],
        "jobs": [],
        "paths": [],
        "cron": [],
        "branches": [],
    }

    # name:
    m = re.search(r'^name:\s*(.+?)(?:\s*#|$)', text, re.MULTILINE)
    if m:
        info["name"] = m.group(1).strip().strip('"\'')

    # triggers section
    on_match = re.search(r'^on:\s*\n((?:\s+.+\n?)+?)(?=^\S|\Z)',
                         text, re.MULTILINE)
    if on_match:
        on_block = on_match.group(1)
        for trig in ("push", "pull_request", "schedule", "workflow_dispatch"):
            if re.search(rf'^\s+{trig}:', on_block, re.MULTILINE):
                info["triggers"].append(trig)
        # cron
        info["cron"] = re.findall(r'cron:\s*[\'"](.+?)[\'"]', on_block)
        # branches
        for m in re.finditer(r'branches:\s*\[(.+?)\]', on_block):
            info["branches"].extend(
                b.strip().strip('"\'') for b in m.group(1).split(",")
            )
        # paths
        for m in re.finditer(r'^\s+paths:\s*\n((?:\s+- .+\n?)+)',
                             on_block, re.MULTILINE):
            info["paths"].extend(re.findall(r'-\s*[\'"]?(.+?)[\'"]?$',
                                            m.group(1), re.MULTILINE))

    # jobs
    info["jobs"] = re.findall(r'^\s\s([a-z][a-z0-9_-]*):\s*\n\s+(?:name:|runs-on:)',
                              text, re.MULTILINE)

    return info


# ── Verifier per workflow ─────────────────────────────────────────────────────

def run_cmd(cmd: list[str], cwd: Path = ROOT, timeout: int = 600) -> tuple[int, str]:
    """Запустить команду, вернуть (returncode, output_tail)."""
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout
        )
        out = (proc.stdout + proc.stderr).strip()
        tail = "\n".join(out.splitlines()[-5:]) if out else ""
        return proc.returncode, tail
    except subprocess.TimeoutExpired:
        return 124, f"⏱ timeout after {timeout}s"
    except FileNotFoundError as e:
        return 127, f"command not found: {e}"


def verify_test_yml(quick: bool) -> dict:
    """Симулирует test.yml: python-syntax + pytest tests/."""
    result: dict = {"steps": []}

    # Step 1: python syntax check
    t0 = time.time()
    py_files = list((ROOT / "scripts").glob("*.py"))
    bad = []
    for f in py_files:
        rc, _ = run_cmd(["python", "-m", "py_compile", str(f)], timeout=30)
        if rc != 0:
            bad.append(f.name)
    result["steps"].append({
        "name": "python-syntax (scripts/)",
        "status": Status.PASS if not bad else Status.FAIL,
        "details": f"{len(py_files)} files checked"
                   + (f", {len(bad)} failed: {bad[:3]}" if bad else ""),
        "elapsed_s": round(time.time() - t0, 1),
    })

    if quick:
        result["steps"].append({
            "name": "pytest tests/ (skipped, --quick)",
            "status": Status.SKIP,
            "details": "use without --quick to run pytest",
            "elapsed_s": 0,
        })
        return result

    # Step 2: pytest tests/
    t0 = time.time()
    rc, tail = run_cmd(
        ["python", "-m", "pytest", "tests/",
         "-q", "--tb=no", "-p", "no:cacheprovider", "--timeout=60"],
        timeout=900,
    )
    result["steps"].append({
        "name": "pytest tests/",
        "status": Status.PASS if rc == 0 else Status.FAIL,
        "details": tail.split("\n")[-1] if tail else "",
        "elapsed_s": round(time.time() - t0, 1),
    })
    return result


def verify_benchmark_yml(quick: bool) -> dict:
    """benchmark.yml — запускает docs-toolkit bench."""
    if quick:
        return {"steps": [{"name": "docs-toolkit bench (skipped, --quick)",
                          "status": Status.SKIP, "details": "", "elapsed_s": 0}]}

    bench_dir = ROOT / "docs-toolkit" / "bench"
    if not bench_dir.exists():
        return {"steps": [{"name": "bench directory",
                          "status": Status.SKIP,
                          "details": "docs-toolkit/bench/ не существует",
                          "elapsed_s": 0}]}

    t0 = time.time()
    # Просто проверим что docs-toolkit pytest идёт
    rc, tail = run_cmd(
        ["python", "-m", "pytest", "docs-toolkit/tests/",
         "-q", "--tb=no", "--timeout=60", "-x"],
        timeout=900,
    )
    return {"steps": [{
        "name": "docs-toolkit pytest",
        "status": Status.PASS if rc == 0 else Status.FAIL,
        "details": tail.split("\n")[-1] if tail else "",
        "elapsed_s": round(time.time() - t0, 1),
    }]}


def verify_docs_yml(quick: bool) -> dict:
    """docs.yml — symbolic check, реально регенерация docs идёт долго."""
    return {"steps": [{
        "name": "docs.yml: ручная регенерация",
        "status": Status.MANUAL,
        "details": "Запустить: python scripts/improve_run_all.py --fast --group reports",
        "elapsed_s": 0,
    }]}


def verify_docs_check_yml(quick: bool) -> dict:
    """docs_check.yml — валидация структуры docs/."""
    t0 = time.time()
    validate_script = ROOT / "scripts" / "improve_validate.py"
    if not validate_script.exists():
        return {"steps": [{"name": "validate", "status": Status.SKIP,
                          "details": "improve_validate.py не найден",
                          "elapsed_s": 0}]}

    rc, tail = run_cmd(["python", str(validate_script)], timeout=120)
    return {"steps": [{
        "name": "docs validation",
        "status": Status.PASS if rc == 0 else Status.FAIL,
        "details": tail.split("\n")[-1] if tail else "",
        "elapsed_s": round(time.time() - t0, 1),
    }]}


def verify_docs_portal_yml(quick: bool) -> dict:
    """docs-portal.yml — сборка docs-toolkit/docs/ в HTML."""
    portal = ROOT / "docs-toolkit" / "docs"
    if not portal.exists():
        return {"steps": [{"name": "portal source", "status": Status.SKIP,
                          "details": "docs-toolkit/docs/ нет", "elapsed_s": 0}]}
    return {"steps": [{
        "name": "portal build",
        "status": Status.MANUAL,
        "details": "Сборка статического сайта (mkdocs/sphinx) — ручная",
        "elapsed_s": 0,
    }]}


def verify_publish_toolkit_yml(quick: bool) -> dict:
    """publish-toolkit.yml — публикация в PyPI на tag."""
    return {"steps": [{
        "name": "publish (tag-only)",
        "status": Status.MANUAL,
        "details": "Триггерится только git tag toolkit-v* — не симулируем",
        "elapsed_s": 0,
    }]}


def verify_enrich_docs_yml(quick: bool) -> dict:
    """enrich-docs.yml — наш новый workflow, manual-only."""
    if quick:
        return {"steps": [{"name": "enrich scripts (skipped)",
                          "status": Status.SKIP, "details": "use --no-quick",
                          "elapsed_s": 0}]}

    # Проверим что enrichment-скрипты вообще запускаются (dry-run)
    scripts_to_check = [
        "improve_see_also.py",
        "improve_auto_toc.py",
        "improve_crosslink_all.py",
        "improve_auto_linker.py",
        "improve_subtopic_fill.py",
        "improve_abstract.py",
    ]
    results = []
    for s in scripts_to_check:
        path = ROOT / "scripts" / s
        if not path.exists():
            results.append({"name": s, "status": Status.SKIP,
                          "details": "не найден", "elapsed_s": 0})
            continue
        t0 = time.time()
        rc, tail = run_cmd(["python", str(path), "--help"], timeout=15)
        results.append({
            "name": f"{s} --help",
            "status": Status.PASS if rc == 0 else Status.FAIL,
            "details": "OK" if rc == 0 else tail[:80],
            "elapsed_s": round(time.time() - t0, 1),
        })
    return {"steps": results}


# ── Verifier registry ─────────────────────────────────────────────────────────

VERIFIERS = {
    "test.yml":              verify_test_yml,
    "benchmark.yml":         verify_benchmark_yml,
    "docs.yml":              verify_docs_yml,
    "docs_check.yml":        verify_docs_check_yml,
    "docs-portal.yml":       verify_docs_portal_yml,
    "publish-toolkit.yml":   verify_publish_toolkit_yml,
    "enrich-docs.yml":       verify_enrich_docs_yml,
}


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", help="Только этот workflow (без .yml)")
    ap.add_argument("--quick", action="store_true",
                    help="Пропустить медленные шаги (pytest)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    if not WORKFLOWS_DIR.exists():
        print(f"❌ {WORKFLOWS_DIR} не найден", file=sys.stderr)
        return 1

    report: dict = {"workflows": []}
    workflows = sorted(WORKFLOWS_DIR.glob("*.yml"))

    if args.only:
        target = args.only if args.only.endswith(".yml") else f"{args.only}.yml"
        workflows = [w for w in workflows if w.name == target]
        if not workflows:
            print(f"❌ Workflow '{target}' не найден", file=sys.stderr)
            return 1

    for wf in workflows:
        info = parse_workflow_yaml(wf)
        verifier = VERIFIERS.get(wf.name)
        if not verifier:
            steps = [{"name": "unknown workflow",
                      "status": Status.SKIP,
                      "details": "нет верификатора для этого файла",
                      "elapsed_s": 0}]
        else:
            steps = verifier(args.quick)["steps"]

        report["workflows"].append({
            **info,
            "steps": steps,
        })

    # Output
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    # Human-readable
    print("=" * 72)
    print("VERIFY ALL WORKFLOWS — локальная симуляция GitHub Actions")
    print("=" * 72)

    overall_ok = True
    for wf in report["workflows"]:
        print(f"\n📄 {wf['file']}  ({wf['name'] or '?'})")
        print(f"   Триггеры: {', '.join(wf['triggers']) or '—'}")
        if wf["cron"]:
            print(f"   Cron: {wf['cron']}")
        if wf["branches"]:
            print(f"   Ветки: {wf['branches']}")
        if wf["paths"]:
            print(f"   Paths ({len(wf['paths'])}): {wf['paths'][:3]}…")
        print(f"   Jobs: {wf['jobs']}")

        for step in wf["steps"]:
            t = f" ({step['elapsed_s']}s)" if step["elapsed_s"] else ""
            print(f"     {step['status']}  {step['name']}{t}")
            if step["details"]:
                print(f"        ↳ {step['details']}")
            if "fail" in step["status"]:
                overall_ok = False

    print()
    print("=" * 72)
    print("ИТОГ:", "✅ all workflows verifiable" if overall_ok else "❌ есть проблемы")
    print("=" * 72)
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
