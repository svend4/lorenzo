"""
improve_contradiction_check.py — поиск противоречивых утверждений в базе знаний.

Ищет предложения, содержащие одни и те же сущности, но противоположные утверждения:
  - Числа: «X имеет 5 компонентов» vs «X имеет 8 компонентов»
  - Булевы: «X поддерживает Y» vs «X не поддерживает Y»
  - Версии: «версия 1.0» vs «версия 2.0» (об одном и том же)
  - Факты с «является/это» vs «не является/не это»

Создаёт docs/CONTRADICTIONS.md.
Запуск:
    python scripts/improve_contradiction_check.py
    python scripts/improve_contradiction_check.py --section 05-habr-projects
    python scripts/improve_contradiction_check.py --min-confidence 0.5
"""
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MIN_CONFIDENCE = 0.4
if "--min-confidence" in sys.argv:
    idx = sys.argv.index("--min-confidence")
    if idx + 1 < len(sys.argv):
        MIN_CONFIDENCE = float(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "CONTRADICTIONS.md", "SEARCH.md", "READABILITY.md",
    "TIMELINE.md", "NAMED_ENTITIES.md", "SOURCE_MAP.md",
    "READING_ORDER.md", "SITEMAP.md", "OUTLINE.md",
    "CONCEPT_GRAPH.md", "KEYWORD_INDEX.md", "PARAGRAPH_QUALITY.md",
    "VOCABULARY.md", "COVERAGE.md", "HEATMAP.md", "GRAPH.md",
    "TABLES.md", "CONSISTENCY.md", "METRICS.md", "HEALTH.md",
}

# Числа меньше MIN_NUM игнорируются как нумерация списков
MIN_NUM = 3.0

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "что", "был", "the", "a", "an", "is", "of", "in",
    "on", "to", "for", "with", "by", "and", "it", "we",
}

# ─── Извлечение claim'ов ───────────────────────────────────────────────────

NUMBER_RE = re.compile(r'\b(\d+(?:[.,]\d+)?)\s*(%|тыс|млн|млрд|k|m|gb|mb|ms|s)?\b')
VERSION_RE = re.compile(r'\bv?(\d+\.\d+(?:\.\d+)?)\b')
NEG_RE     = re.compile(r'\bне\s+\w+|\bнет\b|\bno\b|\bnot\b|\bdoesn.t\b|\bdon.t\b', re.I)


def _clean_sentence(s: str) -> str:
    s = re.sub(r'[*_`#|>\[\]]', '', s)
    s = re.sub(r'https?://\S+', '[URL]', s)
    # убираем bare URL-пути вида domain.com/path/123/
    s = re.sub(r'\b\w+\.\w{2,4}/\S+', '[URL]', s)
    return re.sub(r'\s+', ' ', s).strip()


def _keywords(sentence: str, n: int = 6) -> frozenset[str]:
    tokens = re.findall(r'[а-яёa-z]{3,}', sentence.lower())
    filtered = [t for t in tokens if t not in STOPWORDS]
    return frozenset(filtered[:n])


def _extract_claims(text: str, source: str) -> list[dict]:
    """Извлекает утверждения вида {subject, predicate_type, value, sentence, source}."""
    clean_text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean_text = re.sub(r'<!--.*?-->', ' ', clean_text, flags=re.DOTALL)
    sentences = [s.strip() for s in re.split(r'[.!?]+', clean_text) if len(s.strip()) > 20]

    claims = []
    for sent in sentences:
        sent_clean = _clean_sentence(sent)
        kw = _keywords(sent_clean)
        if len(kw) < 2:
            continue

        # Числовые утверждения (пропускаем маленькие числа — нумерация списков)
        for m in NUMBER_RE.finditer(sent_clean):
            num = float(m.group(1).replace(',', '.'))
            if num < MIN_NUM:
                continue
            claims.append({
                "type": "numeric",
                "keywords": kw,
                "value": num,
                "negated": bool(NEG_RE.search(sent_clean[:m.start()])),
                "sentence": sent_clean[:200],
                "source": source,
            })

        # Версии
        for m in VERSION_RE.finditer(sent_clean):
            claims.append({
                "type": "version",
                "keywords": kw,
                "value": m.group(1),
                "negated": False,
                "sentence": sent_clean[:200],
                "source": source,
            })

        # Булевы (есть vs нет)
        has_neg = bool(NEG_RE.search(sent_clean))
        has_affirm = bool(re.search(
            r'\bподдержива[её]т\b|\bимеет\b|\bявляется\b|\bвключает\b'
            r'|\bsupport[s]?\b|\bhas\b|\bis\b|\bprovid[es]+\b',
            sent_clean, re.I
        ))
        if has_affirm or has_neg:
            claims.append({
                "type": "boolean",
                "keywords": kw,
                "value": "false" if has_neg else "true",
                "negated": has_neg,
                "sentence": sent_clean[:200],
                "source": source,
            })

    return claims


