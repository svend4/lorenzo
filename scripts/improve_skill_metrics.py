"""
improve_skill_metrics.py — quality metrics for .claude/skills/*.md files.

Analyses each skill file against a rubric and produces:
  docs/SKILL_METRICS.md  — ranked quality table + per-skill details
  .claude/skill_quality.json — machine-readable scores

Quality rubric (0–10 each, weighted):
  structure   (2×) — has ## Когда / ## Шаги / ## Пример sections
  length      (1×) — 200–800 words is ideal
  examples    (2×) — has code blocks or concrete examples
  steps       (2×) — numbered step list
  tools       (1×) — references Read/Bash/Edit tools or scripts
  clarity     (2×) — short sentences, no walls of text

Usage:
  python scripts/improve_skill_metrics.py          # generate report
  python scripts/improve_skill_metrics.py --top 10 # top N skills
  python scripts/improve_skill_metrics.py --low    # skills needing work
  python scripts/improve_skill_metrics.py --json   # JSON only
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT       = Path(__file__).parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"
OUT_MD     = ROOT / "docs" / "SKILL_METRICS.md"
OUT_JSON   = ROOT / ".claude" / "skill_quality.json"

USAGE_LOG  = ROOT / ".claude" / "skill_metrics.jsonl"


# ── Scoring ──────────────────────────────────────────────────────────────────

def _has_section(text: str, *patterns: str) -> bool:
    for pat in patterns:
        if re.search(rf"^##\s+{pat}", text, re.IGNORECASE | re.MULTILINE):
            return True
    return False


def score_skill(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    words = len(text.split())
    lines = text.splitlines()

    # Structure (0–10): canonical sections present
    struct = 0
    if _has_section(text, r"Когда|When|Trigger"):
        struct += 3
    if _has_section(text, r"Шаги|Steps|Как"):
        struct += 3
    if _has_section(text, r"Пример|Example|Output|Результат"):
        struct += 4

    # Length (0–10): 200-800 words ideal
    if 200 <= words <= 800:
        length_score = 10
    elif words < 100:
        length_score = 2
    elif words < 200:
        length_score = 5
    elif words <= 1200:
        length_score = 7
    else:
        length_score = 4

    # Examples (0–10): code blocks, backtick commands, concrete file paths
    code_blocks = len(re.findall(r"```", text)) // 2
    inline_code = len(re.findall(r"`[^`]{5,}`", text))
    examples_score = min(10, code_blocks * 3 + inline_code)

    # Steps (0–10): numbered list items
    numbered = len(re.findall(r"^\s*\d+\.", text, re.MULTILINE))
    steps_score = min(10, numbered * 2)

    # Tools (0–10): mentions tools/scripts
    tool_mentions = len(re.findall(
        r"Read|Bash|Edit|Write|python\s+scripts|grep|find\s+docs", text
    ))
    tools_score = min(10, tool_mentions * 2)

    # Clarity (0–10): avg sentence length 10-20 words is ideal
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s for s in sentences if len(s.split()) >= 3]
    if sentences:
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
        if 8 <= avg_len <= 22:
            clarity = 10
        elif avg_len < 5 or avg_len > 35:
            clarity = 4
        else:
            clarity = 7
    else:
        clarity = 3

    # Weighted total (max 100)
    total = (
        struct        * 2 +
        length_score  * 1 +
        examples_score * 2 +
        steps_score   * 2 +
        tools_score   * 1 +
        clarity       * 2
    )
    # total max = 10*2 + 10*1 + 10*2 + 10*2 + 10*1 + 10*2 = 100

    return {
        "skill":         path.stem,
        "path":          str(path.relative_to(ROOT)),
        "words":         words,
        "total":         total,
        "structure":     struct,
        "length":        length_score,
        "examples":      examples_score,
        "steps":         steps_score,
        "tools":         tools_score,
        "clarity":       clarity,
        "code_blocks":   code_blocks,
        "numbered_steps": numbered,
    }


# ── Usage stats ───────────────────────────────────────────────────────────────

def load_usage() -> dict[str, int]:
    if not USAGE_LOG.exists():
        return {}
    counts: dict[str, int] = {}
    for line in USAGE_LOG.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
            sk = e.get("skill", "")
            if sk:
                counts[sk] = counts.get(sk, 0) + 1
        except json.JSONDecodeError:
            continue
    return counts


# ── Report ────────────────────────────────────────────────────────────────────

def build_report(scores: list[dict], usage: dict[str, int]) -> str:
    date = datetime.now().strftime("%Y-%m-%d")
    avg  = sum(s["total"] for s in scores) / max(len(scores), 1)
    good = sum(1 for s in scores if s["total"] >= 70)
    poor = sum(1 for s in scores if s["total"] < 50)

    lines = [
        "# Skill Quality Metrics — Svyazi 2.0",
        "",
        f"_Сгенерировано: {date}_",
        "",
        f"**Скилов:** {len(scores)}  "
        f"**Среднее качество:** {avg:.0f}/100  "
        f"**Хороших (≥70):** {good}  "
        f"**Требуют доработки (<50):** {poor}",
        "",
        "## Рейтинг качества",
        "",
        "| Скил | Score | Struct | Len | Examples | Steps | Tools | Clarity | Uses | Words |",
        "|------|-------|--------|-----|----------|-------|-------|---------|------|-------|",
    ]

    for s in scores:
        uses = usage.get(s["skill"], 0)
        grade = "✅" if s["total"] >= 70 else ("⚠️" if s["total"] >= 50 else "❌")
        lines.append(
            f"| {grade} `{s['skill']}` | **{s['total']}** "
            f"| {s['structure']} | {s['length']} | {s['examples']} "
            f"| {s['steps']} | {s['tools']} | {s['clarity']} "
            f"| {uses} | {s['words']} |"
        )

    lines += [
        "",
        "## Улучшение скилов",
        "",
        "Скилы с низким score (<50) — кандидаты на доработку:",
        "",
    ]
    for s in scores:
        if s["total"] >= 50:
            continue
        issues = []
        if s["structure"] < 6:
            issues.append("добавить секции `## Когда`, `## Шаги`, `## Пример`")
        if s["examples"] < 4:
            issues.append("добавить примеры кода/команд")
        if s["steps"] < 4:
            issues.append("добавить нумерованные шаги")
        if s["length"] < 5:
            issues.append(f"расширить ({s['words']} слов, оптимально 200-800)")
        if issues:
            lines.append(f"**`{s['skill']}`** ({s['total']}/100): " + "; ".join(issues))

    return "\n".join(lines) + "\n"


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args    = sys.argv[1:]
    top_n   = 0
    low_only = "--low" in args
    json_only = "--json" in args

    for i, a in enumerate(args):
        if a == "--top" and i + 1 < len(args):
            try:
                top_n = int(args[i + 1])
            except ValueError:
                pass

    if not SKILLS_DIR.exists():
        print(f"⚠ Директория скилов не найдена: {SKILLS_DIR}")
        return 1

    skill_files = [
        p for p in SKILLS_DIR.glob("*.md")
        if not p.stem.startswith("_")
    ]
    if not skill_files:
        print("⚠ Скилы не найдены.")
        return 1

    scores = [score_skill(p) for p in skill_files]
    scores.sort(key=lambda s: -s["total"])

    if top_n:
        scores = scores[:top_n]
    if low_only:
        scores = [s for s in scores if s["total"] < 50]

    usage = load_usage()

    if json_only:
        print(json.dumps(scores, ensure_ascii=False, indent=2))
        return 0

    # Write outputs
    report = build_report(scores, usage)
    OUT_MD.write_text(report, encoding="utf-8")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps({
            "generated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "count": len(scores),
            "avg_score": round(sum(s["total"] for s in scores) / max(len(scores), 1), 1),
            "skills": scores,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    avg = sum(s["total"] for s in scores) / max(len(scores), 1)
    good = sum(1 for s in scores if s["total"] >= 70)
    poor = sum(1 for s in scores if s["total"] < 50)

    print(f"📊 Skill Quality Metrics")
    print(f"   Скилов:       {len(scores)}")
    print(f"   Средний балл: {avg:.0f}/100")
    print(f"   Хороших (≥70): {good}")
    print(f"   Слабых (<50):  {poor}")
    print(f"\n✅ {OUT_MD.relative_to(ROOT)}")

    print(f"\n— Топ-10 —")
    for s in scores[:10]:
        grade = "✅" if s["total"] >= 70 else ("⚠️" if s["total"] >= 50 else "❌")
        print(f"  {grade} {s['total']:3d}/100  {s['skill']}")

    if poor > 0 and not low_only:
        print(f"\n— Слабые скилы (< 50) —")
        for s in scores:
            if s["total"] < 50:
                print(f"  ❌ {s['total']:3d}/100  {s['skill']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
