"""
improve_missing.py — находит темы/проекты упомянутые в документах
но слабо раскрытые (мало файлов, мало слов).
Создаёт docs/MISSING.md — карту пробелов знаний.
Запуск: python scripts/improve_missing.py
"""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Ожидаемые темы и их минимальный порог раскрытия (файлов)
EXPECTED_COVERAGE = {
    # Проекты
    "Svyazi":          {"min_files": 5,  "min_words": 2000},
    "CardIndex":       {"min_files": 3,  "min_words": 500},
    "AgentFS":         {"min_files": 3,  "min_words": 500},
    "knowledge-space": {"min_files": 3,  "min_words": 500},
    "Yodoca":          {"min_files": 2,  "min_words": 300},
    "NGT Memory":      {"min_files": 2,  "min_words": 300},
    "LiteParse":       {"min_files": 2,  "min_words": 300},
    "SENTINEL":        {"min_files": 2,  "min_words": 200},
    "mclaude":         {"min_files": 2,  "min_words": 200},
    "AI Factory":      {"min_files": 2,  "min_words": 200},
    "Rufler":          {"min_files": 2,  "min_words": 200},
    # Архитектурные концепции
    "Evidence Envelope":     {"min_files": 2, "min_words": 200},
    "Card Envelope":         {"min_files": 2, "min_words": 200},
    "Memory Write Policy":   {"min_files": 2, "min_words": 200},
    "Skill Policy":          {"min_files": 1, "min_words": 100},
    "Review Record":         {"min_files": 1, "min_words": 100},
    # Темы
    "бюджетный роутинг":     {"min_files": 2, "min_words": 300},
    "privacy by design":     {"min_files": 1, "min_words": 100},
    "local-first":           {"min_files": 2, "min_words": 300},
    "CRDT":                  {"min_files": 1, "min_words": 100},
    "лицензия BSL":          {"min_files": 1, "min_words": 50},
    "AutoResearch":          {"min_files": 1, "min_words": 100},
    "self-improvement":      {"min_files": 1, "min_words": 100},
    "voice ingestion":       {"min_files": 1, "min_words": 100},
    "Sozialrecht":           {"min_files": 1, "min_words": 200},
}


def measure_coverage(term: str) -> dict:
    """Считает сколько файлов и слов содержат термин."""
    files = []
    total_words = 0
    low_term = term.lower()

    for f in DOCS.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        if low_term in text.lower():
            files.append(str(f.relative_to(ROOT)))
            # Слова в абзацах где упоминается термин
            for para in text.split("\n\n"):
                if low_term in para.lower():
                    total_words += len(para.split())

    return {"files": files, "words": total_words}


def main():
    print("Анализ пробелов в документации...")
    results = []

    for term, thresholds in EXPECTED_COVERAGE.items():
        cov = measure_coverage(term)
        files_ok = len(cov["files"]) >= thresholds["min_files"]
        words_ok = cov["words"] >= thresholds["min_words"]
        status = "✅" if (files_ok and words_ok) else ("⚠️" if cov["files"] else "❌")
        results.append({
            "term": term,
            "status": status,
            "files": len(cov["files"]),
            "words": cov["words"],
            "min_files": thresholds["min_files"],
            "min_words": thresholds["min_words"],
            "sample_files": cov["files"][:2],
        })

    # Сортируем: сначала проблемные
    results.sort(key=lambda x: (x["status"] == "✅", -x["files"]))

    lines = [
        "# Карта пробелов знаний\n",
        "Анализ покрытия ключевых тем и проектов в docs/.\n",
        "| Статус | Тема / Проект | Файлов | Слов | Минимум | Примеры файлов |",
        "|--------|---------------|--------|------|---------|----------------|",
    ]

    for r in results:
        sample = ", ".join(f"`{f.split('/')[-1]}`" for f in r["sample_files"])
        lines.append(
            f"| {r['status']} | **{r['term']}** | {r['files']} | {r['words']} "
            f"| ≥{r['min_files']}ф/{r['min_words']}сл | {sample} |"
        )

    # Итог
    ok = sum(1 for r in results if r["status"] == "✅")
    warn = sum(1 for r in results if r["status"] == "⚠️")
    bad = sum(1 for r in results if r["status"] == "❌")

    lines += [
        f"\n## Итог\n",
        f"- ✅ Хорошо раскрыто: **{ok}**",
        f"- ⚠️ Слабо раскрыто: **{warn}**",
        f"- ❌ Отсутствует: **{bad}**\n",
        "## Рекомендации\n",
        "Темы со статусом ❌ или ⚠️ нужно дополнить отдельными документами.",
    ]

    out = DOCS / "MISSING.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  ✅ {ok}  ⚠️ {warn}  ❌ {bad}")


if __name__ == "__main__":
    main()