def _keywords_overlap(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


MAX_BUCKET = 50  # пропускаем слишком общие ключевые слова


def _find_contradictions(all_claims: list[dict]) -> list[dict]:
    """Ищет противоречия через инвертированный keyword-индекс (не O(n²))."""
    from collections import defaultdict

    # Строим индекс: (type, keyword) → [claim_idx]
    inv: dict[tuple, list[int]] = defaultdict(list)
    for idx, c in enumerate(all_claims):
        for kw in c["keywords"]:
            inv[(c["type"], kw)].append(idx)

    seen: set[tuple] = set()
    contradictions = []

    for (claim_type, kw), idxs in inv.items():
        if len(idxs) < 2 or len(idxs) > MAX_BUCKET:
            continue
        # Проверяем только пары в пределах этого bucket
        for ii in range(len(idxs)):
            for jj in range(ii + 1, len(idxs)):
                i, j = idxs[ii], idxs[jj]
                pair_key = (min(i, j), max(i, j))
                if pair_key in seen:
                    continue
                seen.add(pair_key)

                ci, cj = all_claims[i], all_claims[j]
                if ci["source"] == cj["source"]:
                    continue

                kw_sim = _keywords_overlap(ci["keywords"], cj["keywords"])
                if kw_sim < 0.3:
                    continue

                contradiction = False
                detail = ""

                if ci["type"] == "numeric":
                    if ci["value"] != cj["value"]:
                        denom = max(ci["value"], cj["value"])
                        ratio = min(ci["value"], cj["value"]) / denom if denom else 1.0
                        if ratio < 0.7:
                            contradiction = True
                            detail = f"{ci['value']} vs {cj['value']}"

                elif ci["type"] == "version":
                    if ci["value"] != cj["value"]:
                        contradiction = True
                        detail = f"v{ci['value']} vs v{cj['value']}"

                elif ci["type"] == "boolean":
                    if ci["value"] != cj["value"]:
                        contradiction = True
                        detail = "утверждение vs отрицание"

                if contradiction:
                    confidence = kw_sim * (0.8 if ci["type"] in ("version", "numeric") else 0.5)
                    if confidence >= MIN_CONFIDENCE:
                        contradictions.append({
                            "type": ci["type"],
                            "detail": detail,
                            "confidence": round(confidence, 2),
                            "keywords": sorted(ci["keywords"] & cj["keywords"])[:5],
                            "claim_a": {"sentence": ci["sentence"], "source": ci["source"]},
                            "claim_b": {"sentence": cj["sentence"], "source": cj["source"]},
                            "_dedup_key": tuple(sorted([ci["source"], cj["source"]])) + (detail,),
                        })

    # Дедупликация: одна пара предложений → одно противоречие (лучшая уверенность)
    dedup: dict = {}
    for c in contradictions:
        sent_key = (c["claim_a"]["sentence"][:80], c["claim_b"]["sentence"][:80])
        norm_key = tuple(sorted(sent_key))
        if norm_key not in dedup or c["confidence"] > dedup[norm_key]["confidence"]:
            dedup[norm_key] = c
    result = [{k: v for k, v in c.items() if k != "_dedup_key"} for c in dedup.values()]
    return sorted(result, key=lambda x: -x["confidence"])


def main() -> None:
    print("⚡ improve_contradiction_check.py — поиск противоречий")
    print(f"   Мин. уверенность: {MIN_CONFIDENCE}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "obsidian" not in str(f)
             and "confluence" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    all_claims = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(f.relative_to(ROOT))
        claims = _extract_claims(text, rel)
        all_claims.extend(claims)

    print(f"   Утверждений извлечено: {len(all_claims)}")
    print("   Поиск противоречий...", end=" ", flush=True)

    contradictions = _find_contradictions(all_claims)
    print(f"найдено: {len(contradictions)}\n")

    TYPE_LABELS = {
        "numeric": "🔢 Числовое",
        "version": "📦 Версия",
        "boolean": "✅/❌ Булево",
    }

    lines = [
        "# Противоречия в базе знаний\n",
        f"_Обновлено: {TODAY}_\n",
        f"Утверждений: **{len(all_claims)}** | Противоречий: **{len(contradictions)}**\n",
        "> Автоматический поиск без LLM — возможны ложные срабатывания.\n",
    ]

    if contradictions:
        lines += ["## Найденные противоречия\n"]
        for i, c in enumerate(contradictions[:30], 1):
            t = TYPE_LABELS.get(c["type"], c["type"])
            kw = ', '.join(f'`{k}`' for k in c["keywords"][:4])
            lines += [
                f"### {i}. {t} — {c['detail']} (уверенность: {c['confidence']})\n",
                f"**Общие ключевые слова:** {kw}\n",
                f"**A:** `{c['claim_a']['source']}`",
                f"> {c['claim_a']['sentence'][:150]}\n",
                f"**B:** `{c['claim_b']['source']}`",
                f"> {c['claim_b']['sentence'][:150]}\n",
                "---\n",
            ]
    else:
        lines.append("_Противоречий не найдено при текущем пороге уверенности._\n")

    out = DOCS / "CONTRADICTIONS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  противоречий: {len(contradictions)}")


if __name__ == "__main__":
    main()
