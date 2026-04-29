"""
improve_paragraph_quality.py — находит проблемные абзацы в документах.

Проверяет:
  - Слишком короткие абзацы (< MIN_SENTENCES предложений)
  - Копипаста: абзац почти идентичен другому в том же файле (Jaccard > 0.8)
  - «Водяные» абзацы: много союзов/местоимений, мало ключевых слов
  - «Оборванные»: заканчиваются без знака препинания
  - Повторяющиеся начала: три подряд абзаца с одного слова
  - Сверхдлинные предложения: > MAX_SENT_WORDS слов

Создаёт docs/PARAGRAPH_QUALITY.md.
Запуск:
    python scripts/improve_paragraph_quality.py
    python scripts/improve_paragraph_quality.py --section 02-anthropic-vacancies
    python scripts/improve_paragraph_quality.py --verbose
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

VERBOSE = "--verbose" in sys.argv

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "PARAGRAPH_QUALITY.md", "SEARCH.md", "READABILITY.md",
    "OUTLINE.md", "TIMELINE.md", "NAMED_ENTITIES.md",
}

MIN_PARA_WORDS   = 15     # абзац с меньшим числом слов — «короткий»
MAX_SENT_WORDS   = 60     # предложение длиннее — «сверхдлинное»
WATER_THRESHOLD  = 0.55   # доля стоп-слов выше — «водяной»
DUP_THRESHOLD    = 0.75   # Jaccard для обнаружения дублей внутри файла

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "он", "она", "они", "мы", "вы",
    "его", "её", "их", "мне", "тебе", "всё", "при", "от", "до", "об",
    "же", "бы", "ли", "да", "нет", "есть", "была", "были", "будет",
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "can", "could", "should", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "or", "and", "not", "but", "it",
    "its", "we", "you", "they", "their", "our", "this", "that",
}


def _paragraphs(text: str) -> list[str]:
    """Извлекает абзацы, убирая markdown-элементы."""
    clean = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    clean = re.sub(r'<!--.*?-->', '', clean, flags=re.DOTALL)
    clean = re.sub(r'^#{1,6}\s+.+$', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^\|.+\|$', '', clean, flags=re.MULTILINE)  # таблицы
    clean = re.sub(r'^[-*]\s+', '', clean, flags=re.MULTILINE)   # списки → текст
    paras = [p.strip() for p in re.split(r'\n{2,}', clean) if len(p.strip()) > 10]
    return paras


def _tokens(text: str) -> list[str]:
    return re.findall(r'[а-яёa-z]{3,}', text.lower())


def _jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    return len(sa & sb) / max(1, len(sa | sb))


def _water_ratio(para: str) -> float:
    """Доля стоп-слов в абзаце."""
    tokens = _tokens(para)
    if not tokens:
        return 0.0
    stops = sum(1 for t in tokens if t in STOPWORDS)
    return stops / len(tokens)


def _is_truncated(para: str) -> bool:
    """Абзац обрывается без знака препинания."""
    stripped = para.strip()
    return bool(stripped) and stripped[-1] not in '.!?:;»"'


def _max_sentence_length(para: str) -> int:
    """Максимальная длина предложения в словах."""
    sents = re.split(r'[.!?]+', para)
    return max((len(s.split()) for s in sents if s.strip()), default=0)


def _repeating_starts(paras: list[str]) -> list[int]:
    """Индексы абзацев с повторяющимися начальными словами (3+ подряд)."""
    result = []
    starts = []
    for para in paras:
        words = _tokens(para)
        starts.append(words[0] if words else "")

    for i in range(2, len(starts)):
        if starts[i] == starts[i-1] == starts[i-2] and starts[i]:
            result.extend([i-2, i-1, i])

    return list(set(result))


def analyze_file(path: Path) -> list[dict]:
    """Возвращает список проблем [{type, para_idx, para_text, detail}]."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []

    paras = _paragraphs(text)
    if not paras:
        return []

    issues = []
    tokens_cache = [_tokens(p) for p in paras]
    rep_starts = set(_repeating_starts(paras))

    for i, para in enumerate(paras):
        toks = tokens_cache[i]
        wc = len(para.split())

        if wc < MIN_PARA_WORDS and wc > 3:
            issues.append({
                "type": "short", "idx": i,
                "text": para[:100],
                "detail": f"{wc} слов",
            })

        water = _water_ratio(para)
        if water > WATER_THRESHOLD and wc > 20:
            issues.append({
                "type": "watery", "idx": i,
                "text": para[:100],
                "detail": f"{water*100:.0f}% стоп-слов",
            })

        if _is_truncated(para) and wc > 10:
            issues.append({
                "type": "truncated", "idx": i,
                "text": para[:100],
                "detail": "нет знака в конце",
            })

        max_sent = _max_sentence_length(para)
        if max_sent > MAX_SENT_WORDS:
            issues.append({
                "type": "long_sentence", "idx": i,
                "text": para[:100],
                "detail": f"предложение {max_sent} слов",
            })

        if i in rep_starts:
            issues.append({
                "type": "repeat_start", "idx": i,
                "text": para[:100],
                "detail": f"начинается со слова '{toks[0] if toks else '?'}'",
            })

        # Дубли внутри файла
        for j in range(i + 1, min(i + 20, len(paras))):
            if _jaccard(toks, tokens_cache[j]) > DUP_THRESHOLD and len(toks) > 8:
                issues.append({
                    "type": "duplicate", "idx": i,
                    "text": para[:100],
                    "detail": f"дубль с абзацем #{j+1}",
                })
                break

    return issues


def main() -> None:
    print("🔎 improve_paragraph_quality.py — качество абзацев")
    if VERBOSE:
        print("   Режим: verbose\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    all_results: dict[str, list] = {}
    type_counts: Counter = Counter()

    for f in files:
        issues = analyze_file(f)
        if issues:
            all_results[str(f.relative_to(ROOT))] = issues
            for iss in issues:
                type_counts[iss["type"]] += 1

    TYPE_LABELS = {
        "short":        "⚪ Короткий абзац",
        "watery":       "💧 Водяной текст",
        "truncated":    "✂️  Оборванный",
        "long_sentence":"📏 Длинное предложение",
        "repeat_start": "🔁 Повтор начала",
        "duplicate":    "♊ Дубль",
    }

    lines = [
        "# Качество абзацев\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов с проблемами: **{len(all_results)}**\n",
        "## Типы проблем\n",
        "| Тип | Кол-во |",
        "|-----|--------|",
    ]
    for t, label in TYPE_LABELS.items():
        if type_counts[t]:
            lines.append(f"| {label} | {type_counts[t]} |")

    lines += ["\n## По файлам\n"]
    for fpath, issues in sorted(all_results.items(), key=lambda x: -len(x[1])):
        lines.append(f"### `{fpath}` ({len(issues)} проблем)\n")
        type_summary = Counter(iss["type"] for iss in issues)
        summary_str = ', '.join(f"{TYPE_LABELS[t].split()[-1]}: {n}" for t, n in type_summary.items())
        lines.append(f"_{summary_str}_\n")
        if VERBOSE:
            for iss in issues[:10]:
                label = TYPE_LABELS.get(iss["type"], iss["type"])
                lines.append(f"- {label} — {iss['detail']}")
                lines.append(f"  > {iss['text'][:80]}...")
        lines.append("")

    out = DOCS / "PARAGRAPH_QUALITY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  файлов с проблемами: {len(all_results)}")
    for t, cnt in type_counts.most_common():
        print(f"  {TYPE_LABELS.get(t, t)}: {cnt}")


if __name__ == "__main__":
    main()
